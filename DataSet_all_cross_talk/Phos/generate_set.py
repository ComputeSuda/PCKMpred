import random

import pandas as pd
import numpy as np

train_feature_file = 'Phos_all_dataset_features.xlsx'
test_feature_file = 'Phos_others_dataset_features.xlsx'

SeqSet = './Seq_set'
StrSet = './Str_set'
NoSeqSet = './NoSeq_set'
NoStrSet = './NoStr_set'


# 用于生成训练集以及测试集（txt文件）, train_nums训练集的数量, test_nums训练集的数量, data_nums一个数据集的大小。
def random_dataset(train_feature_filepath, test_feature_filepath, train_nums, test_nums, train_data_nums, test_data_nums):
    train_po_feature = pd.read_excel(train_feature_filepath, sheet_name='Positive_sel_features')
    train_ne_feature = pd.read_excel(train_feature_filepath, sheet_name='Negative_sel_features')
    test_po_feature = pd.read_excel(test_feature_filepath, sheet_name='Positive_sel_features')
    test_ne_feature = pd.read_excel(test_feature_filepath, sheet_name='Negative_sel_features')

    train_po_datas = train_po_feature.values.tolist()
    train_ne_datas = train_ne_feature.values.tolist()
    test_po_datas = test_po_feature.values.tolist()
    test_ne_datas = test_ne_feature.values.tolist()
    # positive_datas = datas[:205].tolist()
    # negative_datas = datas[205:].tolist()
    random.shuffle(train_po_datas)
    random.shuffle(train_ne_datas)
    random.shuffle(test_po_datas)
    random.shuffle(test_ne_datas)
    # print(positive_datas[-1])
    # print(negative_datas[0])
    train_po_nums = [item for item in range(0, len(train_po_datas))]
    train_ne_nums = [item for item in range(0, len(train_ne_datas))]
    test_po_nums = [item for item in range(0, len(test_po_datas))]
    test_ne_nums = [item for item in range(0, len(test_ne_datas))]

    def write_file(fileout_path, datas_list):
        with open(fileout_path, 'w') as f:
            for datas in datas_list:
                f.writelines([str(d) + ' ' for d in datas])
                f.write('\n')

    # dataSet需要使用到的数据, data_nums一个数据集中的数量, set_nums数据集的数量。
    def random_Set(positive_datas, negative_datas, data_nums, set_nums, flag):
        for set_num in range(set_nums):
            if flag:
                random_positive_nums = random.sample(train_po_nums, data_nums)
                random_negative_nums = random.sample(train_ne_nums, data_nums)
            else:
                random_positive_nums = random.sample(test_po_nums, data_nums)
                random_negative_nums = random.sample(test_ne_nums, data_nums)
            samples_Noseq = []
            samples_Nostr = []
            samples_seq = []
            samples_str = []
            for i in range(data_nums):
                samples_Noseq.append(
                    [positive_datas[random_positive_nums[i]][0]] + positive_datas[random_positive_nums[i]][2:11])
                samples_Noseq.append(
                    [negative_datas[random_positive_nums[i]][0]] + negative_datas[random_negative_nums[i]][2:11])
                samples_Nostr.append(
                    [positive_datas[random_positive_nums[i]][0]] + positive_datas[random_positive_nums[i]][12:])
                samples_Nostr.append(
                    [negative_datas[random_positive_nums[i]][0]] + negative_datas[random_negative_nums[i]][12:])
                samples_seq.append(positive_datas[random_positive_nums[i]][:11])
                samples_seq.append(negative_datas[random_negative_nums[i]][:11])
                samples_str.append(
                    [positive_datas[random_positive_nums[i]][0]] + positive_datas[random_positive_nums[i]][11:])
                samples_str.append(
                    [negative_datas[random_positive_nums[i]][0]] + negative_datas[random_negative_nums[i]][11:])
            if flag:
                write_file(NoSeqSet + '/train' + str(set_num) + '.txt', samples_Noseq)
                write_file(NoStrSet + '/train' + str(set_num) + '.txt', samples_Nostr)
                write_file(SeqSet + '/train' + str(set_num) + '.txt', samples_seq)
                write_file(StrSet + '/train' + str(set_num) + '.txt', samples_str)
            else:
                write_file(NoSeqSet + '/test' + str(set_num) + '.txt', samples_Noseq)
                write_file(NoStrSet + '/test' + str(set_num) + '.txt', samples_Nostr)
                write_file(SeqSet + '/test' + str(set_num) + '.txt', samples_seq)
                write_file(StrSet + '/test' + str(set_num) + '.txt', samples_str)

    random_Set(train_po_datas, train_ne_datas, train_data_nums, train_nums, True)
    random_Set(test_po_datas, test_ne_datas, test_data_nums, test_nums, False)


if __name__ == '__main__':
    random_dataset(train_feature_file, test_feature_file, train_nums=50, test_nums=5, train_data_nums=70, test_data_nums=70)
