import time

from Model.Knn_model import Knn_model
from Model.Rf_model import Rf_model
from Model.Svm_model import Svm_model

NoSeq_set_path = 'DataSet_all_cross_talk/Phos/NoSeq_set'
NoStr_set_path = 'DataSet_all_cross_talk/Phos/NoStr_set'
Seq_set_path = 'DataSet_all_cross_talk/Phos/Seq_set'
Str_set_path = 'DataSet_all_cross_talk/Phos/Str_set'


def get_result(model, seqpath, strpath, nums, outpath, flag_all):
    for num in range(nums):
        metric_result = {'accuracy': 0, 'precision': 0, 'sensitivity': 0, 'specificity': 0,
                         'true_positive_rate': 0, 'true_negative_rate': 0, 'false_positive_rate': 0,
                         'false_negative_rate': 0, 'f1_score': 0, 'auc': 0, 'matthews_correlation_coefficient': 0}
        # metric_roc = {'fpr': [], 'tpr': []}
        _, _, metric_seq, metric_seq_roc = model(seqpath + '/train' + str(num) + '.txt', seqpath + '/test' + str(int(num/10)) + '.txt', True)
        _, _, metric_str, metric_str_roc = model(strpath + '/train' + str(num) + '.txt', strpath + '/test' + str(int(num/10)) + '.txt', False)
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
            write_result(outpath + 'phos_cross_talk_all_result314-100_all.txt', metric_result, True)
            write_result(outpath + 'phos_cross_talk_all_result314-100_seq.txt', metric_seq, False)
            write_result(outpath + 'phos_cross_talk_all_result314-100_str.txt', metric_str, False)
        else:
            write_result(outpath + 'phos_cross_talk_NoAll_result314-100_all.txt', metric_result, True)
            write_result(outpath + 'phos_cross_talk_NoAll_result314-100_seq.txt', metric_seq, False)
            write_result(outpath + 'phos_cross_talk_NoAll_result314-100_str.txt', metric_str, False)


# get_result(Rf_model, Seq_set_path, Str_set_path, 50, './Result/RF/', True)
# get_result(Rf_model, NoSeq_set_path, NoStr_set_path, 50, './Result/RF/', False)
#
# get_result(Svm_model, Seq_set_path, Str_set_path, 50, './Result/SVM/', True)
# get_result(Svm_model, NoSeq_set_path, NoStr_set_path, 50, './Result/SVM/', False)
#
# get_result(Knn_model, Seq_set_path, Str_set_path, 50, './Result/KNN/', True)
# get_result(Knn_model, NoSeq_set_path, NoStr_set_path, 50, './Result/KNN/', False)
