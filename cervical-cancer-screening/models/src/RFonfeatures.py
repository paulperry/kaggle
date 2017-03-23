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
os.chdir('/users/cuoco/home/KC/cervical-cancer-screening/src')
trainfile=('../input/patients_train.csv.gz')
testfile=('../input/patients_test.csv.gz')
train=pd.read_csv(trainfile,low_memory=False )
test=pd.read_csv(testfile,low_memory=False )
train_ex_file=('../input/train_patients_to_exclude.csv.gz')
train_ex=pd.read_csv(train_ex_file,low_memory=False)
train=train[train.patient_id.isin(train_ex.patient_id)==False]
test_ex_file=('../input/test_patients_to_exclude.csv.gz')
test_ex=pd.read_csv(test_ex_file,low_memory=False)
test=test[test.patient_id.isin(test_ex.patient_id)==False]
print(train.shape,test.shape)

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
#train=pd.merge(train,procedure_vagi, on='patient_id',how='left')
#test=pd.merge(test,procedure_vagi, on='patient_id',how='left')
#train=pd.merge(train,procedure_plan_type, on='patient_id',how='left')
#test=pd.merge(test,procedure_plan_type, on='patient_id',how='left')
#print('after merging procedure')
#print(train.shape,test.shape)
#train=pd.merge(train,rx_payment, on='patient_id',how='left')
#test=pd.merge(test,rx_payment, on='patient_id',how='left')
#print('after merging rx_payment')
#print(train.shape,test.shape)
train=pd.merge(train,train_pract_screen_ratio, on='patient_id',how='left')
test=pd.merge(test,test_pract_screen_ratio, on='patient_id',how='left')
print('after merging pract_screen_ratio')
print(train.shape,test.shape)


###############################################################################################


def preprocess_data(train,test):

    id_test=test['patient_id']
    train=train.drop(['patient_id'],axis=1)
    test=test.drop(['patient_id'],axis=1)
    train=train.drop_duplicates()
    y=train['is_screener']
    train=train.drop(['is_screener'],axis=1)
    #train=train.drop(['activity_month','primary_physician_role','practitioner_id_y'],axis=1)
    #test=test.drop(['activity_month','primary_physician_role','practitioner_id_y'],axis=1)
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
#print(train.columns)
print(train.shape,test.shape)
id_test,test,train,y=preprocess_data(train,test)
print(train.shape,test.shape)

X=np.asarray(train)
y=np.asarray(y)
X_test=np.asarray(test)
X_train,X_val,y_train,y_val = train_test_split(X,y,test_size=0.15,random_state=538)
from sklearn import linear_model,ensemble
#
clf=ensemble.RandomForestClassifier(n_estimators=100,random_state=100,max_depth=8,max_features=None,n_jobs=-1)
#clf =linear_model.SGDClassifier(loss='hinge', penalty='l2', alpha=0.00001, l1_ratio=0.15, fit_intercept=True, n_iter=200,
#                                shuffle=True, verbose=0, epsilon=0.1, n_jobs=-1, random_state=17, learning_rate='invscaling',eta0=1.0, power_t=0.5, class_weight=None, warm_start=False, average=False)
clf.fit(X_train,y_train)
predictions=clf.predict_proba(X_test)[:,1]
from sklearn.metrics import roc_auc_score
y_pred=clf.predict(X_val)
score=roc_auc_score(y_val, y_pred)

model='RF'
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
 #
