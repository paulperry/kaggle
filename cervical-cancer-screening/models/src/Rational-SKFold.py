from __future__ import print_function
import os
import pandas as pd
import xgboost as xgb
import time

import shutil
from sklearn import preprocessing
from sklearn.cross_validation import train_test_split
import numpy as np
from sklearn.utils import shuffle
from sklearn import metrics,cross_validation
import sys

def archive_results(filename,results,algo,script):
    """
    :type algo: basestring
    :type script: basestring
    :type results: DataFrame
    """
    #assert results == pd.DataFrame
    now=time.localtime()[0:5]
    dirname='../archive'
    subdirfmt='%4d-%02d-%02d-%02d-%02d'
    subdir=subdirfmt %now
    if not os.path.exists(os.path.join(dirname,str(algo))):
        os.mkdir(os.path.join(dirname,str(algo)))
    dir_to_create=os.path.join(dirname,str(algo),subdir)
    if not os.path.exists(dir_to_create):
        os.mkdir(dir_to_create)
    os.chdir(dir_to_create)

    results.to_csv(filename,index=False,float_format='%.6f')
    shutil.copy2(script,'.')

    return

###############################################################################################
#
train_file = '../features/train_big_table.csv.gz'
test_file = '../features/test_big_table.csv.gz'
train = pd.read_csv(train_file)
test = pd.read_csv(test_file)
print (train.shape,test.shape)
from sklearn import preprocessing
for f in train.columns:
        if train[f].dtype == 'object':
            print(f)
            lbl = preprocessing.LabelEncoder()
            lbl.fit(list(train[f].values) + list(test[f].values))
            train[f] = lbl.transform(list(train[f].values))
            test[f] = lbl.transform(list(test[f].values))
train=train.sort_index(axis=1)
test=test.sort_index(axis=1)
print (train.columns, test.columns)
train_fpsoto=pd.read_csv('../features/train_fpsoto.csv.gz')
test_fpsoto=pd.read_csv('../features/test_fpsoto.csv.gz')
train=pd.merge(train,train_fpsoto,on='patient_id',how='left')
test=pd.merge(test,test_fpsoto,on='patient_id',how='left')
print('after merging fpsoto')
print(train.shape,test.shape)
del train_fpsoto,test_fpsoto
train_obgyn=pd.read_csv('../features/train_obgyn.csv.gz')
test_obgyn=pd.read_csv('../features/test_obgyn.csv.gz')
train=pd.merge(train,train_obgyn,on='patient_id',how='left')
test=pd.merge(test,test_obgyn,on='patient_id',how='left')
print('after merging obgyn')
print(train.shape,test.shape)
del train_obgyn,test_obgyn
cancer_train=pd.read_csv('../features/train_diagnosis_cancer.csv.gz',index_col=None)

cancer_train['have_cancer']=1
cancer_train['sum_cancer']=1

idxC=cancer_train.groupby(['patient_id'])['patient_id'].mean().astype(int)
hc=cancer_train.groupby(['patient_id'])['have_cancer'].mean().astype(int)
sumhc=cancer_train.groupby(['patient_id'])['sum_cancer'].sum().astype(int)
cancer_train = pd.DataFrame({"patient_id": idxC.values, 'have_cancer': hc.values,'sum_cancer': sumhc.values })
print(cancer_train.head(5))

cancer_test=pd.read_csv('../features/test_diagnosis_cancer.csv.gz',index_col=None)
cancer_test['have_cancer']=1
cancer_test['sum_cancer']=1
print(cancer_test.info())
idxC=cancer_test.groupby(['patient_id'])['patient_id'].mean().astype(int)
hc=cancer_test.groupby(['patient_id'])['have_cancer'].mean().astype(int)
sumhc=cancer_test.groupby(['patient_id'])['sum_cancer'].sum().astype(int)
cancer_test = pd.DataFrame({"patient_id": idxC.values, 'have_cancer': hc.values,'sum_cancer': sumhc.values })

train=pd.merge(train,cancer_train, on='patient_id',how='left')
test=pd.merge(test,cancer_test, on='patient_id',how='left')
print(train.shape,test.shape)


