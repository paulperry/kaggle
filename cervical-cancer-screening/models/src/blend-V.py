""""
This is for the moment the best blend with the coefficients 0.4*VW and 0.6*XGB.
NN does not contribute
"""

import pandas as pd
import numpy as np
import os
import math



inputdir='../blend/'
preds0=pd.read_csv(inputdir+'XGBOOST_Best_score_0.820948.csv.gz')

preds2=pd.read_csv(inputdir+'XGBOOST_Best_score_0.827847.csv.gz')

preds0=preds0.sort_values('patient_id', axis=0)

preds2=preds2.sort_values('patient_id', axis=0)


preds=(0.46*preds0['predict_screener'].values+0.54*preds2['predict_screener'].values)
idx = preds0.patient_id.values.astype(int)

# Create your first submission file
submission = pd.DataFrame({"patient_id": idx, "predict_screener": preds})
submission.to_csv(inputdir+"Multi-model-XGB-XGB-best.csv", index=False)
