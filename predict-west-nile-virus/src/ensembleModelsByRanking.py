import pandas as pd
import numpy as np
from scipy.stats import rankdata

weights = [0.9,0.8,1.0] # your weights for each model
files = ['predictions1.csv', 'predictions2.csv', 'predictions3.csv'] # your prediction files 

finalRank = 0
for i in range(len(files)):
    temp_df = pd.read_csv(files[i])
    finalRank = finalRank + rankdata(temp_df.WnvPresent, method='ordinal') * weights[i]
finalRank = finalRank / (max(finalRank) + 1.0)

df = temp_df.copy()
df['WnvPresent'] = finalRank
df.to_csv('ensembleByRanking.csv', index = False)