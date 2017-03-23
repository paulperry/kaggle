library(data.table)
library(fastfurious)
library(Hmisc)
library(Matrix)
library(plyr)

### FUNCS

### CONFIG 

### FAST-FURIOUS 
ff.setBasePath(path = '/Users/gino/kaggle/fast-furious/gitHub/fast-furious/')
ff.bindPath(type = 'data' , sub_path = 'dataset/deloitte-western-australia-rental-prices/data')
ff.bindPath(type = 'code' , sub_path = 'competitions/deloitte-western-australia-rental-prices')
ff.bindPath(type = 'elab' , sub_path = 'dataset/deloitte-western-australia-rental-prices/elab' ,  createDir = T) 

####
source(paste0(ff.getPath("code"),"fastImpute.R"))

## DATA 
train = as.data.frame( fread(paste(ff.getPath("data") , "train.csv" , sep='') , stringsAsFactors = F))
test = as.data.frame( fread(paste(ff.getPath("data") , "test.csv" , sep='') , stringsAsFactors = F))

land_admin_areas = as.data.frame( fread(paste(ff.getPath("data") , "land_admin_areas.csv" , sep='') , stringsAsFactors = F))
land_pins = as.data.frame( fread(paste(ff.getPath("data") , "land_pins.csv" , sep='') , stringsAsFactors = F))
land = as.data.frame( fread(paste(ff.getPath("data") , "land.csv" , sep='') , stringsAsFactors = F))
land_restrictions = as.data.frame( fread(paste(ff.getPath("data") , "land_restrictions.csv" , sep='') , stringsAsFactors = F))
land_urban = as.data.frame( fread(paste(ff.getPath("data") , "land_urban.csv" , sep='') , stringsAsFactors = F))
land_valuation_key = as.data.frame( fread(paste(ff.getPath("data") , "land_valuation_key.csv" , sep='') , stringsAsFactors = F))
land_zonings = as.data.frame( fread(paste(ff.getPath("data") , "land_zonings.csv" , sep='') , stringsAsFactors = F))

valuation_entities = as.data.frame( fread(paste(ff.getPath("data") , "valuation_entities.csv" , sep='') , stringsAsFactors = F)) 
valuation_entities_classifications = as.data.frame( fread(paste(ff.getPath("data") , "valuation_entities_classifications.csv" , sep='') , 
                                                          stringsAsFactors = F))  
valuation_entities_details = as.data.frame( fread(paste(ff.getPath("data") , "valuation_entities_details.csv" , sep='') , 
                                                  stringsAsFactors = F))  

points_of_interest = as.data.frame( fread(paste(ff.getPath("data") , "points_of_interest.csv" , sep='') , 
                                                  stringsAsFactors = F))  
demographics = as.data.frame( fread(paste(ff.getPath("data") , "demographics.csv" , sep='') , 
                                          stringsAsFactors = F))  
demographics_key = as.data.frame( fread(paste(ff.getPath("data") , "demographics_key.csv" , sep='') , 
                                          stringsAsFactors = F))  
distances = as.data.frame( fread(paste(ff.getPath("data") , "distances.csv" , sep='') , 
                                        stringsAsFactors = F))  

## PROCS 

############################################################################
#############   TRAIN / TEST   #############################################
############################################################################

##### FINAL 

# remove NAs 
obsNAs = ff.obsNA(train)

# Ytrain
train = train[-obsNAs,]
Ytrain = train$REN_BASE_RENT

# remove REN_LEASE_LENGTH and REN_BASE_RENT (only in train)
predToDel = "REN_LEASE_LENGTH"
train = train [, -grep(pattern = paste(predToDel , "REN_BASE_RENT" , sep = "|") , x = colnames(train))]
test = test [, -grep(pattern = predToDel  , x = colnames(test))]

# makefeature 
train$REN_DATE_EFF_FROM = as.Date(train$REN_DATE_EFF_FROM)
test$REN_DATE_EFF_FROM = as.Date(test$REN_DATE_EFF_FROM)
l = ff.makeFeatureSet(data.train = train , data.test = test , meta = c("N","D","N"))
train = l$traindata
test = l$testdata
rm(l)

train = cbind(train,Ytrain=Ytrain)

############################################################################
#############   LAND           #############################################
############################################################################

### land
sum(is.na(land))

predNAs = ff.predNA(data = land,asIndex=F)
for (pp in predNAs) {
  perc = sum(is.na(land[,pp]))/nrow(land)
  cat("[",pp,"]:",perc,"-- NAs",sum(is.na(land[,pp])),"\n")
}

