-- Based on Postgres
-- change dir to where the files are
\cd /Users/paulperry/Documents/kaggle/western-australia-rental-prices/data
-- presumes that a database 'australia' is created'
\c australia;
set datestyle to 'DMY';
set client_encoding to latin1;
create extension tablefunc;

-- drop and (re)create all tables

drop table valuation_entities_details ;
CREATE TABLE valuation_entities_details
(
URV_DATE_EFF_FROM date NULL,       
URV_DESCRIPTION varchar(25) NULL, 
URV_ID bigint NULL,                
URV_VEN_QUALITY_IND varchar(1) NULL, 
URV_VEN_QUANTITY_IND varchar(1) NULL, 
UVV_DATE_EFF_FROM date NULL,       
UVV_DATE_EFF_TO date NULL,         
UVV_QUALITY varchar(4) NULL,      
UVV_QUANTITY double precision NULL,
VE_NUMBER bigint
);                                     

drop table valuation_entities_classifications ;
CREATE TABLE valuation_entities_classifications
(                                              
VE_NUMBER bigint,
VEC_CLS_CODE bigint NULL,                  
VEC_DATE_EFF_FROM date NULL,               
VEC_DATE_EFF_TO date NULL,                 
CLS_DESCRIPTION varchar(50) NULL,         
CLS_CURRENT_USE_IND varchar(1) NULL,      
CLS_VACANT_LAND_IND varchar(1) NULL,      
CLS_MULTI_RES_IND varchar(1) NULL,        
CLS_VE_USE varchar(1) NULL,               
CLS_RESTRICT_TYPE varchar(1) NULL,        
CLS_CODE_PLURAL double precision NULL      
);

drop table valuation_entities;
CREATE TABLE valuation_entities         
(                                       
VE_GOVT_CALC_METHOD varchar(1) NULL,      
VE_CRIT_INFRA_IND varchar(1) NULL,        
VE_DATE_CREATED timestamp NULL,          
VE_DATE_MODIFIED timestamp NULL,         
VE_DESCRIPTION varchar(100),           
VE_SUB_NUMBER double precision NULL,
VE_NUMBER bigint,
VE_UNIT_NO varchar(9) NULL,               
VE_USE varchar(1) NULL                    
);

drop table points_of_interest ;
CREATE TABLE points_of_interest     
(                                   
X double precision NULL,        
Y double precision NULL,        
poifeatureclass text NULL,      
classificationcode bigint NULL, 
fcsubtype text NULL,            
facilitytype text NULL,         
nameid bigint NULL,             
geographicfeaturename text NULL,
featuretext text NULL,          
addresstext text NULL           
);                                  

drop table land_zonings ;
CREATE TABLE land_zonings                   
(
LGZ_DUAL_ZONING_REASON varchar(2) NULL,
LNZ_DATE_EFF_FROM date NULL,            
LNZ_DATE_EFF_TO date NULL,
LAN_ID bigint ,
LNZ_LGZ_ZON_CODE varchar(10) NULL,     
LGZ_DATE_EFF_FROM date NULL,            
LGZ_DATE_EFF_TO varchar NULL,              
LGZ_DESCRIPTION varchar(25) NULL,      
LGZ_MIN_UNIT_AREA double precision NULL,          
LGA_NAME varchar(25) NULL              
);

drop table land_valuation_key ;
CREATE TABLE land_valuation_key
(                              
LAN_ID bigint ,
VE_NUMBER bigint,
PRIMARY KEY (LAN_ID, VE_NUMBER)
);                             

drop table land_urban ;
CREATE TABLE land_urban                
(
ULV_DATE_EFF_FROM date NULL,       
ULV_DATE_EFF_TO date NULL,
LAN_ID bigint ,
ULV_QUALITY varchar(4) NULL,      
ULV_QUANTITY double precision NULL,
URV_DESCRIPTION varchar(25) NULL, 
URV_ID bigint NULL,                
URV_QUALIFIER varchar(6) NULL,    
URV_URN_NAME varchar(6) NULL,     
URV_VEN_QUANTITY_IND varchar(1) NULL     
);                                     

drop table land_restrictions ;
CREATE TABLE land_restrictions
(                             
LAN_ID bigint,
LRS_DATE_START date NULL, 
LRS_DATE_END date NULL,   
LRS_RST_CODE varchar(6) NULL,   
LRS_COMMENT varchar(2000) NULL,    
RST_DESCRIPTION varchar(25) NULL 
);

