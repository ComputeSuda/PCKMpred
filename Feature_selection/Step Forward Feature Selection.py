from collections import Counter

import pandas as pd
import numpy as np
import warnings

warnings.filterwarnings('ignore')

import matplotlib.pyplot as plt
import seaborn as sns
# %matplotlib inline

from sklearn.model_selection import train_test_split

from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.metrics import roc_auc_score

from mlxtend.feature_selection import SequentialFeatureSelector as SFS


def run_randomForests(X_train, X_test, y_train, y_test):
    rf = RandomForestClassifier(n_estimators=200, random_state=39, max_depth=4)
    rf.fit(X_train, y_train)
    print('Train set')
    pred = rf.predict_proba(X_train)
    print('Random Forests roc-auc: {}'.format(roc_auc_score(y_train, pred[:, 1])))
    print('Test set')
    pred = rf.predict_proba(X_test)
    print('Random Forests roc-auc: {}'.format(roc_auc_score(y_test, pred[:, 1])))

    return pred


# find and remove correlated features
# in order to reduce the feature space a bit
# so that the algorithm takes shorter

def correlation(dataset, threshold):
    col_corr = set()  # Set of all the names of correlated columns
    corr_matrix = dataset.corr()
    for i in range(len(corr_matrix.columns)):
        for j in range(i):
            if abs(corr_matrix.iloc[i, j]) > threshold:  # we are interested in absolute coeff value
                colname = corr_matrix.columns[i]  # getting the name of column
                col_corr.add(colname)
    return col_corr


def Step_Forward_Feature_Selection(txt_path, result_path, flag) -> float:  # flag: True(seq:5), False(str:15)
    # load dataset
    # txt = np.loadtxt('../DataSet_all_cross_talk/DataSet1/Seq_set/test5.txt')
    if flag == 5:  # str
        datas = []
        with open(txt_path, 'r') as f1:
            for line in f1.readlines():
                print(line)
                if 'None' in line:
                    pass
                else:
                    # print(line.strip('\n').split(' '))
                    datas.append([float(item) for item in line.strip(' \n').split(' ')])
        txt = np.array(datas)
    else:
        txt = np.loadtxt(txt_path)
    data = pd.DataFrame(txt)
    # data = pd.read_csv('feature_str.csv')
    print(data.shape)
    # print(data.head())
    # In practice, feature selection should be done after data pre-processing,
    # so ideally, all the categorical variables are encoded into numbers,
    # and then you can assess how deterministic they are of the target

    # select numerical columns:

    # numerics = ['int16', 'int32', 'int64', 'float16', 'float32', 'float64']
    # numerical_vars = list(data.select_dtypes(include=numerics).columns)
    # data = data[numerical_vars]
    # print(data.shape)

    # separate train and test sets
    X_train, X_test, y_train, y_test = train_test_split(
        data.drop(labels=[0], axis=1),
        data[0],
        test_size=0.25,
        random_state=1)

    len_fea = X_train.shape[1]

    print(X_train.shape, X_test.shape)
    print(Counter(y_train), Counter(y_test))

    corr_features = correlation(X_train, 0.8)

    print('correlated features: ', len(set(corr_features)))

    # removed correlated  features
    X_train.drop(labels=corr_features, axis=1, inplace=True)
    X_test.drop(labels=corr_features, axis=1, inplace=True)

    # print(X_train.shape, X_test.shape)

    # step forward feature selection
    # Select 10 features based on optimal ROC_AUC scoring criteria

    sfs1 = SFS(RandomForestClassifier(n_jobs=4),
               k_features=flag,  # seq:5, str:15
               forward=True,
               floating=False,
               verbose=2,
               scoring='roc_auc',
               cv=3)

    sfs1 = sfs1.fit(np.array(X_train.fillna(0)), y_train)

    # print(sfs1.k_feature_idx_)
    selected_feat = X_train.columns[list(sfs1.k_feature_idx_)]
    print(list(selected_feat))

    pred = run_randomForests(X_train[selected_feat].fillna(0),
                             X_test[selected_feat].fillna(0),
                             y_train, y_test)

    with open(result_path, 'a') as f:
        f.write('feature:\t')
        for item in list(selected_feat):
            f.write(str(item) + '\t')
        f.write('auc: ' + str(roc_auc_score(y_test, pred[:, 1])) + '\n')


# seq_file_path = '../DataSet_all_cross_talk/DataSet2/Seq_set'
# str_file_path = '../DataSet_all_cross_talk/DataSet2/Str_set'
