# From: https://www.kaggle.com/slothouber/two-sigma-financial-modeling/kagglegym-emulation
#
# This file minics the kagglegym api, including scoring.
#
# You can use it to run experiments locally on the sample training set..
# To do this follow the following steps.
#
# Create the following directory structure
# .
# +--input
# |  +- train.h5
# +--Models
#    +- kagglegym.py
#    +- __init__.py
#    +- test_gym.py
#
# Where
#
# - train.h5 contains the unzipped data for the competition.
#
# - kagglegym.py is this file
#
# - test_gym.py  is a file with the following content:
#
#    import kagglegym
#
#    env = kagglegym.make()
#    observation = env.reset()
#
#    print(len(observation.target))
#    print(len(observation.train))
#
#    n = 0
#    rewards = []
#    while True:
#        target = observation.target
#        target.loc[:, 'y'] = 0.01
#        observation, reward, done, info = env.step(target)
#        if done:
#            break
#        rewards.append(reward)
#        n = n + 1
#
#    print(info)
#    print(n)
#    print(rewards[0:15])
#
# Running
#    python test_gym.py
#
# Should result in:
#
#  968
#  806298
#  {'public_score': -0.42791846067884648}
#  906
# [-0.57244240701870674, -0.69602355761934143, -0.76969605094330085,
# -0.88292556152797097, -0.77409471948462827, -0.62031952966389658,
# -0.39146488525587475, -0.84779897534426341, -0.45051451441360757,
# -0.56453402316570156, -0.89329857536073409, -0.81062686366326098,
# -0.61593843763923251, -0.67321374079183682, -0.82632908490446888]
#
# Revision history:
# 1. Minimal verion posted by Frans Slothouber on the forum.
#    see link https://www.kaggle.com/c/two-sigma-financial-modeling/discussion/26044#148202
# 2. Modification by Devin that add score
#    Parent of this fork
# 3. Bug fix for the scoring function, and documentation
#    This fork
# 4. Bug fix for computation of final score. Thanks to PeterBruhn and vgoklani
# 5. Fix in reset function, thanks to Devin
#

import pandas as pd
import numpy as np
from sklearn.metrics import r2_score


def r_score(y_true, y_pred, sample_weight=None, multioutput=None):
    r2 = r2_score(y_true, y_pred, sample_weight=sample_weight,
                  multioutput=multioutput)
    r = (np.sign(r2)*np.sqrt(np.abs(r2)))
    if r <= -1:
        return -1
    else:
        return r


class Observation(object):
    def __init__(self, train, target, features):
        self.train = train
        self.target = target
        self.features = features


class Environment(object):
    ID_COL_NAME = "id"
    SAMPLE_COL_NAME = "sample"
    TARGET_COL_NAME = "y"
    TIME_COL_NAME = "timestamp"
    
    def __init__(self):
        with pd.HDFStore("../input/train.h5", "r") as hfdata:
            self.timestamp = 0
            fullset = hfdata.get("train")
            self.unique_timestamp = fullset["timestamp"].unique()
            # Get a list of unique timestamps
            # use the first half for training and
            # the second half for the test set
            n = len(self.unique_timestamp)
            i = int(n/2)
            timesplit = self.unique_timestamp[i]
            self.n = n
            self.unique_idx = i
            self.train = fullset[fullset.timestamp < timesplit]
            self.test = fullset[fullset.timestamp >= timesplit]

            # Needed to compute final score
            self.full = self.test.loc[:, ['timestamp', 'y']]
            self.full['y_hat'] = 0.0
            self.temp_test_y = None

    def reset(self):
        timesplit = self.unique_timestamp[self.unique_idx]

        self.unique_idx = int(self.n / 2)
        self.unique_idx += 1
        subset = self.test[self.test.timestamp == timesplit]

        # reset index to conform to how kagglegym works
        target = subset.loc[:, ['id', 'y']].reset_index(drop=True)
        self.temp_test_y = target['y']

        target.loc[:, 'y'] = 0.0  # set the prediction column to zero

        # changed bounds to 0:110 from 1:111 to mimic the behavior
        # of api for feature
        features = subset.iloc[:, :110].reset_index(drop=True)

        observation = Observation(self.train, target, features)
        return observation

    def step(self, target):
        timesplit = self.unique_timestamp[self.unique_idx-1]
        # Since full and target have a different index we need
        # to do a _values trick here to get the assignment working
        y_hat = target.loc[:, ['y']]
        self.full.loc[self.full.timestamp == timesplit, ['y_hat']] = y_hat._values

        if self.unique_idx == self.n:
            done = True
            observation = None
            reward = r_score(self.temp_test_y, target.loc[:, 'y'])
            score = r_score(self.full['y'], self.full['y_hat'])
            info = {'public_score': score}
        else:
            reward = r_score(self.temp_test_y, target.loc[:, 'y'])
            done = False
            info = {}
            timesplit = self.unique_timestamp[self.unique_idx]
            self.unique_idx += 1
            subset = self.test[self.test.timestamp == timesplit]

            # reset index to conform to how kagglegym works
            target = subset.loc[:, ['id', 'y']].reset_index(drop=True)
            self.temp_test_y = target['y']

            # set the prediction column to zero
            target.loc[:, 'y'] = 0

            # column bound change on the subset
            # reset index to conform to how kagglegym works
            features = subset.iloc[:, 0:110].reset_index(drop=True)

            observation = Observation(self.train, target, features)

        return observation, reward, done, info

    def __str__(self):
        return "Environment()"


def make():
    return Environment()
