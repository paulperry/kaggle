""""
This is for the moment the best blend with the coefficients 0.4*VW and 0.6*XGB.
NN does not contribute
"""

import pandas as pd
import numpy as np
import os
import math

def sigmoid(x):
  return 1 / (1 + math.exp(-x))

inputdir='../blend/'
preds0=pd.read_csv(inputdir+'vw_nn.csv.gz')
#preds1=pd.read_csv(inputdir+'Nolearn_score_0.800750.csv.gz')
preds2=pd.read_csv(inputdir+'XGBOOST_Best_score_0.820948.csv.gz')

preds0=preds0.sort_values('patient_id', axis=0)
#preds1=preds1.sort_values('patient_id', axis=0)
preds2=preds2.sort_values('patient_id', axis=0)

#print preds0['predict_screener']
preds0['predict_screener']=preds0['predict_screener'].apply(sigmoid)
#print preds0['predict_screener']
#preds=(0.3*preds0['predict_screener'].values+0.2*preds1['predict_screener'].values\
#       +0.5*preds2['predict_screener'].values)
preds=(0.4*preds0['predict_screener'].values+0.6
       *preds2['predict_screener'].values)
idx = preds0.patient_id.values.astype(int)

# Create your first submission file
submission = pd.DataFrame({"patient_id": idx, "predict_screener": preds})
submission.to_csv(inputdir+"Multi-model-VW-XGB-best-II.csv", index=False)
