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
    test=test.drop(['patient_id' ],axis=1)
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
          "eta": 0.03,
          #"gamma":0.5,
          "max_depth": 8,
          #"max_delta_step":1,
          #"min_child_weight":10,
          "silent":1,
          "subsample": 0.95,
          "colsample_bytree": 0.7,
          "seed": 777,
          "booster": "gbtree",
          "nthread":-1,
          "eval_metric":'auc'
          }
#
# Train an XGBoost model

clf = xgb.train(params, dtrain, num_boost_round=5000, evals=watchlist, early_stopping_rounds=30,verbose_eval=True,
                maximize= True)
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
