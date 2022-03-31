import time

result_path = './Result/'

rf_result = 'RF'
cnn_result = 'Cnn'
lstm_result = 'Lstm'
cnn_lstm_result = 'Cnn_lstm'
lstm_attention_result = 'Lstm_attention'
cnn_lstm_attention_result = 'Cnn_lstm_attention'
cnn_attention_result = 'Cnn_attention'
knn_result = 'KNN'
svm_result = 'SVM'


def get_result(path, outpath):
    metric_result_all = {'accuracy': 0, 'auc': 0, 'precision': 0, 'sensitivity': 0, 'specificity': 0,
                         'true_positive_rate': 0, 'true_negative_rate': 0, 'false_positive_rate': 0,
                         'false_negative_rate': 0, 'f1_score': 0, 'matthews_correlation_coefficient': 0}
    metric_result_no_all = {'accuracy': 0, 'auc': 0, 'precision': 0, 'sensitivity': 0, 'specificity': 0,
                            'true_positive_rate': 0, 'true_negative_rate': 0, 'false_positive_rate': 0,
                            'false_negative_rate': 0, 'f1_score': 0, 'matthews_correlation_coefficient': 0}
    metric_result_seq = {'accuracy': 0, 'auc': 0, 'precision': 0, 'sensitivity': 0, 'specificity': 0,
                         'true_positive_rate': 0, 'true_negative_rate': 0, 'false_positive_rate': 0,
                         'false_negative_rate': 0, 'f1_score': 0, 'matthews_correlation_coefficient': 0}
    metric_result_str = {'accuracy': 0, 'auc': 0, 'precision': 0, 'sensitivity': 0, 'specificity': 0,
                         'true_positive_rate': 0, 'true_negative_rate': 0, 'false_positive_rate': 0,
                         'false_negative_rate': 0, 'f1_score': 0, 'matthews_correlation_coefficient': 0}
    metric_result_no_seq = {'accuracy': 0, 'auc': 0, 'precision': 0, 'sensitivity': 0, 'specificity': 0,
                            'true_positive_rate': 0, 'true_negative_rate': 0, 'false_positive_rate': 0,
                            'false_negative_rate': 0, 'f1_score': 0, 'matthews_correlation_coefficient': 0}
    metric_result_no_str = {'accuracy': 0, 'auc': 0, 'precision': 0, 'sensitivity': 0, 'specificity': 0,
                            'true_positive_rate': 0, 'true_negative_rate': 0, 'false_positive_rate': 0,
                            'false_negative_rate': 0, 'f1_score': 0, 'matthews_correlation_coefficient': 0}

    def read_result(file_path, metric_result):
        with open(file_path, 'r') as f1:
            lines = [item.strip('\t\n') for item in f1.readlines()]
            for line in lines:
                if line.startswith('accuracy'):
                    items = line.split('\t')
                    for item in items:
                        # print(item.split(': '))
                        metric_result[item.split(': ')[0]] += float(item.split(': ')[1])

    read_result(path + '/phos_mutation_all_result314-100_all.txt', metric_result_all)
    read_result(path + '/phos_mutation_NoAll_result314-100_all.txt', metric_result_no_all)
    read_result(path + '/phos_mutation_all_result314-100_seq.txt', metric_result_seq)
    read_result(path + '/phos_mutation_NoAll_result314-100_seq.txt', metric_result_no_seq)
    read_result(path + '/phos_mutation_all_result314-100_str.txt', metric_result_str)
    read_result(path + '/phos_mutation_NoAll_result314-100_str.txt', metric_result_no_str)

    def write_result(write_name, metric_result_all):
        for key in metric_result_all.keys():
            metric_result_all[key] = metric_result_all[key] / 50
        print(metric_result_all)

        with open(outpath, 'a') as f:
            f.write(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '\n')
            f.write(write_name + '\n')
            for key in metric_result_all.keys():
                f.write(key + ': ' + str(round(metric_result_all[key], 3)) + '\t')
            f.write('\n')

    write_result('phos_mutation_all_result314-100_all: ', metric_result_all)
    write_result('phos_mutation_NoAll_result314-100_all: ', metric_result_no_all)
    write_result('phos_mutation_all_result314-100_seq: ', metric_result_seq)
    write_result('phos_mutation_NoAll_result314-100_seq: ', metric_result_no_seq)
    write_result('phos_mutation_all_result314-100_str: ', metric_result_str)
    write_result('phos_mutation_NoAll_result314-100_str: ', metric_result_no_str)


get_result(result_path + rf_result, './Final_result/mutation/Rf.txt')
get_result(result_path + svm_result, './Final_result/mutation/Svm.txt')
get_result(result_path + knn_result, './Final_result/mutation/Knn.txt')
get_result(result_path + cnn_attention_result, './Final_result/mutation/Cnn_attention.txt')
get_result(result_path + cnn_result, './Final_result/mutation/Cnn.txt')
get_result(result_path + lstm_result, './Final_result/mutation/Lstm.txt')
get_result(result_path + cnn_lstm_result, './Final_result/mutation/Cnn_lstm.txt')
get_result(result_path + lstm_attention_result, './Final_result/mutation/Lstm_attention.txt')
get_result(result_path + cnn_lstm_attention_result, './Final_result/mutation/Cnn_lstm_attention.txt')
