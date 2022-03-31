import numpy as np
import tensorflow.keras.metrics as metrics
from imblearn.over_sampling import SMOTE
from keras import models
from keras import layers, Input
from keras import optimizers
from keras import activations
from cal.cal_metric import cal_two_class_metric, cal_two_class_roc
from Model.Generate_sample import read_samples_2d
from Model.Attention import attention_3d_block_v2


def Cnn_Lstm_attention_model(train_path, test_path, iter, epochs, batch_size, flag):
    train_data, train_label = read_samples_2d(train_path, flag)
    test_data, test_label = read_samples_2d(test_path, flag)
    if not flag:
        smo = SMOTE(random_state=30)
        train_data = np.squeeze(train_data, axis=1)
        train_data, train_label = smo.fit_resample(train_data, train_label)
        train_data = np.expand_dims(train_data, axis=1)
    input_x = Input(shape=(train_data.shape[1], train_data.shape[2]))
    for i in range(iter):
        x_1 = layers.Conv1D(200, 1, padding='same')(input_x)  # Output dimension 200, convolution kernel 1
        x_1 = layers.BatchNormalization()(x_1)
        x_1 = activations.relu(x_1)
        # x_1 = layers.MaxPooling1D(pool_size=1, strides=1)(x_1)
        # x_1 = layers.Conv1D(150, 7, padding='same')(x_1)
        # x_1 = layers.BatchNormalization()(x_1)
        # x_1 = activations.relu(x_1)
        # # x_1 = layers.MaxPooling1D(pool_size=2, strides=1)(x_1)
        # x_1 = layers.Conv1D(100, 25, padding='same')(x_1)
        # x_1 = layers.BatchNormalization()(x_1)
        # x_1 = activations.relu(x_1)
        # # x_1 = layers.MaxPooling1D(pool_size=2, strides=1)(x_1)
        # x_1 = layers.Conv1D(200, 30, padding='same')(x_1)
        # x_1 = layers.BatchNormalization()(x_1)
        # x_1 = activations.relu(x_1)
        # x_1 = layers.MaxPooling1D(pool_size=2, strides=1)(x_1)
        # x_1 = layers.Conv1D(100, 50, padding='same')(x_1)
        # x_1 = layers.BatchNormalization()(x_1)
        # x_1 = activations.relu(x_1)
        # x_1 = layers.MaxPooling1D(pool_size=2, strides=1)(x_1)
        # x = layers.Conv1D(180, 7, activation='relu', padding='same')(x)
        # x = layers.Flatten()(x_1)
        # out_x_1 = layers.GlobalMaxPooling1D()(x_1)
        out_x_1 = layers.GlobalAvgPool1D()(x_1)
        # out_x_1 = attention_3d_block_v2(x_1, mode='feature', SINGLE_ATTENTION_VECTOR=True)

        x_2 = layers.LSTM(300, return_sequences=True)(input_x)
        x_2 = layers.LSTM(200, return_sequences=True)(x_2)
        x_2 = layers.LSTM(100, return_sequences=True)(x_2)
        # x_2 = layers.LSTM(200, return_sequences=True)(x_2)
        # x_2 = layers.LSTM(150, return_sequences=True)(x_2)
        # out_x_2 = layers.LSTM(100)(x_2)     # (None, 100)
        out_x_2 = attention_3d_block_v2(x_2, mode='feature', SINGLE_ATTENTION_VECTOR=True)

        x = layers.concatenate([out_x_1, out_x_2], axis=-1)

        # x = layers.Dense(250, activation='relu')(x)
        # x = layers.Dropout(0.6)(x)
        x = layers.Dense(150, activation='relu')(x)
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


# Cnn_Lstm_attention_model('../DataSet/Seq_set/train11.txt', '../DataSet/Seq_set/test1.txt', 30, 30, 128)