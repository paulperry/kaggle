from __future__ import print_function
import os,sys
import pandas as pd
import shutil
import time
from sklearn import preprocessing
from sklearn.cross_validation import train_test_split
import numpy as np
from sklearn.utils import shuffle
from sklearn.metrics import roc_auc_score

# Lasagne (& friends) imports
import theano,lasagne
from lasagne import regularization
from lasagne import layers
from lasagne.layers import InputLayer,DropoutLayer,DenseLayer, Conv1DLayer
from nolearn.lasagne import BatchIterator, NeuralNet
from lasagne.objectives import categorical_crossentropy, aggregate, binary_crossentropy
from lasagne.updates import nesterov_momentum,sgd,rmsprop,adagrad,adadelta,adam
from lasagne.nonlinearities import softmax,identity,sigmoid,tanh,rectify,leaky_rectify, very_leaky_rectify,identity
from nolearn.lasagne import TrainSplit
#
import logging
logging.basicConfig(
            format="%(message)s",
            level=logging.DEBUG,
            stream=sys.stdout)
#######################################
class AdjustVariable (object):
    def __init__ (self,name,start=0.03,stop=0.001):
        self.name = name
        self.start,self.stop = start,stop
        self.ls = None

    def __call__ (self,nn,train_history):
        if self.ls is None:
            self.ls = np.linspace (self.start,self.stop,nn.max_epochs)

        epoch = train_history[-1]['epoch']
        new_value = np.float32 (self.ls[epoch - 1])
        getattr (nn,self.name).set_value (new_value)


class EarlyStopping (object):
    def __init__ (self,patience=100):
        self.patience = patience
        self.best_valid = np.inf
        self.best_valid_epoch = 0
        self.best_weights = None

    def __call__ (self,nn,train_history):
        current_valid = train_history[-1]['valid_loss']
        current_epoch = train_history[-1]['epoch']
        if current_valid < self.best_valid:
            self.best_valid = current_valid
            self.best_valid_epoch = current_epoch
            self.best_weights = nn.get_all_params_values ()
        elif self.best_valid_epoch + self.patience < current_epoch:
            print("Early stopping.")
            print("Best valid loss was {:.6f} at epoch {}.".format (
                    self.best_valid,self.best_valid_epoch))
            nn.load_params_from (self.best_weights)
            raise StopIteration ()


class _OnEpochFinished:
    def __call__(self, nn, train_history):
        self.train_history = train_history
        if len(train_history) > 1:
            raise StopIteration()

#################################################################################
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
train_file = '../features/train_big_table.csv.gz'
test_file = '../features/test_big_table.csv.gz'
train = pd.read_csv(train_file)
test = pd.read_csv(test_file)
print( train.shape,test.shape)
from sklearn import preprocessing
for f in train.columns:
        if train[f].dtype == 'object':
            print(f)
            lbl = preprocessing.LabelEncoder()
            lbl.fit(list(train[f].values) + list(test[f].values))
            train[f] = lbl.transform(list(train[f].values))
            test[f] = lbl.transform(list(test[f].values))
train=train.sort_index(axis=1)
test=test.sort_index(axis=1)
print(train.columns, test.columns)
train_fpsoto=pd.read_csv('../features/train_fpsoto.csv.gz')
test_fpsoto=pd.read_csv('../features/test_fpsoto.csv.gz')
train=pd.merge(train,train_fpsoto,on='patient_id',how='left')
test=pd.merge(test,test_fpsoto,on='patient_id',how='left')
print('after merging fpsoto')
print(train.shape,test.shape)
del train_fpsoto,test_fpsoto
train_obgyn=pd.read_csv('../features/train_obgyn.csv.gz')
test_obgyn=pd.read_csv('../features/test_obgyn.csv.gz')
train=pd.merge(train,train_obgyn,on='patient_id',how='left')
test=pd.merge(test,test_obgyn,on='patient_id',how='left')
print('after merging obgyn')
print(train.shape,test.shape)
del train_obgyn,test_obgyn
cancer_train=pd.read_csv('../features/train_diagnosis_cancer.csv.gz',index_col=None)

cancer_train['have_cancer']=1
cancer_train['sum_cancer']=1

idxC=cancer_train.groupby(['patient_id'])['patient_id'].mean().astype(int)
hc=cancer_train.groupby(['patient_id'])['have_cancer'].mean().astype(int)
sumhc=cancer_train.groupby(['patient_id'])['sum_cancer'].sum().astype(int)
cancer_train = pd.DataFrame({"patient_id": idxC.values, 'have_cancer': hc.values,'sum_cancer': sumhc.values })
print(cancer_train.head(5))

cancer_test=pd.read_csv('../features/test_diagnosis_cancer.csv.gz',index_col=None)
cancer_test['have_cancer']=1
cancer_test['sum_cancer']=1
print(cancer_test.info())
idxC=cancer_test.groupby(['patient_id'])['patient_id'].mean().astype(int)
hc=cancer_test.groupby(['patient_id'])['have_cancer'].mean().astype(int)
sumhc=cancer_test.groupby(['patient_id'])['sum_cancer'].sum().astype(int)
cancer_test = pd.DataFrame({"patient_id": idxC.values, 'have_cancer': hc.values,'sum_cancer': sumhc.values })

train=pd.merge(train,cancer_train, on='patient_id',how='left')
test=pd.merge(test,cancer_test, on='patient_id',how='left')
print(train.shape,test.shape)


virus_train=pd.read_csv('../features/train_diagnosis_virus.csv.gz',index_col=None)

virus_train['have_virus']=1
virus_train['sum_virus']=1