predToDel = c("LAN_LDS_NUMBER","LAN_LDS_NUMBER_ID_TYPE3","LAN_DATE_SUBDIVISION_LGA","LAN_DATE_SUBDIVISION_WAPC" , "LAN_SKETCH_ID" , 
              "LAN_ID1_PART_LOT" , "LAN_ID2_LOT" , "LAN_ID2_LOT" , "LAN_ID2_PART_LOT" , "LAN_ID3_PART_LOT" , "LAN_DATE_SURVEY_STRATA", 
              "LAN_DATE_LEASE_EXPIRY" , "LAN_DATE_LEASE_FROM" , "LAN_STR_ID_HAS_CORNER" )

for (pp in predToDel) land[,pp] <- NULL

## impute 
land$LAN_LDS_NUMBER_IS_RURAL[is.na(land$LAN_LDS_NUMBER_IS_RURAL)] <- -1 
land$LAN_ID1_LOT_NO[is.na(land$LAN_ID1_LOT_NO)] <- -1 
land$LLG_DATE_EFF_FROM[is.na(land$LLG_DATE_EFF_FROM)] <- "1849-01-01"
land$SUB_POSTCODE[is.na(land$SUB_POSTCODE)] <- -1 
land$URT_DATE_EFF_FROM[is.na(land$URT_DATE_EFF_FROM)] <- "1849-01-01"

sum(is.na(land))

## date 
land$LAN_DATE_SUBDIVISION_MFP = as.Date(land$LAN_DATE_SUBDIVISION_MFP)
land$LLG_DATE_EFF_FROM = as.Date(land$LLG_DATE_EFF_FROM)
land$URT_DATE_EFF_FROM = as.Date(land$URT_DATE_EFF_FROM)

## categ 
feature.names = colnames(land)
for (f in feature.names) {
  if (class(land[,f])=="character") {
    cat(">>> ",f," is character \n")
    levels <- unique(land[,f])
    land[,f] <- as.integer(factor(land[,f], levels=levels))
  }
}

## encode 
## dates index: 10 , 39 , 50 
meta_land = c(rep("N",9),"D",rep("N",28),"D",rep("N",10),"D","N")
l = ff.makeFeatureSet(data.train = land , data.test = land , meta = meta_land , 
                      scaleNumericFeatures = F , parallelize = F , remove1DummyVarInCatPreds = F)
land = l$traindata
rm(l)

### land_valuation_key
sum(! unique(land_valuation_key$VE_NUMBER) %in% unique(c(train$VE_NUMBER,test$VE_NUMBER)) ) ## 867777 
sum(! unique(c(train$VE_NUMBER)) %in%  unique(land_valuation_key$VE_NUMBER) ) # 3 
sum(! unique(c(test$VE_NUMBER)) %in%  unique(land_valuation_key$VE_NUMBER) ) # 0 

## remove such 3 VEN from train set 
VEN_remove = setdiff(x = unique(train$VE_NUMBER) , y = unique(land_valuation_key$VE_NUMBER))
train = train[! train$VE_NUMBER %in% VEN_remove,]

## remove from land VE_NUMBER not occurring either in train set or test set 
VEN_remove =  setdiff(x = unique(land_valuation_key$VE_NUMBER) , y = c(train$VE_NUMBER,test$VE_NUMBER) )
land_valuation_key = land_valuation_key[! land_valuation_key$VE_NUMBER %in% VEN_remove,,drop=F]

## LAN_ID e' unique in land_valuation_key ? ... no 
length(land_valuation_key$LAN_ID) == length(unique(land_valuation_key$LAN_ID))

## VE_NUMBER e' unique in land_valuation_key ? .. no 
length(land_valuation_key$VE_NUMBER) == length(unique(land_valuation_key$VE_NUMBER))

head(sort(table(land_valuation_key$VE_NUMBER),decreasing = T),100)
#4544602 4670844 1579901 2528154  730167 2728706 3469023 4074201 4403945 ..
#   20       7       6       6       5       5       5       5       5  ...

land_valuation_key[land_valuation_key$VE_NUMBER == 4544602,]
#   LAN_ID VE_NUMBER
#  1082263   4544602
#   684025   4544602
#  2327936   4544602
#  ...         ... 