drop table land_pins ;
CREATE TABLE land_pins                          
(                                               
LAN_ID bigint,         
LNP_POL_PIN bigint NULL,          
LNP_CENTROID_EASTING bigint NULL, 
LNP_CENTROID_NORTHING bigint NULL,
LNP_CENTROID_YLAT double precision NULL,    
LNP_CENTROID_ZONE bigint NULL,    
LNP_CENTROID_XLONG double precision NULL,   
LNP_PIN bigint NULL,              
LNP_Z50_EASTING double precision NULL,      
LNP_Z50_NORTHING double precision NULL,     
LNP_TEXT_EASTING double precision NULL,     
LNP_TEXT_NORTHING double precision NULL,    
LNP_TEXT_XLONG double precision NULL,       
LNP_TEXT_YLAT double precision NULL         
);                                              

drop table land_admin_areas ;
CREATE TABLE land_admin_areas      
(                                  
LAN_ID bigint ,
LAA_ADA_LGA_NUMBER bigint NULL,
LAA_ADA_CODE bigint NULL,      
LAA_DATE_EFF_FROM date NULL,   
LAA_DATE_EFF_TO date NULL,     
LGA_NAME varchar NULL         
);                                 

drop table land;
CREATE TABLE land
(
LAN_ID bigint PRIMARY KEY,
LAN_MULTIPLE_ZONING_FLAG varchar(1) NULL,           
LAN_SURVEY_STRATA_IND varchar(1) NULL,              
LAN_SRD_TAXABLE varchar(1) NULL,                    
LAN_ID_TYPE varchar(1) NULL,                      
LAN_POWER varchar(1) NULL,                          
LAN_WATER varchar(1) NULL,                          
LAN_GAS varchar(1) NULL,                            
LAN_DRAINAGE varchar(1) NULL,                       
LAN_DATE_SUBDIVISION_MFP date NULL,           
LAN_LST_CODE varchar(5) NULL,                       
LAN_LDS_NUBMER double precision NULL,         
LAN_LDS_NUMBER_ID_TYPE3 double precision NULL,
LAN_LDS_NUMBER_IS_RURAL double precision NULL,
LAN_HOUSE_NO varchar(9) NULL,                       
LAN_HOUSE_NO_SFX varchar(1) NULL,                   
LAN_ADDRESS_SITUATION varchar(50) NULL,              
LAN_LOT_NO varchar(9) NULL,                         
LAN_UNIT_NO varchar(9) NULL,                        
LAN_DATE_REDUNDANT_EFF varchar NULL,             
LAN_DATE_SUBDIVISION_LGA date NULL,           
LAN_DATE_SUBDIVISION_WAPC date NULL,          
LAN_RESERVE_CLASS varchar(1) NULL,                  
LAN_SKETCH_ID varchar(4) NULL,          
LAN_LOCATION varchar(50) NULL,                       
LAN_URBAN_MAP_GRID varchar(10) NULL,                 
LAN_ID1_SURVEY_NO varchar(6) NULL,                  
LAN_ID1_ALPHA_LOT varchar(2) NULL,                  
LAN_ID1_LOT_NO double precision NULL,         
LAN_ID1_PART_LOT double precision NULL,       
LAN_ID1_LEASE_PART varchar(4) NULL,                 
LAN_ID1_SECTION varchar(2) NULL,                    
LAN_ID1_TYPE varchar(1) NULL,                       
LAN_ID1_TOWN_LOT varchar(6) NULL,                   
LAN_ID1_TOWN_LOT_TYPE varchar(2) NULL,              
LAN_ID2_LOT varchar(5) NULL,            
LAN_ID2_PART_LOT bigint NULL,       
LAN_ID2_LEASE_PART varchar(4) NULL,                 
LAN_ID2_TYPE varchar(1) NULL,                       
LAN_ID2_ALPHA_PREFIX varchar(2) NULL,               
LAN_ID2_ALPHA_SUFFIX varchar(1) NULL,               
LAN_ID3_TYPE varchar(1) NULL,                       
LAN_ID3_LEASE_RESERVE_NO varchar(7) NULL,           
LAN_ID3_PART_LOT bigint NULL,       
LAN_ID3_LEASE_PART varchar(4) NULL,                 
LAN_DATE_SURVEY_STRATA date NULL,             
LAN_PART_LOT_SOURCE varchar(1) NULL,                
LAN_DATE_LEASE_EXPIRY date NULL,              
LAN_DATE_LEASE_FROM date NULL,                
LAN_STR_ID varchar NULL,                       
LAN_STR_ID_HAS_CORNER varchar NULL,  
LLG_DATE_EFF_FROM date NULL,                  
LDS_NAME varchar(50) NULL,                           
LDS_CODE varchar(5) NULL,                           
LDS_STATUS varchar(1) NULL,                         
STR_NAME varchar(40) NULL,                           
STR_STY_CODE varchar(40) NULL,                       
CORNER_STR_NAME varchar(40) NULL,                    
CORNER_STR_STATUS varchar(1) NULL,                  
CORNER_STR_STY_CODE varchar(4) NULL,                
SUB_NAME varchar(40) NULL,                           
SUB_POSTCODE double precision NULL,           
URT_DATE_EFF_FROM date NULL,                  
URT_URBAN_RURAL_IND varchar(1) NULL                 
);                                                