virus_train=pd.read_csv('../features/train_diagnosis_virus.csv.gz',index_col=None)

virus_train['have_virus']=1
virus_train['sum_virus']=1

idxC=virus_train.groupby(['patient_id'])['patient_id'].mean().astype(int)
hc=virus_train.groupby(['patient_id'])['have_virus'].mean().astype(int)
sumhc=virus_train.groupby(['patient_id'])['sum_virus'].sum().astype(int)
virus_train = pd.DataFrame({"patient_id": idxC.values, 'have_virus': hc.values,'sum_virus': sumhc.values })
print(virus_train.head(5))

virus_test=pd.read_csv('../features/test_diagnosis_virus.csv.gz',index_col=None)
virus_test['have_virus']=1
virus_test['sum_virus']=1
print(virus_test.info())
idxC=virus_test.groupby(['patient_id'])['patient_id'].mean().astype(int)
hc=virus_test.groupby(['patient_id'])['have_virus'].mean().astype(int)
sumhc=virus_test.groupby(['patient_id'])['sum_virus'].sum().astype(int)
virus_test = pd.DataFrame({"patient_id": idxC.values, 'have_virus': hc.values,'sum_virus': sumhc.values })

train=pd.merge(train,virus_train, on='patient_id',how='left')
test=pd.merge(test,virus_test, on='patient_id',how='left')
print(train.shape,test.shape)
del cancer_train,cancer_test,virus_train,virus_test
procedure_counts=pd.read_csv('../features/procedure/procedure_counts_selected.csv.gz')

train=pd.merge(train,procedure_counts,on='patient_id',how='left')
test=pd.merge(test,procedure_counts,on='patient_id',how='left')
print('after merging ZZ procedure ')
print(train.shape,test.shape)
del procedure_counts
procedure_years=pd.read_csv('../features/procedure/procedure_years.csv.gz')
train=pd.merge(train,procedure_years,on='patient_id',how='left')
test=pd.merge(test,procedure_years,on='patient_id',how='left')
print('after merging ZZ procedure ')
print(train.shape,test.shape)
del procedure_years
activity_stats=pd.read_csv('../features/activity/activity_stats.csv.gz')
train=pd.merge(train,activity_stats,on='patient_id',how='left')
test=pd.merge(test,activity_stats,on='patient_id',how='left')
print('after merging ZZ activity ')
print(train.shape,test.shape)
del activity_stats
import shutil

from sklearn.utils import shuffle
def preprocess_data(train,test):

    y=train['is_screener']
    id_test=test['patient_id']
    id_train=train['patient_id']
    train=train.drop(['patient_id','is_screener' ],axis=1)
    test=test.drop(['patient_id' ],axis=1)
    train=train.fillna(0)
    test=test.fillna(0)
    return id_test,id_train,test,train,y
print(train.shape,test.shape)
id_test,id_train,test,train,y=preprocess_data(train,test)
print(train.shape,test.shape)
feature_names=train.columns

X=np.asarray(train)
y=np.asarray(y)
X_test=np.asarray(test)
DTest=xgb.DMatrix(data=X_test)
params = {"objective": "binary:logistic",
          "eta": 0.07,
          #"gamma":0.5,
          "max_depth": 14,
          #"max_delta_step":1,
          "min_child_weight":5,
          "silent":1,
          "subsample": 0.94,
          "colsample_bytree": 0.56,
          "colsample_bylevel":0.9,
          "seed": 95,
          "booster": "gbtree",
          "nthread":6,
          "eval_metric":'auc'
          }

skf = cross_validation.StratifiedKFold(y, n_folds=3)
p=0
total=0
auc_tot=0
train_plus=pd.DataFrame([])
y_plus=pd.DataFrame([])
for train_index, test_index in skf:
  total+=1