lvkd = table(land_valuation_key$VE_NUMBER)
sum(lvkd>1) ##1694 
lvkd = lvkd[lvkd>1]
ve_lvkd = as.numeric(names(lvkd))
sum(unique(train$VE_NUMBER) %in% ve_lvkd) #1410
sum(unique(test$VE_NUMBER) %in% ve_lvkd) #688
te_lvdk = unique(test$VE_NUMBER)[unique(test$VE_NUMBER) %in% ve_lvkd]
mean(lvkd[names(lvkd) %in% te_lvdk]) ## 2.321221 

# 7624 19456 25805 39584 72903 77429 
# 2     2     2     2     2     3

ve = 7624
land_valuation_key[land_valuation_key$VE_NUMBER==ve,]

# LAN_ID VE_NUMBER
#  3427801      7624
#  4074461      7624

land[land$LAN_ID %in% land_valuation_key[land_valuation_key$VE_NUMBER==ve,]$LAN_ID,]

## >>> no rule. 100% pure noise. you have to cut without a criterion !!
for (ve in ve_lvkd) {
  li = land_valuation_key[land_valuation_key$VE_NUMBER==ve,]$LAN_ID
  ## maybe, last one is more updated??
  land_valuation_key = land_valuation_key[ ! (land_valuation_key$VE_NUMBER==ve & land_valuation_key$LAN_ID %in% li[1:(length(li)-1)]),]
}

## remove from land LAN_ID not occurring in land_valuation_key
sum(! (unique(land_valuation_key$LAN_ID) %in% unique(land$LAN_ID))  ) ## 0 
sum(! (unique(land$LAN_ID) %in% unique(land_valuation_key$LAN_ID))  ) ## 885370 
LD_remove =  setdiff(x = unique(land$LAN_ID) , y = unique(land_valuation_key$LAN_ID) )
land = land[! land$LAN_ID %in% LD_remove,,drop=F]

## joins 
sum(! (land_valuation_key$LAN_ID %in% land$LAN_ID) ) #0
sum(! (land$LAN_ID %in% land_valuation_key$LAN_ID) ) #0 
land = merge(x = land , y = land_valuation_key , by="LAN_ID" , all = F)

## Xtrain
sum(! (train$VE_NUMBER %in% land$VE_NUMBER) ) #0
Xtrain = merge(x = train , y = land , by = "VE_NUMBER" , all=F)
stopifnot(nrow(Xtrain)==nrow(train))
cat(">>> Xtrain:",dim(Xtrain),"\n")
Xtrain.n_now = nrow(Xtrain)

## Xtest
sum(! (test$VE_NUMBER %in% land$VE_NUMBER) ) #0
Xtest = merge(x = test , y = land , by = "VE_NUMBER" , all = F)
stopifnot(nrow(Xtest)==nrow(test))
cat(">>> Xtest:",dim(Xtest),"\n")
Xtest.n_now = nrow(Xtest)

##############################################  MERGE with Xtrain_NAs5.csv / Ytrain_NAs5.csv / Xtest_NAs5.csv  ######################

## write on disk 
cat(">>> merging from disk  Xtrain_NAs5.csv / Ytrain_NAs5.csv / Xtest_NAs5.csv ... \n")
Xtrain_NAs5 = as.data.frame( fread(paste(ff.getPath("elab") , "Xtrain_NAs5.csv" , sep='') , stringsAsFactors = F))
Xtest_NAs5 = as.data.frame( fread(paste(ff.getPath("elab") , "Xtest_NAs5.csv" , sep='') , stringsAsFactors = F))
Ytrain_NAs5 = as.data.frame( fread(paste(ff.getPath("elab") , "Ytrain_NAs5.csv" , sep='') , stringsAsFactors = F))