drop table demographics_key ;
CREATE TABLE demographics_key     
(                                 
LAN_ID bigint ,
LNP_PIN bigint NULL,
SA1_7 bigint NULL
);                                

drop table demographics;
CREATE TABLE demographics                 
(                                         
FEATURE_ID bigint NULL,               
AREA_ALBERS_SQM double precision NULL,
GCCSA_CODE_2011 text NULL,            
GCCSA_NAME_2011 text NULL,            
SA1_7 bigint PRIMARY KEY,                    
SA1_MAINCODE_2011 bigint NULL,        
SA2_5DIGITCODE_2011 bigint NULL,      
SA2_MAINCODE_2011 bigint NULL,        
SA2_NAME_2011 text NULL,              
SA3_CODE_2011 bigint NULL,            
SA3_NAME_2011 text NULL,              
SA4_CODE_2011 bigint NULL,            
SA4_NAME_2011 text NULL,              
STATE_CODE_2011 bigint NULL,          
STATE_NAME_2011 text NULL,            
Min_X bigint NULL,                    
Min_Y bigint NULL,                    
Max_X bigint NULL,                    
Max_Y bigint NULL,                    
POACODE bigint NULL,                  
RA_CODE11 bigint NULL,                
RA_NAME11 text NULL,                  
Segment11 bigint NULL,                
Segment11_Desc text NULL,             
Segment11_Desc2 text NULL,            
Segment11_Map text NULL,              
CODE bigint NULL,                     
SEGMENT_NAMES text NULL,              
MOVIE_TITLES text NULL,               
GROUPS text NULL,                     
GROUPS_1 text NULL,                   
GROUPS_2 text NULL,                   
Predominant_Lifestage text NULL,      
Financial_Status text NULL,           
Worklife text NULL,                   
Area_Wealth_Dynamic text NULL,        
Stability_Indicator text NULL,        
FeatureCodeGroup bigint NULL,         
Feature_code bigint NULL              
);

drop table train;
CREATE TABLE train
(
REN_ID bigint PRIMARY KEY,
REN_DATE_EFF_FROM date,
REN_BASE_RENT double precision,
VE_NUMBER bigint ,
REN_LEASE_LENGTH varchar(30) NULL
);

drop table test;
CREATE TABLE test
(
REN_ID bigint PRIMARY KEY,
REN_DATE_EFF_FROM date,
VE_NUMBER bigint,
REN_LEASE_LENGTH varchar(20) NULL
);

drop table sample_submission;
CREATE TABLE sample_submission
(
REN_ID bigint PRIMARY KEY,
REN_BASE_RENT double precision
);

drop table distances;
CREATE TABLE distances
(
PIN bigint,
STRADDRESS text,
LOTNO int NULL,
PITYPE_1 text NULL,
PITYPE_2 text NULL, 
PITYPE_3_1 text NULL, 
PITYPE_3_2 text NULL,
OWNERSHIP text,
REGNO text,
Distance_Coast int,
Distance_Hospital int,
Name_Hospital text,
Distance_School_poly int, 
Name_School_poly text, 
Distance_Reserve int, 
Name_Reserve text, 
Distance_WaterBody int,
Name_WaterBody text, 
Distance_ArterialRoad int, 
Name_Road text, 
Distance_GPO int, 
Distance_GolfCourse int,
Name_GolfCourse text,
Distance_University int, 
Name_University text, 
Distance_Freeway int, 
Name_Freeway text, 
Distance_ShoppingCentre int, 
Name_ShoppingCentre text, 
Distance_TrainStation int,
Name_TrainStation text, 
Distance_RailLine int,
Name_RailLine text, 
Distance_Airport int, 
Name_Airport text
);


