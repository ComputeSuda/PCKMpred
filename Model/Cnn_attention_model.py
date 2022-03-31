from collections import Counter

import tensorflow.keras.metrics as metrics
from imblearn.over_sampling import SMOTE
from keras import models, activations
from keras import layers, Input
from keras import optimizers
import numpy as np
from sklearn.model_selection import train_test_split

# from EGSmote.egsmote import EGSmote
from cal.cal_metric import cal_two_class_metric, cal_two_class_roc
from Model.Attention import attention_3d_block_v2
from Model.Generate_sample import read_samples_2d


def Cnn_attention_model(train_path, test_path, iter, epochs, batch_size, flag):
    train_data, train_label = read_samples_2d(train_path, flag)
    test_data, test_label = read_samples_2d(test_path, flag)
    # train_data, test_data, train_label,  = SMOTE(random_state=30)test_label = train_test_split(train_data)
    if not flag:
        smo = SMOTE(random_state=30)
        train_data = np.squeeze(train_data, axis=1)
        train_data, train_label = smo.fit_resample(train_data, train_label)
        train_data = np.expand_dims(train_data, axis=1)
    # if not flag:
    #     egsmote = EGSmote(sampling_rate=0.25)
    #     train_data = np.squeeze(train_data, axis=1)
    #     train_data, train_label = egsmote.fit_resample(train_data, train_label)
    #     train_data = np.expand_dims(train_data, axis=1)
    print(train_data.shape, Counter(train_label))
    input_x = Input(shape=(train_data.shape[1], train_data.shape[2]))
    for i in range(iter):
        x = layers.Conv1D(300, 1, padding='same')(input_x)  # Output dimension 200, convolution kernel 1
        x = layers.BatchNormalization()(x)
        x = activations.relu(x)
        out_x = attention_3d_block_v2(x, mode='feature', SINGLE_ATTENTION_VECTOR=True)

        # x = layers.Dense(250, activation='relu')(x)
        # x = layers.Dropout(0.6)(x)
        x = layers.Dense(150, activation='relu')(out_x)
        # x = layers.Dropout(0.5)(x)
        x = layers.Dense(100, activation='relu')(x)
        # x = layers.Dropout(0.5)(x)
        x = layers.Dense(64, activation='relu')(x)
        # x = layers.Dropout(0.5)(x)
        # x = layers.Dense(10, activation='relu')(x)
        out_x = layers.Dense(1, activation='sigmoid')(x)

        model = models.Model(input_x, out_x)
        model.compile(optimizer=optimizers.RMSprop(lr=0.001), loss='binary_crossentropy',
                      metrics=['acc', metrics.SensitivityAtSpecificity(0.5), metrics.SpecificityAtSensitivity(0.5),
                               metrics.AUC()])
        print(model.summary())
        for j in range(1):
            # for new_data, new_label in generate_two_data(train_data, train_label):
            # new_data, new_label = get_two_class_data(train_data, train_label)  # 得到新样本
            new_data, new_label = train_data, train_label
            # print('data shape:', new_data.shape)
            history = model.fit(new_data, new_label, epochs=epochs, batch_size=batch_size, verbose=1)
            history = history.history
        if i == 0:
            pred_prob = model.predict(test_data)
        else:
            pred_prob += model.predict(test_data)
    pred_prob /= iter
    # print(pred_prob.reshape(-1)[:20])
    matrix, metric = cal_two_class_metric(test_label, pred_prob)
    #  roc
    metric_roc = cal_two_class_roc(test_label, pred_prob)
    print(matrix)
    print(metric)
    return pred_prob, matrix, metric, metric_roc


# Cnn_attention_model('../DataSet_all_cross_talk/DataSet4-100/Str_set/train1.txt', '../DataSet_all_cross_talk/DataSet4-100/Str_set/test0.txt', 5, 30, 128, False)