## checks 
Xtrain_NAs5$Ytrain_NAs5 = Ytrain_NAs5
mCols = c("REN_ID","VE_NUMBER" , "REN_DATE_EFF_FROM" , "LAN_MULTIPLE_ZONING_FLAG" , "LAN_SURVEY_STRATA_IND" , "LAN_SRD_TAXABLE" , "LAN_ID_TYPE" , "LAN_POWER"
          , "LAN_WATER", "LAN_GAS", "LAN_DRAINAGE", "LAN_DATE_SUBDIVISION_MFP",  "LAN_LST_CODE",  "LAN_LDS_NUMBER_IS_RURAL", "LAN_HOUSE_NO", "LAN_HOUSE_NO_SFX"
          , "LAN_ADDRESS_SITUATION" , "LAN_LOT_NO" , "LAN_UNIT_NO", "LAN_DATE_REDUNDANT_EFF", "LAN_RESERVE_CLASS", "LAN_LOCATION", "LAN_URBAN_MAP_GRID", "LAN_ID1_SURVEY_NO"
          , "LAN_ID1_ALPHA_LOT",  "LAN_ID1_LOT_NO" , "LAN_ID1_LEASE_PART", "LAN_ID1_SECTION",  "LAN_ID1_TYPE", "LAN_ID1_TOWN_LOT", "LAN_ID1_TOWN_LOT_TYPE" , "LAN_ID2_LEASE_PART"
          , "LAN_ID2_TYPE" , "LAN_ID2_ALPHA_PREFIX", "LAN_ID2_ALPHA_SUFFIX", "LAN_ID3_TYPE", "LAN_ID3_LEASE_RESERVE_NO", "LAN_ID3_LEASE_PART", "LAN_PART_LOT_SOURCE"
          , "LAN_STR_ID",  "LLG_DATE_EFF_FROM", "LDS_NAME", "LDS_CODE", "LDS_STATUS", "STR_NAME", "STR_STY_CODE", "CORNER_STR_NAME", "CORNER_STR_STATUS"
          , "CORNER_STR_STY_CODE", "SUB_NAME" , "SUB_POSTCODE",  "URT_DATE_EFF_FROM",  "URT_URBAN_RURAL_IND")

## train 
data = merge(x = Xtrain , y = Xtrain_NAs5 , by = mCols , all = F) 
stopifnot(sum(data$Ytrain_NAs4 != data$Ytrain)==0)
data$Ytrain_NAs5 <- NULL

## test 
data_test = merge(x = Xtest , y = Xtest_NAs5 , by = mCols , all = F) 
stopifnot(nrow(data_test)==nrow(Xtest_NAs5) , nrow(data_test)==nrow(Xtest))

## finally 
Xtrain <- data 
Xtest <- data_test

rm(list = c("data","data_test"))
cat(">>> end of merge\n")
##############################################  End of MERGE 

### points_of_interest.csv  / demographics / demographics_key / distances
cat(">>> points_of_interest.csv  / demographics / demographics_key / distances  ... \n") 
head(demographics_key) 
sum(! unique(demographics_key$LAN_ID) %in% unique(land$LAN_ID) ) / length(unique(demographics_key$LAN_ID)) ## 0.754351
dinit = sum(! unique(land$LAN_ID) %in%  unique(demographics_key$LAN_ID)  ) / length(unique(land$LAN_ID)) # 0.0001178763

## focus on LAN_ID occurring in land 
demographics_key <- demographics_key[demographics_key$LAN_ID %in% unique(land$LAN_ID) , ]
stopifnot(sum(! unique(land$LAN_ID) %in%  unique(demographics_key$LAN_ID)  ) / length(unique(land$LAN_ID)) == dinit)

###### demographics 
cat(">>> processing demographics ... \n") 
#describe(demographics)
## keep: FEATURE_ID / AREA_ALBERS_SQM / GCCSA_CODE_2011 /  SA1_7 / SA1_MAINCODE_2011 
##       SA2_5DIGITCODE_2011 / SA2_MAINCODE_2011 / SA3_CODE_2011 / SA4_CODE_2011 / 
##       STATE_CODE_2011 / POACODE / RA_CODE11 / RA_NAME11 / Segment11 / SEGMENT_NAMES / GROUPS_1 / GROUPS_2

pred_keep = c("LAN_ID", "FEATURE_ID","AREA_ALBERS_SQM","GCCSA_CODE_2011","SA1_7" , "SA1_MAINCODE_2011" ,  
              "SA2_5DIGITCODE_2011", "SA2_MAINCODE_2011" , "SA3_CODE_2011" , "SA4_CODE_2011" , 
              "STATE_CODE_2011" , "POACODE" , "RA_CODE11" ,  "RA_NAME11" , "Segment11", "SEGMENT_NAMES", "GROUPS_1" , 
              "GROUPS_2")

demographics_key_noNA = demographics_key[! is.na(demographics_key$SA1_7),c("LAN_ID","SA1_7")]
data = merge(x = demographics , y = demographics_key_noNA , by="SA1_7" , all = F)

data = data[, pred_keep ]
data$SA1_7 <- NULL

## encode 
feature.names = colnames(data)
for (f in feature.names) {
  if (class(data[,f])=="character") {
    cat(">>> ",f," is character \n")
    levels <- unique(data[,f])
    data[,f] <- as.integer(factor(data[,f], levels=levels))
  }
}