# print("TRAIN:", train_index, "TEST:", test_index)
  X_train, X_val = X[train_index], X[test_index]
  y_train, y_val = y[train_index], y[test_index]

  dtest=xgb.DMatrix(data=X_val,label=y_val)
  dtrain=xgb.DMatrix(data=X_train,label=y_train)
  watchlist = [(dtest,'eval'), (dtrain,'train')]
  print ('start running example to start from a initial prediction')
  # train xgboost for 10 round
  cls = xgb.train( params, dtrain, 20, watchlist )
  # Note: we need the margin value instead of transformed prediction in set_base_margin
  # do predict with output_margin=True, will always give you margin values before logistic transformation
  ptrain = cls.predict(dtrain, output_margin=True)
  ptest = cls.predict(dtest, output_margin=True)
  dtrain.set_base_margin(ptrain)
  dtest.set_base_margin(ptest)
  print ('this is result of running from initial prediction')
  cls = xgb.train( params, dtrain, 500, watchlist,early_stopping_rounds=50,  verbose_eval=True)

  ###################################################################################

  y_pred=cls.predict(dtest)
  preds_tr=pd.DataFrame({'preds':y_pred})
  auc=metrics.roc_auc_score(y_val, y_pred)
  print ('AUC =%s' %auc)
  auc_tot+=auc
  p +=cls.predict(DTest)
  train_tmp=pd.DataFrame(X_val, columns=feature_names)
  train_tmp=pd.concat([train_tmp,preds_tr],axis=1)
  y_tmp=pd.DataFrame({'target':y_val})
  y_plus=y_plus.append(y_tmp, ignore_index=True)
  train_plus=train_plus.append(train_tmp, ignore_index=True)
p /=(float(total))
auc_tot/=(float(total))
print ('AUC averaged =%s' %auc_tot)
print (train_plus.shape,y_plus.shape)
#
#
preds=pd.DataFrame({'preds':p})
test=pd.DataFrame(X_test, columns=feature_names)
test=pd.concat([test,preds],axis=1)

X=np.asarray(train_plus)
y=np.asarray(y_plus).ravel()
X_test=np.asarray(test)
###########save on disk to be used later
train_plus['patient_id']=id_train
test['patient_id']=id_test

train_plus.to_csv('../input/metatrain.csv',index=False)
test.to_csv('../input/metatest.csv',index=False)

del train,test,train_tmp,y_tmp,train_plus,y_pred

print ('starting second level')
X_train,X_val,y_train,y_val=train_test_split(X,y,test_size=0.1,random_state=77)
dtest=xgb.DMatrix(data=X_val,label=y_val)
dtrain=xgb.DMatrix(data=X_train,label=y_train)
DTest=xgb.DMatrix(data=X_test)
watchlist = [(dtest,'eval'), (dtrain,'train')]
p=0
total=1
for i in range(1,total+1):
 seed_xgb=i+93

 print(i) ,
 print ('start running example to start from a initial prediction')
 # specify parameters via map, definition are same as c++ version

 params = {"objective": "binary:logistic",
          "eta": 0.07,
          #"gamma":0.5,
          "max_depth": 14,
          #"max_delta_step":1,
          "min_child_weight":5,
          "silent":1,
          "subsample": 0.94,
          "colsample_bytree": 0.56,
          "colsample_bylevel":0.9,
          "seed": seed_xgb,
          "booster": "gbtree",
          "nthread":6,
          "eval_metric":'auc'
          }
 print ('this is result of running from initial prediction')
 cls = xgb.train( params, dtrain, 4000, watchlist,early_stopping_rounds=50,  verbose_eval=True)

 ###################################################################################

 y_pred=cls.predict(dtest)
 auc=metrics.roc_auc_score(y_val, y_pred)
 print ('AUC =%s' %auc)
 p +=cls.predict(DTest)
p /=(float(total))
print ('AUC averaged =%s' %auc_tot)
print ('AUC =%s' %auc)




model='XGBOOST_two_Stage'
 #
# predict on test set
submission='%s_score_%03f.csv' %(model,auc)
# create submission file

xgb_preds = pd.DataFrame({"patient_id": id_test, 'predict_screener': p})

xgb_preds.to_csv('../output/'+submission,index=False)
script=os.path.abspath(__file__)
print (script)
ranking=0.75
print ('score= %03f'%auc)
if auc>ranking:
    print('score is higher than %s'%ranking)
    archive_results(submission,xgb_preds,model,script)
