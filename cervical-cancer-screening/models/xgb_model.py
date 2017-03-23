
# coding: utf-8

# # Genentech Cervical Cancer - XGB Paul Perry
# 
# https://www.kaggle.com/c/cervical-cancer-screening/

# In[1]:

# imports
import sys # for stderr
import numpy as np
import pandas as pd
import sklearn as skl
from sklearn import metrics
import matplotlib.pyplot as plt


# versions 
import sys
print(pd.datetime.now())
print('Python: '+sys.version)
print('numpy: '+np.__version__)
print('pandas: '+pd.__version__)
print('sklearn: '+skl.__version__)


# In[4]:

import datetime
start = datetime.datetime.now()
print(start)

print('loading train_bt_encoded.csv')
train_file = './features/train_bt_encoded.csv'
train = pd.read_csv(train_file)
train.set_index('patient_id', inplace=True)


cols = list(train.columns)

test_cols = list(cols)
test_cols.remove('is_screener')

# ## XGBoost

import xgboost as xgb

print('transforming train')

train.fillna(0,inplace=True)

### BUG BUG BUG ???
for physician in ['GO','GYN','OBG','OBS','OCC','ON','OTO','PCP','REN']:
    train[train[physician] > 0] = 1
print train.head(10)

### SOLVED BUG
#for physician in ['GO','GYN','OBG','OBS','OCC','ON','OTO','PCP','REN']:
#    train.loc[train[physician] > 0,physician] = 1
#print train.head(10)

dtrain = train[cols].copy()
xval  = dtrain.iloc[9::10,:]
xhold = dtrain.iloc[10::10,:]
xtrain = dtrain.loc[~dtrain.index.isin(xval.index),:]
xtrain = xtrain.loc[~xtrain.index.isin(xhold.index),:]
Y_train = xtrain.is_screener
X_train = xtrain.drop('is_screener',axis=1)

Y_val = xval.is_screener
X_val = xval.drop('is_screener',axis=1)

Y_hold = xhold.is_screener
X_hold = xhold.drop('is_screener',axis=1)

xg_train = xgb.DMatrix(X_train, label=Y_train)
xg_val = xgb.DMatrix(X_val, label=Y_val)
watchlist = [(xg_val, 'validation'), (xg_train, 'train')]

# set params
params = {'objective': 'binary:logistic',
          'booster': 'gbtree',
          'eta': 0.5,
          'max_depth': 5,
          'colsample_bylevel':1.0,
          'colsample_bytree': 0.3,
          'silent': 1,
          'eval_metric': 'auc',
          'seed': 8888
          }

print(params)

num_round = 100
early_stopping_rounds=10


# Train an XGBoost model

bst = xgb.train(params, xg_train, num_round, evals=watchlist, early_stopping_rounds=early_stopping_rounds, 
                 verbose_eval=True)