-- create all index'es

CREATE INDEX val_ent_details_ve_num ON valuation_entities_details (VE_NUMBER);
CREATE INDEX val_ent_details_urv_id ON valuation_entities_details (URV_ID);
CREATE INDEX val_ent_class_ve_num ON valuation_entities_classifications (VE_NUMBER);
CREATE INDEX val_ent_ve_number ON valuation_entities (VE_NUMBER);
CREATE INDEX land_zonings_lan_id ON land_zonings (LAN_ID);
CREATE INDEX land_urban_lan_id ON land_urban (LAN_ID);
CREATE INDEX land_res_lan_id on land_restrictions (LAN_ID);
CREATE INDEX land_pins_lan_id on land_pins (LAN_ID);
CREATE INDEX land_admin_areas_lan_id on land_admin_areas (LAN_ID);
CREATE INDEX train_ve_num on train (VE_NUMBER);
CREATE INDEX test_ve_num on test (VE_NUMBER);
CREATE INDEX test_ren_id on test (REN_ID);
CREATE INDEX submission_ren_id on sample_submission (REN_ID);
CREATE UNIQUE INDEX land_val_key ON land_valuation_key (LAN_ID, VE_NUMBER);
CREATE UNIQUE INDEX land_lan_id on land (LAN_ID);
drop index dem_key;
CREATE UNIQUE INDEX dem_key on demographics_key (LAN_ID,  LNP_PIN);
CREATE UNIQUE INDEX dem_idx on demographics (SA1_7);
create index latlonidx on land_pins using gist(ll_to_earth(lnp_centroid_ylat, lnp_centroid_xlong));

-- import all CSV's

\copy demographics from 'demographics.csv'  null as 'NA' csv header
\copy demographics_key from 'demographics_key.csv'  null as 'NA' csv header
\copy land from 'land.csv'  null as 'NA' csv header
\copy land_admin_areas from 'land_admin_areas.csv'  null as 'NA' csv header
\copy land_pins from 'land_pins.csv'  null as 'NA' csv header
\copy land_restrictions from 'land_restrictions.csv'  null as 'NA' csv header
# sed s/,\"\",/,,/ land_urban.csv > land_urban_null.csv
\copy land_urban from 'land_urban.csv'  null as 'NA' csv header
\copy land_valuation_key from 'land_valuation_key.csv'  null as 'NA' csv header
\copy land_zonings from 'land_zonings.csv'  null as 'NA' csv header
\copy points_of_interest from 'points_of_interest.csv'  null as 'NA' csv header
# sed 
\copy valuation_entities from 'valuation_entities_null.csv'  null as 'NA' csv header
\copy valuation_entities_classifications from 'valuation_entities_classifications.csv'  null as 'NA' csv header
\copy valuation_entities_details from 'valuation_entities_details.csv'  null as 'NA' csv header 
\copy train from 'train.csv'  null as 'NA' csv header
\copy test from 'test.csv'  null as 'NA' csv header
\copy sample_submission from 'sample_submission.csv' null as 'NA' csv header
# sed s/,\"\",/,,/ distances.csv > distances_null.csv
\copy distances from 'distances_null.csv' null as '' csv header


-- alter train and test to add the lat and lon to the table

alter table train add column lat double precision null;
alter table train add column lon double precision null;
alter table test add column lat double precision null;
alter table test add column lon double precision null;

update train t1
set lat=lnp_centroid_ylat, lon=lnp_centroid_xlong
from land_pins t3, land_valuation_key t2
where t1.ve_number = t2.ve_number and t2.lan_id = t3.lan_id;

create index trainlatlonidx on train using gist(ll_to_earth(lnp_centroid_ylat, lnp_centroid_xlong));


-- need a function for median.  May need to change they function signature
-- to be double precision to match the type in the DB

CREATE OR REPLACE FUNCTION _final_median(NUMERIC[])
   RETURNS NUMERIC AS
$$
   SELECT AVG(val)
   FROM (
     SELECT val
     FROM unnest($1) val
     ORDER BY 1
     LIMIT  2 - MOD(array_upper($1, 1), 2)
     OFFSET CEIL(array_upper($1, 1) / 2.0) - 1
   ) sub;
