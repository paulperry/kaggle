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

train_file = '../features/train_big_table.csv.gz'
test_file = '../features/test_big_table.csv.gz'
train = pd.read_csv(train_file)
test = pd.read_csv(test_file)
print(train.shape,test.shape)
procedure=pd.read_csv('../features/procedure/procedure_counts_selected.csv.gz',usecols=['patient_id','57454','81252','57456','57455','S4020','Q4111','S0605','23675','3303F','27756','G0143','00632','90696','S4023','69710','S9145'])
train=pd.merge(train,procedure,on='patient_id',how='left')
test=pd.merge(test,procedure,on='patient_id',how='left')
print('after merging ZZ procedure ')
print(train.shape,test.shape)
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

del cancer_test,cancer_train
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
del virus_test,virus_train

def preprocess_data(train,test):

    y=train['is_screener']
    id_test=test['patient_id']
    train=train.drop(['patient_id','is_screener' ],axis=1)
    test=test.drop(['patient_id' ],axis=1)

    for f in train.columns:
        if train[f].dtype == 'object':
            print(f)
            lbl = preprocessing.LabelEncoder()
            lbl.fit(list(train[f].values) + list(test[f].values))
            train[f] = lbl.transform(list(train[f].values))
            test[f] = lbl.transform(list(test[f].values))
    return id_test,test,train,y
print(train.shape,test.shape)

train=train.sort_index(axis=1)
test=test.sort_index(axis=1)
train=train.fillna(0)
test=test.fillna(0)

id_test,test,train,y=preprocess_data(train,test)
print(train.shape,test.shape)

X=np.asarray(train)
y=np.asarray(y)
X_test=np.asarray(test)

X,y=shuffle(X,y,random_state=9)
X_train,X_val,y_train,y_val = train_test_split(X,y,test_size=0.1,random_state=17)
from sklearn import preprocessing
#scl=decomposition.PCA(n_components=30,whiten=True)
scl=preprocessing.RobustScaler()
X_train=scl.fit_transform(X_train)
X_val=scl.transform(X_val)
X_test=scl.transform(X_test)


from sklearn import linear_model,ensemble
#
clf=ensemble.RandomForestClassifier(n_estimators=300,random_state=100,max_depth=15,max_features=None,n_jobs=-1)
#clf =linear_model.SGDClassifier(loss='hinge', penalty='l2', alpha=0.00001, l1_ratio=0.15, fit_intercept=True, n_iter=200,
#                                shuffle=True, verbose=0, epsilon=0.1, n_jobs=-1, random_state=17, learning_rate='invscaling',eta0=1.0, power_t=0.5, class_weight=None, warm_start=False, average=False)
clf.fit(X_train,y_train)
from sklearn import metrics
y_pred=clf.predict_proba(X_val)[:,1]

score=metrics.roc_auc_score(y_val, y_pred)
print('score on extra set:%s' %score)


model='RF_onTable_features'
#
# predict on test set

submission='%s_score_%03f.csv' %(model,score)
# create submission file
predictions=clf.predict_proba(X_test)[:,1]
preds = pd.DataFrame({"patient_id": id_test, 'predict_screener': predictions})

test_ex_file=('../input/test_patients_to_exclude.csv.gz')
test_ex=pd.read_csv(test_ex_file,low_memory=False)

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