idxC=virus_train.groupby(['patient_id'])['patient_id'].mean().astype(int)
hc=virus_train.groupby(['patient_id'])['have_virus'].mean().astype(int)
sumhc=virus_train.groupby(['patient_id'])['sum_virus'].sum().astype(int)
virus_train = pd.DataFrame({"patient_id": idxC.values, 'have_virus': hc.values,'sum_virus': sumhc.values })
print(virus_train.head(5))

virus_test=pd.read_csv('../features/test_diagnosis_virus.csv.gz',index_col=None)
virus_test['have_virus']=1
virus_test['sum_virus']=1
print(virus_test.info())
idxC=virus_test.groupby(['patient_id'])['patient_id'].mean().astype(int)
hc=virus_test.groupby(['patient_id'])['have_virus'].mean().astype(int)
sumhc=virus_test.groupby(['patient_id'])['sum_virus'].sum().astype(int)
virus_test = pd.DataFrame({"patient_id": idxC.values, 'have_virus': hc.values,'sum_virus': sumhc.values })

train=pd.merge(train,virus_train, on='patient_id',how='left')
test=pd.merge(test,virus_test, on='patient_id',how='left')
print(train.shape,test.shape)
del cancer_train,cancer_test,virus_train,virus_test
procedure_counts=pd.read_csv('../features/procedure/procedure_counts_selected.csv.gz')

train=pd.merge(train,procedure_counts,on='patient_id',how='left')
test=pd.merge(test,procedure_counts,on='patient_id',how='left')
print('after merging ZZ procedure ')
print(train.shape,test.shape)
del procedure_counts
procedure_years=pd.read_csv('../features/procedure/procedure_years.csv.gz')
train=pd.merge(train,procedure_years,on='patient_id',how='left')
test=pd.merge(test,procedure_years,on='patient_id',how='left')
print('after merging ZZ procedure ')
print(train.shape,test.shape)
del procedure_years
activity_stats=pd.read_csv('../features/activity/activity_stats.csv.gz')
train=pd.merge(train,activity_stats,on='patient_id',how='left')
test=pd.merge(test,activity_stats,on='patient_id',how='left')
print('after merging ZZ activity ')
print(train.shape,test.shape)
del activity_stats
import shutil

from sklearn.utils import shuffle
def preprocess_data(train,test):

    y=train['is_screener']
    id_test=test['patient_id']
    train=train.drop(['patient_id','is_screener' ],axis=1)
    test=test.drop(['patient_id' ],axis=1)
    train=train.fillna(0)
    test=test.fillna(0)
    return id_test,test,train,y
print(train.shape,test.shape)
id_test,test,train,y=preprocess_data(train,test)
print(train.shape,test.shape)



X=np.asarray(train).astype(np.float32)
y=np.asarray(y).astype(np.int32)
X_test=np.asarray(test).astype(np.float32)

X,y=shuffle(X,y,random_state=9)

X_train,X_val0,y_train,y_val0 = train_test_split(X,y,test_size=0.1,random_state=95)

preproc=preprocessing.StandardScaler()
X_train=preproc.fit_transform(X_train).astype(np.float32)
X_val0=preproc.transform(X_val0).astype(np.float32)
X_test=preproc.transform(X_test).astype(np.float32)

clf=NeuralNet (
 layers=[
        ('input', layers.InputLayer),
        ('dropout1', layers.DropoutLayer),
        ('hidden2', layers.DenseLayer),
        ('maxout2',layers.FeaturePoolLayer),
        ('dropout2', layers.DropoutLayer),
        ('hidden3', layers.DenseLayer),
        ('maxout3',layers.FeaturePoolLayer),
        ('dropout3', layers.DropoutLayer),
        ('hidden4', layers.DenseLayer),
        ('output', layers.DenseLayer)
        ],
    input_shape = (None, X_train.shape[1]),
    dropout1_p = 0.1,
    hidden2_num_units = 1024,
    hidden2_nonlinearity=rectify,
    maxout2_pool_size=2,
    dropout2_p = 0.5,
    hidden3_num_units = 512,
    hidden3_nonlinearity=sigmoid,
    maxout3_pool_size=2,
    dropout3_p = 0.4,
    
    hidden4_num_units = 256,
    hidden4_nonlinearity=very_leaky_rectify,
    output_num_units = 2,
    output_nonlinearity = lasagne.nonlinearities.softmax,

    # optimization method:
    # update = adam,
    #update=nesterov_momentum,
    update_momentum=theano.shared(np.float32(0.9)),
    update_learning_rate=theano.shared(np.float32(0.01)),
    ###
         
    regression = False, 
    max_epochs = 2000,

    train_split=TrainSplit (eval_size=0.1),
    #custom_score=('auc', lambda y_true, y_proba: roc_auc_score(y_true, y_proba[:, 1])),

    on_epoch_finished=[
        AdjustVariable ('update_learning_rate',start=0.01,stop=0.0001),
        AdjustVariable('update_momentum', start=0.9, stop=0.999),
        EarlyStopping (patience=50),
        ],
    verbose = 1
    )

clf.fit(X_train,y_train)
from sklearn import metrics
y_pred=clf.predict_proba(X_val0)[:,1]

score=metrics.roc_auc_score(y_val0, y_pred)
print('score on extra set:%s' %score)


model='Nolearn'
#
# predict on test set

submission='%s_score_%03f.csv' %(model,score)
# create submission file
predictions=clf.predict_proba(X_test)[:,1]
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
ranking=0.75
print ('score= %03f'%score)
if score>ranking:
    print('score is higher than %s'%ranking)
    archive_results(submission,xgb_preds,model,script)