$$
LANGUAGE 'sql' IMMUTABLE;
 
CREATE AGGREGATE median(NUMERIC) (
  SFUNC=array_append,
  STYPE=NUMERIC[],
  FINALFUNC=_final_median,
  INITCOND='{}'
);

-- some sample queries I tried out.  I forget what this did.

/*
select 
ren_id  ,
ren_date_eff_from ,
ren_base_rent ,
train.ve_number ,
ren_lease_length ,
ve_govt_calc_method ,
ve_crit_infra_ind ,
ve_description  ,
ve_sub_number ,
ve_unit_no ,
ve_use
from train, valuation_entities
where train.VE_NUMBER = valuation_entities.VE_NUMBER
and ve_date_created = (select max(ve_date_created) from valuation_entities where ve_number = ve_number)
limit 10;

select *
from train, valuation_entities
where train.VE_NUMBER = valuation_entities.VE_NUMBER
limit 10;

select *
from train, land_valuation_key, land
where train.VE_NUMBER = land_valuation_key.VE_NUMBER
and land_valuation_key.LAN_ID = land.LAN_ID
limit 10;


select ve_number , urv_id , uvv_quantity , max(urv_date_eff_from)
from valuation_entities_details 
where urv_ven_quantity_ind like 'Y'
group by ve_number, urv_id, uvv_quantity;

select * from train, test, land_valuation_key, demographics_key, demographics
where (train.ve_number = land_valuation_key.ve_number or
      test.ve_number = land_valuation_key.ve_number) and
      land_valuation_key.lan_id = demographics_key.lan_id and
      demographics_key.sa1_7 = demographics.sa1_7
      limit 10;

select \
ren_id, ve_number, lan_id, lnp_pin, sa1_7, \
feature_id, area_albers_sqm, gccsa_code_2011, \
sa1_maincode_2011, sa2_5digitcode_2011, sa2_maincode_2011, \
sa2_name_2011, sa3_code_2011, sa3_name_2011, sa4_code_2011, \
sa4_name_2011, state_code_2011, state_name_2011, \
poacode, ra_code11, ra_name11,  \
segment11, segment11_desc, segment11_desc2, segment11_map, \
code, segment_names, movie_titles, \
groups, groups_1, groups_2, \
predominant_lifestage, financial_status, worklife, area_wealth_dynamic, \
stability_indicator, featurecodegroup, feature_code  \
from train, test, land_valuation_key, demographics_key, demographics \
where train.ve_number = land_valuation_key.ve_number or \
      test.ve_number = land_valuation_key.ve_number) and \
      land_valuation_key.lan_id = demographics_key.lan_id and \
      demographics_key.sa1_7 = demographics.sa1_7;


select \
train.ren_id, train.ve_number, demographics_key.lan_id, lnp_pin, \
demographics_key.sa1_7, \
area_albers_sqm, gccsa_code_2011, sa2_5digitcode_2011, \
sa3_code_2011, sa4_code_2011, state_code_2011,  \
poacode, ra_code11, code, movie_titles, \
groups, groups_1, groups_2, \
predominant_lifestage, financial_status, worklife, area_wealth_dynamic, \
stability_indicator, featurecodegroup, feature_code  \
from train \
inner join land_valuation_key on land_valuation_key.ve_number = train.ve_number \
inner join demographics_key on demographics_key.lan_id = land_valuation_key.lan_id \
inner join  demographics on demographics.sa1_7 =  demographics_key.sa1_7 ;
      

select count(distinct lan_multiple_zoning_flag ) from land;
select count(distinct lan_survey_strata_ind    ) from land;
select count(distinct lan_srd_taxable          ) from land;
select count(distinct lan_id_type              ) from land;
select count(distinct lan_power                ) from land;
select count(distinct lan_water                ) from land;
select count(distinct lan_gas                  ) from land;
select count(distinct lan_drainage             ) from land;
select count(distinct lan_date_subdivision_mfp ) from land;
select count(distinct lan_lst_code             ) from land;
select count(distinct lan_lds_nubmer           ) from land;
select count(distinct lan_lds_number_id_type3  ) from land;
select count(distinct lan_lds_number_is_rural  ) from land;
select count(distinct lan_house_no             ) from land;
select count(distinct lan_house_no_sfx         ) from land;
select count(distinct lan_address_situation    ) from land;
select count(distinct lan_lot_no               ) from land;
select count(distinct lan_unit_no              ) from land;
select count(distinct lan_date_redundant_eff   ) from land;
select count(distinct lan_date_subdivision_lga ) from land;
select count(distinct lan_date_subdivision_wapc) from land;
select count(distinct lan_reserve_class        ) from land;
select count(distinct lan_sketch_id            ) from land;
select count(distinct lan_location             ) from land;
select count(distinct lan_urban_map_grid       ) from land;
select count(distinct lan_id1_survey_no        ) from land;
select count(distinct lan_id1_alpha_lot        ) from land;
select count(distinct lan_id1_lot_no           ) from land;
select count(distinct lan_id1_part_lot         ) from land;
select count(distinct lan_id1_lease_part       ) from land;
select count(distinct lan_id1_section          ) from land;
select count(distinct lan_id1_type             ) from land;
select count(distinct lan_id1_town_lot         ) from land;
select count(distinct lan_id1_town_lot_type    ) from land;
select count(distinct lan_id2_lot              ) from land;
select count(distinct lan_id2_part_lot         ) from land;
select count(distinct lan_id2_lease_part       ) from land;
select count(distinct lan_id2_type             ) from land;
select count(distinct lan_id2_alpha_prefix     ) from land;
select count(distinct lan_id2_alpha_suffix     ) from land;
select count(distinct lan_id3_type             ) from land;
select count(distinct lan_id3_lease_reserve_no ) from land;
select count(distinct lan_id3_part_lot         ) from land;
select count(distinct lan_id3_lease_part       ) from land;
select count(distinct lan_date_survey_strata   ) from land;
select count(distinct lan_part_lot_source      ) from land;
select count(distinct lan_date_lease_expiry    ) from land;
select count(distinct lan_date_lease_from      ) from land;
select count(distinct lan_str_id               ) from land;
select count(distinct lan_str_id_has_corner    ) from land;
select count(distinct llg_date_eff_from        ) from land;
select count(distinct lds_name                 ) from land;
select count(distinct lds_code                 ) from land;
select count(distinct lds_status               ) from land;
select count(distinct str_name                 ) from land;
select count(distinct str_sty_code             ) from land;
select count(distinct corner_str_name          ) from land;
select count(distinct corner_str_status        ) from land;
select count(distinct corner_str_sty_code      ) from land;
select count(distinct sub_name                 ) from land;
select count(distinct sub_postcode             ) from land;
select count(distinct urt_date_eff_from        ) from land;
select count(distinct urt_urban_rural_ind    ) from land;

*/

