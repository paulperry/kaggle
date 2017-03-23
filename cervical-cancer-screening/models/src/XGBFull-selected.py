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
from sklearn import metrics
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

def preprocess_data(train,test):
    id_test=test['patient_id']

    train=train.drop(['patient_id'],axis=1)
    test=test.drop(['patient_id'],axis=1)
    #train=train.drop_duplicates()
    y=train['is_screener']
    train=train.drop(['is_screener'],axis=1)


    for f in train.columns:
        if train[f].dtype == 'object':
            print(f)
            lbl = preprocessing.LabelEncoder()
            lbl.fit(list(train[f].values) + list(test[f].values))
            train[f] = lbl.transform(list(train[f].values))
            test[f] = lbl.transform(list(test[f].values))

    return id_test,test,train,y

os.chdir(os.getcwd())
trainfile=('../input/patients_train.csv.gz')
testfile=('../input/patients_test.csv.gz')
surgical_file=('../input/surgical_selected_last.csv.gz')
activity_file=('../input/activity_selected_last.csv.gz')
diagnosis_file=('../input/diagnosis_selected_last.csv.gz')
procedure_file=('../input/procedure_selected_last.csv.gz')
prescription_file=('../input/prescription_selected_last.csv.gz')
physicians_file=('../input/physicians.csv.gz')
drugs_file=('../input/drugs.csv.gz')

train=pd.read_csv(trainfile,low_memory=False )
test=pd.read_csv(testfile,low_memory=False )

##prepare a sparse matrix#
train_ex_file=('../input/train_patients_to_exclude.csv.gz')
train_ex=pd.read_csv(train_ex_file,low_memory=False)
train=train[train.patient_id.isin(train_ex.patient_id)==False]
test_ex_file=('../input/test_patients_to_exclude.csv.gz')
test_ex=pd.read_csv(test_ex_file,low_memory=False)
test=test[test.patient_id.isin(test_ex.patient_id)==False]
print(train.shape,test.shape)

surgical=pd.read_csv(surgical_file )
train=pd.merge(train,surgical, on='patient_id',how='left')
test=pd.merge(test,surgical, on='patient_id',how='left')
print('after merging surgical')
print(train.shape,test.shape)

activity=pd.read_csv(activity_file )
train=pd.merge(train,activity, on='patient_id',how='left')
test=pd.merge(test,activity, on='patient_id',how='left')
print('after merging activity')
print(train.shape,test.shape)
prescription=pd.read_csv(prescription_file)
drugs=pd.read_csv(drugs_file)
physicians=pd.read_csv(physicians_file)
prescription=pd.merge(prescription,drugs, left_on='patient_id',right_on='drug_id',how='left')
prescription=pd.merge(prescription,physicians, left_on='patient_id',right_on='practitioner_id',how='left')
train=pd.merge(train,prescription,on='patient_id',how='left')
test=pd.merge(test,prescription,on='patient_id',how='left')
print('after merging prescription ')
print(train.shape,test.shape)

procedure=pd.read_csv(procedure_file )
diagnosis=pd.read_csv(diagnosis_file)
train=pd.merge(train,procedure,on='patient_id',how='left')
test=pd.merge(test,procedure,on='patient_id',how='left')
print('after merging  procedure')
print(train.shape,test.shape)
train=pd.merge(train,diagnosis, on='patient_id',how='left')
test=pd.merge(test,diagnosis, on='patient_id',how='left')
print('after merging diagnosis ')
print(train.shape,test.shape)


train=train.fillna(0)
test=test.fillna(0)

id_test,test,train,y=preprocess_data(train,test)
print(train.shape,test.shape)
#print(train.columns)

X=np.asarray(train)
y=np.asarray(y)
X_test=np.asarray(test)
X,y=shuffle(X,y,random_state=9)
X_train,X_val0,y_train,y_val0 = train_test_split(X,y,test_size=0.1,random_state=17)
X_train,X_val,y_train,y_val = train_test_split(X_train,y_train,test_size=0.1,random_state=77)

#from sklearn import preprocessing,decomposition
#scl=decomposition.PCA(n_components=None,whiten=False)
#scl=preprocessing.RobustScaler()
#X_train=scl.fit_transform(X_train)
#X_val=scl.transform(X_val)
#X_test=scl.transform(X_test)
#X_val0=scl.transform(X_val0)

dval=xgb.DMatrix(data=X_val,label=y_val)
dtrain=xgb.DMatrix(data=X_train,label=y_train)
DTest=xgb.DMatrix(data=X_test)
Dval0=xgb.DMatrix(data=X_val0)
watchlist = [(dval,'eval'), (dtrain,'train')]

params = {"objective": "binary:logistic",
          "eta": 0.023,
          "eta_decay":0.5,
          "max_depth": 6,
          "silent":1,
          "subsample": 0.9,
          "colsample_bytree": 0.65,
          "seed": 1193,
          "booster": "gbtree",
          "nthread":6,
          "eval_metric":'auc'
          }
#
clf = xgb.train(params, dtrain, num_boost_round=1000, evals=watchlist, early_stopping_rounds=30,verbose_eval=True,
                maximize= True)

predictions=clf.predict(DTest)
score=clf.best_score
print('best score:%s'%score)
y_pred=clf.predict(Dval0)

score=metrics.roc_auc_score(y_val0, y_pred)
print('score on extra set:%s' %score)
model='XGBOOST_onselected'
#
# predict on test set
submission='%s_score_%03f.csv' %(model,score)
# create submission file

preds = pd.DataFrame({"patient_id": id_test, 'predict_screener': predictions})
results=preds.groupby(['patient_id'])['predict_screener'].mean()
idx=preds.groupby(['patient_id'])['patient_id'].mean().astype(int)
test_ex['predict_screener']=0.0

# Create your first submission file
xgb_preds0 = pd.DataFrame({"patient_id": idx, "predict_screener": results})
xgb_preds=pd.concat([xgb_preds0,test_ex],axis=0)
xgb_preds.to_csv('../output/'+submission,index=False)
script=os.path.abspath(__file__)
print (script)
ranking=0.75
print ('score= %03f'%score)
if score>ranking:
    print('score is higher than %s'%ranking)
    archive_results(submission,xgb_preds,model,script)
