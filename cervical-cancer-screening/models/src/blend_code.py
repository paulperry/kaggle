import pandas as pd
import numpy as np
import os
from glob import glob
import glob, os
import sys
from kaggleutils import blendingDir
#glob_files = sys.argv[1]
#loc_outfile = sys.argv[2]
glob_files='/home/cuoco/KC/cervical-cancer-screening/output/'
loc_outfile='/home/cuoco/KC/cervical-cancer-screening/output/'
inputdir=glob_files
outputdir=loc_outfile

f,idx,results=blendingDir.blenddir(inputdir,'numeric')
print('number of averaged file: %s' %f)

# Create your first submission file
submission = pd.DataFrame({"patient_id": idx, "predict_screener": results})
submission.to_csv(outputdir+"multi_mean_multimodel.csv", index=False)