/* not sure why I had this here

'lan_multiple_zoning_flag',
'lan_survey_strata_ind',
'lan_srd_taxable',
'lan_id_type',
'lan_power',
'lan_water',
'lan_gas',
'lan_drainage',
'lan_date_subdivision_mfp',
'lan_lst_code',
'lan_lds_nubmer',
'lan_lds_number_id_type3',
'lan_lds_number_is_rural',
'lan_house_no',
'lan_house_no_sfx',
'lan_address_situation',
'lan_lot_no',
'lan_unit_no',
'lan_date_redundant_eff',
'lan_date_subdivision_lga',
'lan_date_subdivision_wapc',
'lan_reserve_class',
'lan_sketch_id',
'lan_location',
'lan_urban_map_grid',
'lan_id1_survey_no',
'lan_id1_alpha_lot',
'lan_id1_lot_no',
'lan_id1_part_lot',
'lan_id1_lease_part',
'lan_id1_section',
'lan_id1_type',
'lan_id1_town_lot',
'lan_id1_town_lot_type',
'lan_id2_lot',
'lan_id2_part_lot',
'lan_id2_lease_part',
'lan_id2_type',
'lan_id2_alpha_prefix',
'lan_id2_alpha_suffix',
'lan_id3_type',
'lan_id3_lease_reserve_no',
'lan_id3_part_lot',
'lan_id3_lease_part',
'lan_date_survey_strata',
'lan_part_lot_source',
'lan_date_lease_expiry',
'lan_date_lease_from',
'lan_str_id',
'lan_str_id_has_corner',
'llg_date_eff_from',
'lds_name',
'lds_code',
'lds_status',
'str_name',
'str_sty_code',
'corner_str_name',
'corner_str_status',
'corner_str_sty_code',
'sub_name',
'sub_postcode',
'urt_date_eff_from',
'urt_urban_rural_ind'

*/
