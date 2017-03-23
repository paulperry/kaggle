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
    now=time.time()[0:5]
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
train_file = '../features/my_train_new_bt_encoded.csv'
test_file = '../features/my_test_new_bt_encoded.csv'
train = pd.read_csv(train_file)
test = pd.read_csv(test_file)
print train.shape,test.shape

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


d_train,d_val,y_train,y_val = train_test_split(train,y,test_size=0.1,random_state=167)

clf = xgb.XGBClassifier(n_estimators = 2000,subsample=0.93,colsample_bytree=0.6,colsample_bylevel=0.9,
                        learning_rate=0.03,
                        min_child_weight=10,max_depth=17,seed=9)

eval_set  = [( d_train, y_train), ( d_val, y_val)]
# Train an XGBoost model
#
xgblog = capture_stderr('xgb-full-my.log')
clf.fit(d_train, y_train,eval_set=eval_set, eval_metric="auc", early_stopping_rounds=100)
from sklearn.externals import joblib
joblib.dump(clf, 'xgb_latestmodel.pkl') 
## to be loaded as clf = joblib.load('xgb_latestmodel.pk1')
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


