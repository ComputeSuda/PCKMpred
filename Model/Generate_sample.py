import numpy as np
import pandas as pd


# Read the sample data to generate a one-dimensional numpy array for training and testing. flag:True(seq), False(str)
def read_samples_1d(filepath, flag):
    features_data_1d = []
    features_label_1d = []
    seq = [0, 1, 2, 7, 8, 9, 12, 14, 16, 17, 18, 19, 22, 26, 34, 35, 41, 42, 43, 44, 46, 47, 51, 54, 55, 57, 59, 60, 63, 64, 65]
    str = [0, 1, 2, 5, 8, 11]
    with open(filepath, 'r') as f:
        datas = f.readlines()
        for data in datas:
            datas_sel = []
            # print(data)
            data = data.strip(' \n').split(' ')
            # print(data)
            # if flag:
            #     for i in seq:
            #         datas_sel.append(data[i])
            # else:
            #     for i in str:
            #         datas_sel.append(data[i])
            datas_sel = data
            if data[1] != 'None':
                data_items = [float(item) for item in datas_sel]
                features_data_1d.append(data_items[1:])
                features_label_1d.append(int(data_items[0]))
    return np.array(features_data_1d), np.array(features_label_1d)


# Read the sample data to generate a two-dimensional numpy array for training and testing. flag: True(seq), False(str)
def read_samples_2d(filepath, flag):
    features_data_2d = []
    features_label_2d = []
    seq = [0, 1, 2, 7, 8, 9, 12, 14, 16, 17, 18, 19, 22, 26, 34, 35, 41, 42, 43, 44, 46, 47, 51, 54, 55, 57, 59, 60, 63,
           64, 65]
    str = [0, 1, 2, 5, 8, 11]
    datas = pd.read_csv(filepath)
    with open(filepath, 'r') as f:
        datas = f.readlines()
        for data in datas:
            datas_sel = []
            data = data.strip(' \n').split(' ')
            # print(data)
            # if flag:
            #     for i in seq:
            #         datas_sel.append(data[i])
            # else:
            #     for i in str:
            #         datas_sel.append(data[i])
            datas_sel = data
            if data[1] != 'None':
                data_items = [float(item) for item in datas_sel]
                features_data_2d.append([data_items[1:]])
                features_label_2d.append(data_items[0])
    return np.array(features_data_2d), np.array(features_label_2d)


def read_samples_csv(filepath, flag):
    features_data_2d = []
    features_label_2d = []
    # seq = [0, 1, 2, 3, 5, 8]
    # str = [0, 1, 2, 5, 8, 11]
    with open(filepath, 'r') as f:
        datas = f.readlines()
        for data in datas:
            # print(data)
            datas_sel = []
            data = data.lstrip('[')
            # print(data)
            data = data.strip('"[\n').split('",')
            # print(len(data))
            items = data[0].split(', ')
            # print(items)
            features_data_2d.append([items])
            features_label_2d.append(int(float(data[1])))
    return np.array(features_data_2d), np.array(features_label_2d)


# read_samples_csv('../Model/train3.csv', True)
