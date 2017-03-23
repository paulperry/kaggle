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
def parse_xgblog(xgblog):
    import re
    pattern = re.compile(r'^\[(?P<round>\d+)\]\s*\D+:(?P<validation>\d+.\d+)\s*\D+:(?P<train>\d+.\d+)')
    xgb_list = []
    with open(xgblog, "r") as ins:
        next(ins)
        for line in ins:
            match = pattern.match(line)
            if match:
                idx = int(match.group("round"))
                validation = float(match.group("validation"))
                training = float(match.group("train"))
                xgb_list.append([idx, validation, training])
            else:
                pass # raise Exception("Failed to parse!")
    return xgb_list


def preprocess_data(train,test):
    id_test=test['patient_id']

    train=train.drop(['patient_id'],axis=1)
    test=test.drop(['patient_id'],axis=1)

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
train_file = '../features/train_big_table.csv.gz'
test_file = '../features/test_big_table.csv.gz'
train = pd.read_csv(train_file,low_memory=False)
test = pd.read_csv(test_file,low_memory=False)


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
print('after merging cancer and virus')
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

dval=xgb.DMatrix(data=X_val,label=y_val)
dtrain=xgb.DMatrix(data=X_train,label=y_train)
DTest=xgb.DMatrix(data=X_test)
Dval0=xgb.DMatrix(data=X_val0)
watchlist = [(dval,'eval'), (dtrain,'train')]


params = {"objective": "binary:logistic",
          "eta": 0.1,
          #"gamma":0.5,
          "max_depth": 8,
          #"max_delta_step":1,
          #"min_child_weight":10,
          "silent":1,
          "subsample": 0.95,
          "colsample_bytree": 0.7,
          "seed": 777,
          "booster": "gbtree",
          "nthread":6,
          "eval_metric":'auc'
          }
#
# Train an XGBoost model
# Train an XGBoost model
#xgblog = capture_stderr('xgb.log')
clf = xgb.train(params, dtrain, num_boost_round=4000, evals=watchlist, early_stopping_rounds=30,verbose_eval=True,
                maximize= True)
restore_stderr()
from sklearn import metrics


predictions=clf.predict(DTest)
score=clf.best_score
print('best score:%s'%score)
y_pred=clf.predict(Dval0)

score=metrics.roc_auc_score(y_val0, y_pred)
print('score on extra set:%s' %score)
model='XGBOOST_onraw_features'
 #
# predict on test set
submission='%s_score_%03f.csv' %(model,score)
# create submission file

xgb_preds = pd.DataFrame({"patient_id": id_test, 'predict_screener': predictions})

xgb_preds.to_csv('../output/'+submission,index=False)
script=os.path.abspath(__file__)
print (script)
ranking=0.75
print ('score= %03f'%score)
if score>ranking:
    print('score is higher than %s'%ranking)
    archive_results(submission,xgb_preds,model,script)
