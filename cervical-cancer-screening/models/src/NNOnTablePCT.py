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
###This is not a fair feature. it include info from label somewhere
#train=train.drop(['pract_screen_pct','age_pct','cbsa_pct'],axis=1)
#test=test.drop(['pract_screen_pct','age_pct','cbsa_pct' ],axis=1)
train=train.fillna(0)
test=test.fillna(0)

id_test,test,train,y=preprocess_data(train,test)
print(train.shape,test.shape)
#print(train.columns)

X=np.asarray(train).astype(np.float32)
y=np.asarray(y).astype(np.int32)
X_test=np.asarray(test).astype(np.float32)
X,y=shuffle(X,y,random_state=9)
X_train,X_val0,y_train,y_val0 = train_test_split(X,y,test_size=0.1,random_state=17)

preproc=preprocessing.StandardScaler()


X_train=preproc.fit_transform(X_train).astype(np.float32)
X_val0=preproc.transform(X_val0).astype(np.float32)
X_test=preproc.transform(test).astype(np.float32)

clf=NeuralNet (
 layers=[
        ('input', layers.InputLayer),
        ('dropout1', layers.DropoutLayer),
        
        ('hidden2', layers.DenseLayer),
        
        ('hidden3', layers.DenseLayer),

        
        ('hidden4', layers.DenseLayer),
        ('dropout4', layers.DropoutLayer),
        
        ('output', layers.DenseLayer)
        ],
    input_shape = (None, X_train.shape[1]),
    dropout1_p = 0.1,
    
    hidden2_num_units = 1000,
    hidden2_nonlinearity=rectify,

    
    hidden3_num_units = 1000,
    hidden3_nonlinearity=sigmoid,
    

    
    hidden4_num_units = 500,
    hidden4_nonlinearity=rectify,
    dropout4_p = 0.1,
    
    output_num_units = 2,
    output_nonlinearity = lasagne.nonlinearities.softmax,

    # optimization method:
    #update = adagrad,
    update=nesterov_momentum,
    update_momentum=theano.shared(np.float32(0.92)),     
    update_learning_rate=theano.shared(np.float32(0.001)),
    ###
         
    regression = False, 
    max_epochs = 1000,

    train_split=TrainSplit (eval_size=0.1),
    #custom_score=('auc', lambda y_true, y_proba: roc_auc_score(y_true, y_proba[:, 1])),

    on_epoch_finished=[
        AdjustVariable ('update_learning_rate',start=0.001,stop=0.0001),
        AdjustVariable('update_momentum', start=0.92, stop=0.999),
        EarlyStopping (patience=100),
        ],
    verbose = 1
    )

clf.fit(X_train,y_train)
from sklearn import metrics
y_pred=clf.predict_proba(X_val0)[:,1]

score=metrics.roc_auc_score(y_val0, y_pred)
print('score on extra set:%s' %score)


model='NN_onTable_features'
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

