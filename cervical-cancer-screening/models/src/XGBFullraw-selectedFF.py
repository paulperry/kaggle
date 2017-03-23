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
train_file = '../input/patients_train.csv.gz'
test_file = '../input/patients_test.csv.gz'
train = pd.read_csv(train_file)
test = pd.read_csv(test_file)
train.drop( 'patient_gender', axis = 1, inplace = True )
test.drop( 'patient_gender', axis = 1, inplace = True )
########## last asctivity files
activity_file=('../input/activity_selected_last.csv.gz')
diagnosis_file=('../input/diagnosis_selected_last.csv.gz')
procedure_file=('../input/procedure_selected_last.csv.gz')
surgical_file=('../input/surgical_selected_last.csv.gz')
prescription_file=('../input/prescription_selected_last.csv.gz')
physicians_file=('../input/physicians.csv.gz')
drugs_file=('../input/drugs.csv.gz')
############ first activity files
activity_file_first=('../input/activity_selected_last.csv.gz')
diagnosis_file_first=('../input/diagnosis_selected_last.csv.gz')
procedure_file_first=('../input/procedure_selected_last.csv.gz')
surgical_file_first=('../input/surgical_selected_last.csv.gz')
prescription_file=('../input/prescription_selected_last.csv.gz')

#activity=pd.read_csv(activity_file )
#Fa=pd.read_csv(activity_file_first,usecols=['activity_year'])
#print(Fa)
#activity['activity_first_year']=Fa['activity_year']
#activity['delta_time_activity']=activity['activity_year']-activity['activity_first_year']
#print(activity[activity['delta_time_activity']!=0,'delta_time_activity'])

#train=pd.merge(train,activity, on='patient_id',how='left')
#test=pd.merge(test,activity, on='patient_id',how='left')
#print('after merging activity')
#print(train.shape,test.shape)

procedure=pd.read_csv(procedure_file )
diagnosis=pd.read_csv(diagnosis_file)
diagnosis=pd.merge(diagnosis,procedure,on=['patient_id','claim_id'],how='left')

train=pd.merge(train,diagnosis, on='patient_id',how='left')
test=pd.merge(test,diagnosis, on='patient_id',how='left')
print('after merging diagnosis ')
print(train.shape,test.shape)

prescription=pd.read_csv(prescription_file)
#drugs=pd.read_csv(drugs_file)
physicians=pd.read_csv(physicians_file)
#prescription=pd.merge(prescription,drugs ,on='drug_id',how='left')
prescription=pd.merge(prescription,physicians,on='practitioner_id',how='left')
train=pd.merge(train,prescription,on='patient_id',how='left')
test=pd.merge(test,prescription,on='patient_id',how='left')
print('after merging prescription ')
print(train.shape,test.shape)
surgical=pd.read_csv(surgical_file )
train=pd.merge(train,surgical, on='patient_id',how='left')
test=pd.merge(test,surgical, on='patient_id',how='left')
print('after merging surgical')
print(train.shape,test.shape)
train_ex_file=('../input/train_patients_to_exclude.csv.gz')
train_ex=pd.read_csv(train_ex_file,low_memory=False)
train=train[train.patient_id.isin(train_ex.patient_id)==False]
test_ex_file=('../input/test_patients_to_exclude.csv.gz')
test_ex=pd.read_csv(test_ex_file,low_memory=False)
test=test[test.patient_id.isin(test_ex.patient_id)==False]
print(train.shape,test.shape)
train_file_t = '../features/train_big_table.csv.gz'
test_file_t = '../features/test_big_table.csv.gz'
train_t = pd.read_csv(train_file_t)
test_t = pd.read_csv(test_file_t)
train_t=train_t.drop(['is_screener','patient_age_group','patient_state','ethinicity','household_income','education_level'],axis=1)
test_t=test_t.drop(['patient_age_group','patient_state','ethinicity','household_income','education_level'],axis=1)
train=pd.merge(train,train_t, on='patient_id',how='left')
test=pd.merge(test,test_t, on='patient_id',how='left')
print('after merging table')
print(train.shape,test.shape)
train_top_diagn=pd.read_csv('../features/train_top_diagnosis.csv.gz',usecols=['patient_id','632'])
test_top_diagn=pd.read_csv('../features/test_diagnosis_632.csv.gz',usecols=['patient_id','632'])

#print(train.columns,test.columns)
train=pd.merge(train,train_top_diagn, on='patient_id',how='left')
test=pd.merge(test,test_top_diagn, on='patient_id',how='left')
train=train[['632','patient_id','is_screener','diagnosis_code','num_procedures','patient_state','state','cbsa','num_visits','patient_age_group','CBSA','surgical_code','claim_id','visits','INPATIENT','household_income','plan_type_y']]
test=test[['632','patient_id','diagnosis_code','num_procedures','patient_state','state','cbsa','num_visits','patient_age_group','CBSA','surgical_code','claim_id','visits','INPATIENT','household_income','plan_type_y']]
train=train.fillna(0)
test=test.fillna(0)

id_test,test,train,y=preprocess_data(train,test)
print(train.shape,test.shape)
#print(train.columns)

X=np.asarray(train)
y=np.asarray(y)
X_test=np.asarray(test)
X_train,X_val0,y_train,y_val0 = train_test_split(X,y,test_size=0.1,random_state=17)
X_train,X_val,y_train,y_val = train_test_split(X_train,y_train,test_size=0.1,random_state=77)

dval=xgb.DMatrix(data=X_val,label=y_val)
dtrain=xgb.DMatrix(data=X_train,label=y_train)
DTest=xgb.DMatrix(data=X_test)
Dval0=xgb.DMatrix(data=X_val0)
watchlist = [(dval,'eval'), (dtrain,'train')]

params = {"objective": "binary:logistic",
          "eta": 0.03,
          "gamma":10,
          "max_depth": 14,
          "max_delta_step":1,
          "min_child_weight":10,
          "silent":1,
          "subsample": 0.85,
          "colsample_bytree": 0.7,
          "seed": 777,
          "booster": "gbtree",
          "nthread":-1,
          "eval_metric":'auc'
          }
#
# Train an XGBoost model
# Train an XGBoost model
xgblog = capture_stderr('xgb.log')
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
