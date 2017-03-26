import time
start_time = time.time()

import numpy as np
import pandas as pd
from sklearn import pipeline, grid_search
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import FeatureUnion
from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import mean_squared_error, make_scorer
from nltk.metrics import edit_distance
from nltk.stem.porter import *
stemmer = PorterStemmer()
import re
import random
random.seed(2016)
import xgboost as xgb

def fmean_squared_error(ground_truth, predictions):
    fmean_squared_error_ = mean_squared_error(ground_truth, predictions)**0.5
    return fmean_squared_error_

RMSE  = make_scorer(fmean_squared_error, greater_is_better=False)

class cust_regression_vals(BaseEstimator, TransformerMixin):
    def fit(self, x, y=None):
        return self
    def transform(self, hd_searches):
        d_col_drops=['id','relevance','search_term','product_title','product_description','product_info','attr','brand']
        hd_searches = hd_searches.drop(d_col_drops,axis=1).values
        return hd_searches

class cust_txt_col(BaseEstimator, TransformerMixin):
    def __init__(self, key):
        self.key = key
    def fit(self, x, y=None):
        return self
    def transform(self, data_dict):
        return data_dict[self.key].apply(str)

train = pd.read_csv('xgb_train.csv')
test  = pd.read_csv('xgb_test.csv')
#xgtrain = xgb.DMatrix(train.values, y_train.values)
#xgtest = xgb.DMatrix(test.values)

y_train = train['relevance']
id_test = test['id']

n_jobs = 1

# http://scikit-learn.org/stable/faq.html#why-do-i-sometime-get-a-crash-freeze-with-n-jobs-1-under-osx-or-linux
if n_jobs != 1:
    import multiprocessing
    multiprocessing.set_start_method('forkserver')

xgb_model = xgb.XGBRegressor(learning_rate=0.25, silent=False, objective="reg:linear", nthread=-1, gamma=0, min_child_weight=1, max_delta_step=0,
                 subsample=1, colsample_bytree=1, colsample_bylevel=1, reg_alpha=0, reg_lambda=1, scale_pos_weight=1,
                 base_score=0.5, seed=0, missing=None)
tfidf = TfidfVectorizer(ngram_range=(1, 1), stop_words='english')
tsvd = TruncatedSVD(n_components=10, random_state = 2016)
clf = pipeline.Pipeline([
        ('union', FeatureUnion(
                    transformer_list = [
                        ('cst',  cust_regression_vals()),  
                        ('txt1', pipeline.Pipeline([('s1', cust_txt_col(key='search_term')), ('tfidf1', tfidf), ('tsvd1', tsvd)])),
                        ('txt2', pipeline.Pipeline([('s2', cust_txt_col(key='product_title')), ('tfidf2', tfidf), ('tsvd2', tsvd)])),
                        ('txt3', pipeline.Pipeline([('s3', cust_txt_col(key='product_description')), ('tfidf3', tfidf), ('tsvd3', tsvd)])),
                        ('txt4', pipeline.Pipeline([('s4', cust_txt_col(key='brand')), ('tfidf4', tfidf), ('tsvd4', tsvd)]))
                        ],
                    transformer_weights = {
                        'cst': 1.0,
                        'txt1': 0.5,
                        'txt2': 0.25,
                        'txt3': 0.0,
                        'txt4': 0.5
                        },
                n_jobs = n_jobs
                )), 
        ('xgb_model', xgb_model)])
param_grid = {'xgb_model__max_depth': [5], 'xgb_model__n_estimators': [10]}
model = grid_search.GridSearchCV(estimator = clf, param_grid = param_grid, n_jobs = n_jobs, cv = 2, verbose = 20, scoring=RMSE)
model.fit(train, y_train.values)

print("Best parameters found by grid search:")
print(model.best_params_)
print("Best CV score:")
print(model.best_score_)
print(model.best_score_ + 0.47003199274)

y_pred = model.predict(test)

#print(len(y_pred))
#pd.DataFrame({"id": id_test, "relevance": y_pred}).to_csv('submission_before.csv',index=False)
min_y_pred = min(y_pred)
max_y_pred = max(y_pred)
min_y_train = min(y_train.values)
max_y_train = max(y_train.values)
print(min_y_pred, max_y_pred, min_y_train, max_y_train)
for i in range(len(y_pred)):
    if y_pred[i]<1.0:
        y_pred[i] = 1.0
    if y_pred[i]>3.0:
        y_pred[i] = 3.0
    #y_pred[i] = min_y_train + (((y_pred[i] - min_y_pred)/(max_y_pred - min_y_pred))*(max_y_train - min_y_train))
pd.DataFrame({"id": id_test, "relevance": y_pred}).to_csv('xgb1_submission.csv',index=False)
print("--- Training & Testing: %s minutes ---" % round(((time.time() - start_time)/60),2))
