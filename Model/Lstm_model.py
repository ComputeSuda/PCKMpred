import tensorflow.keras.metrics as metrics
from imblearn.over_sampling import SMOTE
from keras import models
from keras import layers, Input
from keras import optimizers
import numpy as np
from cal.cal_metric import cal_two_class_metric, cal_two_class_roc
from Model.Attention import attention_3d_block_v2
from Model.Generate_sample import read_samples_2d


def Lstm_model(train_path, test_path, iter, epochs, batch_size, flag):
    train_data, train_label = read_samples_2d(train_path, flag)
    test_data, test_label = read_samples_2d(test_path, flag)
    if not flag:
        smo = SMOTE(random_state=30)
        train_data = np.squeeze(train_data, axis=1)
        train_data, train_label = smo.fit_resample(train_data, train_label)
        train_data = np.expand_dims(train_data, axis=1)
    input_x = Input(shape=(train_data.shape[1], train_data.shape[2]))
    for i in range(iter):
        x = layers.LSTM(300, return_sequences=True)(input_x)
        x = layers.LSTM(200, return_sequences=True)(x)
        x = layers.LSTM(100, return_sequences=True)(x)
        # x = layers.LSTM(200, return_sequences=True)(x)
        # x = layers.LSTM(150, return_sequences=True)(x)
        out_x = layers.LSTM(100)(x)  # (None, 100)
        # out_x = attention_3d_block_v2(x, mode='feature', SINGLE_ATTENTION_VECTOR=True)
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
            print('data shape:', new_data.shape)
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


# Lstm_model('../DataSet/Seq_set/train11.txt', '../DataSet/Seq_set/test1.txt', 30, 30, 128)