cat(">>> missing values: ",sum(is.na(data)),"\n")

## double LAN_ID 
head(sort(table(data$LAN_ID),decreasing = T),20)

# 2662828 1594367   62810  212109  575538  743783  796414 1435965 2249983 2733787 3020573 3083314 3408047 5245628   55583  134663  245924  274817  287229 
#   11       5       3       3       3       3       3       3       3       3       3       3       3       3       2       2       2       2       2 

meta_data = ddply(data , .(LAN_ID) , function(x) c(num=nrow(x)) )
meta_data = meta_data[order(meta_data$num , decreasing = T),]
head(meta_data)
# LAN_ID num
# 145677 2662828  11
# 87338  1594367   5
# 3426     62810   3
# 11668   212109   3
# 31539   575538   3
# 40719   743783   3

LAN_ID.multi <- meta_data[which(meta_data$num>1),]$LAN_ID

data2 <- ddply(data[data$LAN_ID %in% LAN_ID.multi,] , .(LAN_ID) , function(x) {
  return(x[1,])
})
data <- data[! data$LAN_ID %in% LAN_ID.multi , ]
data <- rbind(data,data2)

## merge 
Xtrain = merge(x = Xtrain , y = data , by = "LAN_ID" , all.x = T , all.y = F)
Xtest = merge(x = Xtest , y = data , by = "LAN_ID" , all.x = T , all.y = F)
cat(">>> Xtrain:",dim(Xtrain),"\n")
cat(">>> Xtest:",dim(Xtest),"\n")
stopifnot(nrow(Xtrain)==Xtrain.n_now)
stopifnot(nrow(Xtest)==Xtest.n_now)

cat(">>> imputing NAs (with 0) for XGBoost ...\n")
sum(is.na(Xtrain)) 
sum(is.na(Xtest)) 

Xtrain[is.na(Xtrain)] <- 0 
Xtest[is.na(Xtest)] <- 0 

stopifnot(  sum(is.na(Xtrain)) == 0 ,  sum(is.na(Xtest)) == 0 )


##### distances 
cat(">>> processing distances ... \n") 
describe(distances)
## keep: LAN_ID / LNP_PIN / LOTNO / PITYPE_1 / OWNERSHIP / REGNO / Distance_Coast / Distance_Hospital / Distance_School_poly 
##       Distance_Reserve / Distance_WaterBody / Distance_ArterialRoad / Distance_GPO / Distance_University / Distance_Freeway / 
##       Distance_ShoppingCentre / Distance_TrainStation / Distance_RailLine / Distance_Airport 

## 
predNAs.test = ff.predNA(data=demographics_key,asIndex = F) 
cat(">>> there're ",sum(is.na(demographics_key)),"NAs in demographics_key @:",predNAs.test," --> removing  ...\n")
demographics_key_noNA <- demographics_key[!is.na(demographics_key$LNP_PIN),c("LAN_ID","LNP_PIN")]
colnames(distances)[1] <- "LNP_PIN"
data = merge(x = distances , y = demographics_key_noNA , by="LNP_PIN" , all = F)

pred_keep = c("LAN_ID", "STRADDRESS", "LOTNO" , "PITYPE_1" , "OWNERSHIP" , "REGNO" , "Distance_Coast" , "Distance_Hospital", 
              "Distance_School_poly" , "Distance_Reserve" , "Distance_WaterBody" , "Distance_ArterialRoad" , "Distance_GPO", 
              "Distance_University", "Distance_Freeway" , "Distance_ShoppingCentre" , "Distance_TrainStation" , "Distance_RailLine" , 
              "Distance_Airport")

data <- data[,pred_keep]
## STRADDRESS
data[data$STRADDRESS=="",]$STRADDRESS <- NA
levels <- unique(data$STRADDRESS)
data$STRADDRESS <- as.integer(factor(data$STRADDRESS, levels=levels))
data$STRADDRESS[is.na(data$STRADDRESS)] <- 0 

## make num 
#Distance_Coast         
data$Distance_Coast <- as.numeric(data$Distance_Coast)

#Distance_Hospital      
data$Distance_Hospital <- as.numeric(data$Distance_Hospital)

#Distance_School_poly  
data$Distance_School_poly <- as.numeric(data$Distance_School_poly)

#Distance_Reserve      
data$Distance_Reserve <- as.numeric(data$Distance_Reserve)

# Distance_WaterBody    
data$Distance_WaterBody <- as.numeric(data$Distance_WaterBody)

