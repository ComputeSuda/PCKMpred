import time

# from Model.Rf_model import Rf_model
from Model.Cnn_Lstm_model import Cnn_Lstm_model
from Model.Cnn_model import Cnn_model
from Model.Cnn_Lstm_attention_model import Cnn_Lstm_attention_model
from Model.Lstm_attention_model import Lstm_attention_model
from Model.Lstm_model import Lstm_model
from Model.Generate_sample import *
from Model.Cnn_attention_model import Cnn_attention_model

NoSeq_set_path = 'DataSet_all_mutation/Phos/NoSeq_set'
NoStr_set_path = 'DataSet_all_mutation/Phos/NoStr_set'
Seq_set_path = 'DataSet_all_mutation/Phos/Seq_set'
Str_set_path = 'DataSet_all_mutation/Phos/Str_set'


def get_result(model, seqpath, strpath, nums, outpath, iter, epochs, batchsize, flag_all):
    for num in range(nums):
        metric_result = {'accuracy': 0, 'precision': 0, 'sensitivity': 0, 'specificity': 0,
                         'true_positive_rate': 0, 'true_negative_rate': 0, 'false_positive_rate': 0,
                         'false_negative_rate': 0, 'f1_score': 0, 'auc': 0, 'matthews_correlation_coefficient': 0}
        # metric_roc = {'tpr': [], 'fpr': []}
        _, _, metric_seq, metric_seq_roc = model(seqpath + '/train' + str(num) + '.txt',
                                                 seqpath + '/test' + str(int(num/10)) + '.txt', iter, epochs, batchsize,
                                                 True)
        _, _, metric_str, metric_str_roc = model(strpath + '/train' + str(num) + '.txt',
                                                 strpath + '/test' + str(int(num/10)) + '.txt', iter, epochs, batchsize,
                                                 False)
        print(num, ': ', metric_seq)
        print(num, ': ', metric_str)

        def merge_dict(y, x):
            for k, v in x.items():
                if k in y.keys():
                    y[k] += v
                else:
                    y[k] = v

        merge_dict(metric_result, metric_str)
        merge_dict(metric_result, metric_seq)

        def write_result(outpath, metric_result, flag):
            with open(outpath, 'a') as f:
                f.write(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '\n')
                f.write('sample ' + str(num) + '\n')
                for key in metric_result.keys():
                    if flag:
                        f.write(key + ': ' + str(round(metric_result[key] / 2, 3)) + '\t')
                    else:
                        f.write(key + ': ' + str(round(metric_result[key], 3)) + '\t')
                f.write('\n')

        if flag_all:
            write_result(outpath + 'phos_mutation_all_result314-100_all.txt', metric_result, True)
            write_result(outpath + 'phos_mutation_all_result314-100_seq.txt', metric_seq, False)
            write_result(outpath + 'phos_mutation_all_result314-100_str.txt', metric_str, False)
        else:
            write_result(outpath + 'phos_mutation_NoAll_result314-100_all.txt', metric_result, True)
            write_result(outpath + 'phos_mutation_NoAll_result314-100_seq.txt', metric_seq, False)
            write_result(outpath + 'phos_mutation_NoAll_result314-100_str.txt', metric_str, False)


# get_result(Rf_model(), Seq_set_path, Str_set_path, 50, './Result/RF/mutation_all_result.txt', 5, 30, 64)
# get_result(Rf_model(), NoSeq_set_path, NoStr_set_path, 50, './Result/RF/mutation_NoAll_result.txt', 5, 30, 64)

# get_result(Cnn_model, Seq_set_path, Str_set_path, 50, './Result/Cnn/', 5, 30, 64, True)
# get_result(Cnn_model, NoSeq_set_path, NoStr_set_path, 50, './Result/Cnn/', 5, 30, 64, False)

# get_result(Cnn_attention_model, Seq_set_path, Str_set_path, 50, './Result/Cnn_attention/', 5, 30, 64, True)
# get_result(Cnn_attention_model, NoSeq_set_path, NoStr_set_path, 50, './Result/Cnn_attention/', 5, 30, 64, False)

# get_result(Lstm_model, Seq_set_path, Str_set_path, 50, './Result/Lstm/', 5, 30, 64, True)
# get_result(Lstm_model, NoSeq_set_path, NoStr_set_path, 50, './Result/Lstm/', 5, 30, 64, False)

# get_result(Cnn_Lstm_model, Seq_set_path, Str_set_path, 50, './Result/Cnn_lstm/', 5, 30, 64, True)
# get_result(Cnn_Lstm_model, NoSeq_set_path, NoStr_set_path, 50, './Result/Cnn_lstm/', 5, 30, 64, False)

# get_result(Lstm_attention_model, Seq_set_path, Str_set_path, 50, './Result/Lstm_attention/', 5, 30, 64, True)
# get_result(Lstm_attention_model, NoSeq_set_path, NoStr_set_path, 50, './Result/Lstm_attention/', 5, 30, 64, False)

# get_result(Cnn_Lstm_attention_model, Seq_set_path, Str_set_path, 50, './Result/Cnn_lstm_attention/', 5, 30, 64, True)
# get_result(Cnn_Lstm_attention_model, NoSeq_set_path, NoStr_set_path, 50, './Result/Cnn_lstm_attention/', 5, 30, 64, False)
