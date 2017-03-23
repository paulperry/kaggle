import sys # for stderr
import numpy as np
import pandas as pd
from sklearn import metrics
from sklearn.cross_validation import  train_test_split
import os
import shutil
from datetime import time
import datetime
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

# support class to redirect stderr

class flushfile():
    def __init__(self, f):
        self.f = f
    def __getattr__(self,name):
        return object.__getattribute__(self.f, name)
    def write(self, x):
        self.f.write(x)
        self.f.flush()
    def flush(self):
        self.f.flush()
# Stderr
oldstderr = sys.stderr # global

def capture_stderr(log):
    oldstderr = sys.stderr
    sys.stderr = open(log, 'w')
    sys.stderr = flushfile(sys.stderr)
    return log

def restore_stderr():
    sys.stderr = oldstderr
train_file = '../features/train_big_table.csv.gz'
test_file = '../features/test_big_table.csv.gz'
train = pd.read_csv(train_file)
test = pd.read_csv(test_file)
print train.shape,test.shape
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
print train.columns, test.columns
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
train_physician=pd.read_csv('../features/train_physician.csv.gz')
test_physician=pd.read_csv('../features/test_physician.csv.gz')

for f in train_physician.columns[1:]:
    train_physician.loc[(train_physician[f]>0),f]=1
    test_physician.loc[(test_physician[f]>0),f]=1
train_physician['KoF']=train_physician[train_physician.columns[1:]].sum(axis=1)
test_physician['KoF']=test_physician[test_physician.columns[1:]].sum(axis=1)
print (train_physician.head(5))
print(test_physician.head(5))

train=pd.merge(train,train_physician,on='patient_id',how='left')
test=pd.merge(test,test_physician,on='patient_id',how='left')
print('after merging physician')
print(train.shape,test.shape)

del train_physician,test_physician

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
###save full merged data
train.to_csv('../input/fulltrain.csv')
test.to_csv('../input/fulltest.csv')

from sklearn.utils import shuffle
def preprocess_data(train,test):

    y=train['is_screener']
    id_test=test['patient_id']
    train=train.drop(['patient_id','is_screener' ],axis=1)
    test=test.drop(['patient_id' ],axis=1)
    train=train.fillna(0)
    test=test.fillna(0)
    return id_test,test,train,y

id_test,test,train,y=preprocess_data(train,test)
print(train.shape,test.shape)


from sklearn.metrics import roc_auc_score
import xgboost as xgb
from hyperopt import hp, fmin, tpe, STATUS_OK, Trials

d_train,d_val,y_train,y_val = train_test_split(train,y,test_size=0.2,random_state=167)

def objective(space):

    clf = xgb.XGBClassifier(n_estimators = 200,
                            max_depth = space['max_depth'],
                            min_child_weight = space['min_child_weight'],
                            subsample = space['subsample'],learning_rate=space['learning_rate'],
                            colsample_bytree=space['colsample_bytree'],
                            colsample_bylevel=space['colsample_bylevel'],
                            seed=1950)


    eval_set  = [( d_train, y_train), ( d_val, y_val)]
    xgblog = capture_stderr('xgb.log')
    clf.fit(d_train, y_train,
            eval_set=eval_set, eval_metric="auc",
            early_stopping_rounds=30)

    pred = clf.predict_proba(d_val)[:,1]
    auc = roc_auc_score(y_val, pred)
    print ("SCORE:", auc)

    return{'loss':1-auc, 'status': STATUS_OK }


space ={
        'max_depth': hp.quniform("max_depth", 5, 20, 1),
        'min_child_weight': hp.quniform ('min_child_weight', 1, 10, 1),
        'subsample': hp.uniform ('subsample', 0.7, 1),
        'colsample_bytree': hp.uniform ('colsample_bytree', 0.1, 0.8),
        'colsample_bylevel': hp.uniform ('colsample_bylevel', 0.1, 1.0),
        'learning_rate': hp.uniform ('learning_rate', 0.01, 0.1)
    }


trials = Trials()
best = fmin(fn=objective,
            space=space,
            algo=tpe.suggest,
            max_evals=30,
            trials=trials)

print(best)
for key in best:
    print (key,best[key])

d_train,d_val,y_train,y_val = train_test_split(train,y,test_size=0.1,random_state=167)
clf = xgb.XGBClassifier(n_estimators = 3000,subsample=best['subsample'],colsample_bytree=best['colsample_bytree'],colsample_bylevel=best['colsample_bylevel'],
                        learning_rate=best['learning_rate'],
                        min_child_weight=best['min_child_weight'],max_depth=best['max_depth'],seed=950)
eval_set  = [( d_train, y_train), ( d_val, y_val)]
# Train an XGBoost model
#
xgblog = capture_stderr('xgb-tablegf.log')
clf.fit(d_train, y_train,eval_set=eval_set, eval_metric="auc", early_stopping_rounds=100)

restore_stderr()
pred = clf.predict_proba(d_val)[:,1]
auc = roc_auc_score(y_val, pred)
print ("SCORE:", auc)
score=clf.best_score
print('best score:%s'%score)

model='XGBOOST_Best'

X_test=np.asarray(test)
DTest=xgb.DMatrix(data=X_test)
predictions=clf.predict_proba(test)[:,1]
#
# predict on test set
submission='%s_score_%03f.csv' %(model,score)
# create submission file without grouping the results or eliminating id
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
ranking=0.79
print ('score= %03f'%score)
if score>ranking:
    print('score is higher than %s'%ranking)
    archive_results(submission,xgb_preds,model,script)