# Distance_ArterialRoad  
data$Distance_ArterialRoad <- as.numeric(data$Distance_ArterialRoad)

# Distance_GPO         
data$Distance_GPO <- as.numeric(data$Distance_GPO)

# Distance_University    
data$Distance_University <- as.numeric(data$Distance_University)

# Distance_Freeway      
data$Distance_Freeway <- as.numeric(data$Distance_Freeway)

# Distance_ShoppingCentre
data$Distance_ShoppingCentre <- as.numeric(data$Distance_ShoppingCentre)

# Distance_TrainStation  
data$Distance_TrainStation <- as.numeric(data$Distance_TrainStation)

# Distance_RailLine      
data$Distance_RailLine <- as.numeric(data$Distance_RailLine)

#Distance_Airport       
data$Distance_Airport <- as.numeric(data$Distance_Airport)


## encode 
feature.names = colnames(data)
for (f in feature.names) {
  if (class(data[,f])=="character") {
    cat(">>> ",f," is character \n")
    levels <- unique(data[,f])
    data[,f] <- as.integer(factor(data[,f], levels=levels))
  }
}

cat(">>> missing values: ",sum(is.na(data)),"\n")

## double LAN_ID 
head(sort(table(data$LAN_ID),decreasing = T),20)

# 3032465 2662828   96252 1675536 3417605 4245136 4711400 4856236  538386 2313569 3459350 1594367 1972942  305583  799961  975235  988546 1040008 1154654 
#   34      11       8       8       8       8       8       8       6       6       6       5       5       4       4       4       4       4       4 

meta_data = ddply(data , .(LAN_ID) , function(x) c(num=nrow(x)) )
meta_data = meta_data[order(meta_data$num , decreasing = T),]
head(meta_data)

LAN_ID.multi <- meta_data[which(meta_data$num>1),]$LAN_ID

data2 <- ddply(data[data$LAN_ID %in% LAN_ID.multi,] , .(LAN_ID) , function(x) {
  return(x[1,])
})
data <- data[! data$LAN_ID %in% LAN_ID.multi , ]
data <- rbind(data,data2)

## merge 
Xtrain = merge(x = Xtrain , y = data , by = "LAN_ID" , all.x = T , all.y = F)
Xtest = merge(x = Xtest , y = data , by = "LAN_ID" , all.x = T , all.y = F)
cat(">>> Xtrain:",dim(Xtrain),"\n")
cat(">>> Xtest:",dim(Xtest),"\n")
stopifnot(nrow(Xtrain)==Xtrain.n_now)
stopifnot(nrow(Xtest)==Xtest.n_now)

cat(">>> imputing NAs (with 0) for XGBoost ...\n")
sum(is.na(Xtrain)) 
sum(is.na(Xtest)) 

Xtrain[is.na(Xtrain)] <- -1
Xtest[is.na(Xtest)] <- -1 

stopifnot(  sum(is.na(Xtrain)) == 0 ,  sum(is.na(Xtest)) == 0 )

########### FINAL 
## MEMO #1: remove REN_ID in train / test set before fitting models 
## MEMO #2: in final dataset remove LAN_ID 

Ytrain = Xtrain$Ytrain

predToDel = c("LAN_ID","Ytrain")
for (pp in predToDel) {
  cat(">>> removing ",pp,"...\n")
  Xtrain[,pp] <- NULL
  Xtest[,pp] <- NULL
}

#########
l = ff.featureFilter (Xtrain,
                      Xtest,
                      removeOnlyZeroVariacePredictors=TRUE,
                      performVarianceAnalysisOnTrainSetOnly = TRUE , 
                      removePredictorsMakingIllConditionedSquareMatrix = FALSE, 
                      removeHighCorrelatedPredictors = FALSE, 
                      featureScaling = FALSE)
Xtrain = l$traindata
Xtest = l$testdata  

########

## write on disk 
cat(">>> writing on disk ... \n")
write.csv(Xtrain,
          quote=FALSE, 
          file=paste0(ff.getPath("elab"),"Xtrain_NAs6.csv"),
          row.names=FALSE)
write.csv(data.frame(Ytrain=Ytrain),
          quote=FALSE, 
          file=paste0(ff.getPath("elab"),"Ytrain_NAs6.csv"),
          row.names=FALSE)
write.csv(Xtest,
          quote=FALSE, 
          file=paste0(ff.getPath("elab"),"Xtest_NAs6.csv"),
          row.names=FALSE)


