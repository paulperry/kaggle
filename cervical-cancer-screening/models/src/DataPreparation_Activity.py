from __future__ import print_function
import os
import pandas as pd


os.chdir('/home/cuoco/KC/k-genentech/src')
trainfile=('../input/patients_train.csv.gz')
testfile=('../input/patients_test.csv.gz')
activity_file=('../input/patient_activity_head.csv.gz')

train=pd.read_csv(trainfile,usecols=['patient_id'])
test=pd.read_csv(testfile,usecols=['patient_id'])
id=pd.DataFrame()
id=pd.concat([train,test],axis=0)
print(train.shape,test.shape,id.shape)
chunk=10000000
from sklearn import preprocessing
reader = pd.read_csv(activity_file, sep=',',chunksize=chunk,header=0,iterator=True)
data=pd.DataFrame()
for tmp in reader:
    tmp=tmp[tmp.patient_id.isin(id.patient_id)==True]

    tmp=tmp.sort_values(by='activity_year').groupby("patient_id", as_index=False).last()

    data=pd.concat([data,tmp],axis=0)
    data=data.sort_values(by='activity_year').groupby("patient_id", as_index=False).last()
    print(tmp.shape,data.shape)

 
data=data.fillna(0)
data=data.sort_values(by='activity_year').groupby("patient_id", as_index=False).last()
print(data.shape)
data.to_csv('/home/cuoco/KC/cervical-cancer-screening/input/activity_selected_last.csv',index=False)