from __future__ import print_function
import os
import pandas as pd
import xgboost as xgb
import time

import shutil
from sklearn import preprocessing
from sklearn.cross_validation import train_test_split
import numpy as np

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
os.chdir('/home/cuoco/KC/cervical-cancer-screening/src')
trainfile=('../input/patients_train.csv.gz')
testfile=('../input/patients_test.csv.gz')
train=pd.read_csv(trainfile,low_memory=False )
test=pd.read_csv(testfile,low_memory=False )

surgical=pd.read_csv('../features/surgical_pap.csv.gz')
diagnosis=pd.read_csv('../features/diagnosis_hpv.csv.gz')
procedure_cervi=pd.read_csv('../features/procedure_cervi.csv.gz')
procedure_hpv=pd.read_csv('../features/procedure_hpv.csv.gz')
procedure_vaccine=pd.read_csv('../features/procedure_vaccine.csv.gz')
procedure_vagi=pd.read_csv('../features/procedure_vagi.csv.gz')
procedure_plan_type=pd.read_csv('../features/procedure_plan_type.csv.gz')
rx_payment=pd.read_csv('../features/rx_payment.csv.gz')
train_pract_screen_ratio=pd.read_csv('../features/train_pract_screen_ratio.csv.gz')
test_pract_screen_ratio=pd.read_csv('../features/test_pract_screen_ratio.csv.gz')
visits=pd.read_csv('../features/visits.csv.gz')



train=pd.merge(train,surgical, on='patient_id',how='left')
test=pd.merge(test,surgical, on='patient_id',how='left')
print('after merging surgical')
print(train.shape,test.shape)

train=pd.merge(train,diagnosis, on='patient_id',how='left')
test=pd.merge(test,diagnosis, on='patient_id',how='left')
print('after merging diagnosis')
print(train.shape,test.shape)
#train=pd.merge(train,procedure_cervi, on='patient_id',how='left')
#test=pd.merge(test,procedure_cervi, on='patient_id',how='left')
#train=pd.merge(train,procedure_hpv, on='patient_id',how='left')
#test=pd.merge(test,procedure_hpv, on='patient_id',how='left')
#train=pd.merge(train,procedure_vaccine, on='patient_id',how='left')
#test=pd.merge(test,procedure_vaccine, on='patient_id',how='left')
train=pd.merge(train,procedure_vagi, on='patient_id',how='left')
test=pd.merge(test,procedure_vagi, on='patient_id',how='left')
train=pd.merge(train,procedure_plan_type, on='patient_id',how='left')
test=pd.merge(test,procedure_plan_type, on='patient_id',how='left')
print('after merging procedure')
print(train.shape,test.shape)
train=pd.merge(train,rx_payment, on='patient_id',how='left')
test=pd.merge(test,rx_payment, on='patient_id',how='left')
print('after merging rx_payment')
print(train.shape,test.shape)

train=pd.merge(train,train_pract_screen_ratio, on='patient_id',how='left')
test=pd.merge(test,test_pract_screen_ratio, on='patient_id',how='left')
print('after merging pract_scree_ratio')
print(train.shape,test.shape)
train=pd.merge(train,visits, on='patient_id',how='left')
test=pd.merge(test,visits, on='patient_id',how='left')
print('after merging visits')
print(train.shape,test.shape)

###############################################################################################
def preprocess_data(train,test):
    y=train['is_screener']
    id_test=test['patient_id']
    train=train.drop(['patient_id','is_screener'],axis=1)
    test=test.drop(['patient_id'],axis=1)
    for f in train.columns:
        if train[f].dtype == 'object':
            print(f)
            lbl = preprocessing.LabelEncoder()
            lbl.fit(list(train[f].values) + list(test[f].values))
            train[f] = lbl.transform(list(train[f].values))
            test[f] = lbl.transform(list(test[f].values))
    return id_test,test,train,y

##prepare a sparse matrix
train=train.fillna(0)
test=test.fillna(0)

id_test,test,train,y=preprocess_data(train,test)
#print(train.columns)

X=np.asarray(train)
y=np.asarray(y)
X_test=np.asarray(test)
X_train,X_val,y_train,y_val = train_test_split(X,y,test_size=0.15,random_state=538)

#X_train=scl.fit_transform(X_train)
#X_val=scl.transform(X_val)
#X_test=scl.transform(X_test)

dval=xgb.DMatrix(data=X_val,label=y_val)
dtrain=xgb.DMatrix(data=X_train,label=y_train)
DTest=xgb.DMatrix(data=X_test)
watchlist = [(dval,'eval'), (dtrain,'train')]

params = {"objective": "binary:logistic",
          "eta": 0.001,
          "max_depth": 7,
          "silent":1,
          "subsample": 0.7,
          "colsample_bytree": 0.7,
          "seed": 1241,
          "booster": "gbtree",
          "nthread":-1,
          "eval_metric":'auc'}
#
clf = xgb.train(params, dtrain, num_boost_round=1200, evals=watchlist, early_stopping_rounds=30,
                verbose_eval=True, maximize= False)


predictions=clf.predict(DTest,ntree_limit=clf.best_ntree_limit)
score=clf.best_score

model='XGBOOST'
#
# predict on test set
submission='%s_score_%03f.csv' %(model,score)
# create submission file

preds = pd.DataFrame({"patient_id": id_test, 'predict_screener': predictions})
results=preds.groupby(['patient_id'])['predict_screener'].mean()
idx=preds.groupby(['patient_id'])['patient_id'].mean().astype(int)
# Create your first submission file
xgb_preds = pd.DataFrame({"patient_id": idx, "predict_screener": results})
xgb_preds.to_csv('../output/'+submission,index=False)
script=os.path.abspath(__file__)
print (script)
ranking=0.75
print ('score= %03f'%score)
if score>ranking:
    print('score is higher than %s'%ranking)
    archive_results(submission,xgb_preds,model,script)
