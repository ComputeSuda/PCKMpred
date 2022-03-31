import xlrd
import xlwt

PTM_Name = {'p': 'Phosphorylation', 'ac': 'Acetylation', 'm': 'Methylation', 'ga': 'O-GalNAc',
            'ub': 'Ubiquitination', 'sm': 'Sumoylation', 'gl': 'O-GlcNAc', 'pa': 'Palmitoylation',
            'ng': 'N-linkedGlycosylation', 'sc': 'Succinylation'}

# supply_dataset_file_path = '../Ptm-site/Supply.xlsx'
#
# supply_dataset_workbook = xlrd.open_workbook(supply_dataset_file_path)
# supply_dataset_workbook_sheet = supply_dataset_workbook.sheet_by_name('Sheet1')
# ptm_sites_list = supply_dataset_workbook_sheet.col_values(2)
# print(len(ptm_sites_list))
# ptm_sites_type_list = []
#
# for ptm_site in ptm_sites_list:
#     name = ptm_site.split('-')[1]
#     if name[0] == 'm':
#         name = 'm'
#     ptm_sites_type_list.append((ptm_site, PTM_Name[name]))
#
# work_book = xlwt.Workbook(encoding='utf-8')
# sheet = work_book.add_sheet('Sheet1')
# len_dic = len(ptm_sites_type_list)
# c = 0
# for items in ptm_sites_type_list:
#     sheet.write(c, 0, items[0])
#     sheet.write(c, 1, items[1])
#     c += 1
#
# work_book.save('./ptm_site_name.xlsx')

Ptm_site_all_file_path = './Ptm_site_all.xlsx'
UniprotId_all_file_path = '../Uniprot/uniprotId_all.txt'

Ptm_site_Ltp_file_path = './PTM_LTP.xlsx'

with open(UniprotId_all_file_path, 'r') as f1:
    uniprotIds = [item.strip('\n') for item in f1.readlines()]

print(len(uniprotIds))
Ptm_site_workbook = xlrd.open_workbook(Ptm_site_Ltp_file_path)
# print(Ptm_site_workbook.sheet_names())
ptm_site_workbook_sheet = Ptm_site_workbook.sheet_by_name('Sheet1')

ptm_site_cols = ptm_site_workbook_sheet.ncols
ptm_site_rows = ptm_site_workbook_sheet.nrows

uniprotId_sites_all_dic = dict()

# for uniprotId in uniprotIds:
#     uniprotId_sites_all_dic[uniprotId] = set()

for row in range(1, ptm_site_rows):
    protein_name = ptm_site_workbook_sheet.row_values(row)[0]
    uniprotId = ptm_site_workbook_sheet.row_values(row)[1]
    # print(uniprotId)
    site = ptm_site_workbook_sheet.row_values(row)[2]
    ptm_type = ptm_site_workbook_sheet.row_values(row)[3]
    if uniprotId in uniprotIds:
        if (protein_name, uniprotId) not in uniprotId_sites_all_dic.keys():
            uniprotId_sites_all_dic[(protein_name, uniprotId)] = set()
        uniprotId_sites_all_dic[(protein_name, uniprotId)].add((site.split('-')[0], ptm_type))

print(len(uniprotId_sites_all_dic.keys()))
uniprotId_site_all = [item[1] for item in uniprotId_sites_all_dic.keys()]
for uniprotId in uniprotIds:
    if uniprotId not in uniprotId_site_all:
        print(uniprotId)
# with open('./uniprotId_sites_Ltp.txt', 'w') as f2:
#     for key, values in uniprotId_sites_all_dic.items():
#         f2.write(str(key)+':\t')
#         for value in values:
#             f2.write(str(value)+'\t')
#         else:
#             f2.write('\n')
#
# uniprot_ptm_sites_cross_list = []
#
# import itertools
#
#
# for key, values in uniprotId_sites_all_dic.items():
#     # print(values)
#     print(key)
#     for item in itertools.combinations(values, 2):
#         with open('./neagtive_Ltp.txt', 'a') as f3:
#             f3.write(key[0]+'\t'+key[1]+'\t'+item[0][0]+'\t'+item[0][1]+'\t'+item[1][0]+'\t'+item[1][1]+'\n')
