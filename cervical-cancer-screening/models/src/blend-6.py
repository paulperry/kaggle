""""
This is for the moment the best blend
"""

import pandas as pd
import numpy as np
import os
import math

def sigmoid(x):
  return 1 / (1 + math.exp(-x))

inputdir='../output/'
preds0=pd.read_csv(inputdir+'vw_nn.csv.gz')
preds1=pd.read_csv(inputdir+'Nolearn_score_0.801346.csv.gz')
preds2=pd.read_csv(inputdir+'Nolearn_score_0.802373.csv.gz')
preds3=pd.read_csv(inputdir+'XGBOOST_Best_score_0.880435.csv.gz')
preds4=pd.read_csv(inputdir+'XGBOOST_Best_score_0.881314.csv.gz')

#preds5=pd.read_csv(inputdir+'XGBOOST_Best_score_0.820948.csv.gz')
#preds6=pd.read_csv(inputdir+'XGBOOST_Best_score_0.821531.csv.gz')
preds0=preds0.sort_values('patient_id', axis=0)
preds1=preds1.sort_values('patient_id', axis=0)
preds2=preds2.sort_values('patient_id', axis=0)
preds3=preds3.sort_values('patient_id', axis=0)
preds4=preds4.sort_values('patient_id', axis=0)
#preds5=preds5.sort_values('patient_id', axis=0)
#preds6=preds6.sort_values('patient_id', axis=0)
#print preds0['predict_screener']
preds0['predict_screener']=preds0['predict_screener'].apply(sigmoid)
#print preds0['predict_screener']
#preds=(0.3*preds0['predict_screener'].values+0.2*preds1['predict_screener'].values\
#       +0.5*preds2['predict_screener'].values)
preds=(0.12*preds0['predict_screener'].values+\
    0.02*(preds1['predict_screener'].values+preds2['predict_screener'].values)/2.0+ \
       0.86*(preds3['predict_screener'].values+preds4['predict_screener'].values)/2.0)
idx = preds0.patient_id.values.astype(int)

# Create your first submission file
submission = pd.DataFrame({"patient_id": idx, "predict_screener": preds})
submission.to_csv(inputdir+"BEST-Multi-model-VW-XGB-NN-mean.csv", index=False)
