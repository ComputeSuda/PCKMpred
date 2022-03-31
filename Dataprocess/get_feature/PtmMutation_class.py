import os


class PtmMutation:
    def __init__(self, Id, Pdb, Chain, UniprotId, PtmPdbPosition, PtmPdbPositionAbsolute, PtmUniprotPosition,
                 MutationPdbPosition, MutationPdbPositionAbsolute, MutationUniprotPosition, *items):
        self.Id = Id
        self.Pdb = Pdb
        self.Chain = Chain
        self.UniprotId = UniprotId
        self.PtmPdbPosition = PtmPdbPosition
        self.PtmPdbPositionAbsolute = PtmPdbPositionAbsolute
        self.PtmUniprotPosition = PtmUniprotPosition
        self.MutationPdbPosition = MutationPdbPosition
        self.MutationPdbPositionAbsolute = MutationPdbPositionAbsolute
        self.MutationUniprotPosition = MutationUniprotPosition
        self.items = items  # 其他信息
        self.ptm_pdbchain_feature = {}
        self.ptm_uniprot_feature = {}
        self.mutation_pdbchain_feature = {}
        self.mutation_uniprot_feature = {}
        self.features = []

    '''
    Str and Dyn features
    pdbchain_files(extract features by pdb, chain, pdbpositionabsolute):
    cij(betweenness, clossness, degree, cluster, diversity, eccentricity, strength, eigen_centrality, page_rank)
    anm_cancer_cc(5_per, 5_per_20_per, 20_per_50_per, greater_60_per, top3)
    anm_cancer_prs(effectiveness, prs, sensitivity)
    anm_cancer_sq(sq)
    anm_cancer_stiffness(stiffness)
    gnm_cancer_cc(5_per, 5_per_20_per, 20_per_50_per, greater_60_per, top3)
    gnm_cancer_eigenvector(eigenvector_20, eigenvector_all, eigenvector_top3)
    gnm_cancer_prs(effectiveness, prs, sensitivity)
    gnm_cancer_sq(sq)
    '''

    def pdbchain_feature_cij(self, pdbchain_cij_path):
        # features = ['betweenness', 'clossness', 'degree', 'cluster', 'diversity', 'eccentricity', 'strength','eigen_centrality', 'page_rank']
        files = os.listdir(pdbchain_cij_path)
        pdbChain = self.Pdb + '_' + self.Chain
        pdbChain_files = []
        for file in files:
            if pdbChain in file:
                pdbChain_files.append(file)
        for pdbChain_file in sorted(pdbChain_files):
            print(pdbChain_file)
            with open(pdbchain_cij_path + '\\' + pdbChain_file, 'r') as f:
                datas = f.readlines()
                feature_name = '_'.join(pdbChain_file.split('_')[2:3]) + '_cij'
                self.ptm_pdbchain_feature[feature_name] = datas[self.PtmPdbPositionAbsolute - 1].strip('\n').split(':')[
                    1]
                self.mutation_pdbchain_feature[feature_name] = \
                    datas[self.MutationPdbPositionAbsolute - 1].strip('\n').split(':')[1]
                if self.ptm_pdbchain_feature[feature_name] == 'NA' and self.mutation_pdbchain_feature[
                    feature_name] != 'NA':
                    self.features.append(0)
                    self.features.append(self.mutation_pdbchain_feature[feature_name])
                    self.features.append(float(self.mutation_pdbchain_feature[feature_name]) / 2)
                elif self.ptm_pdbchain_feature[feature_name] != 'NA' and self.mutation_pdbchain_feature[
                    feature_name] == 'NA':
                    self.features.append(0)
                    self.features.append(self.ptm_pdbchain_feature[feature_name])
                    self.features.append(float(self.ptm_pdbchain_feature[feature_name]) / 2)
                elif self.ptm_pdbchain_feature[feature_name] == 'NA' and self.mutation_pdbchain_feature[
                    feature_name] == 'NA':
                    self.features.append(0)
                    self.features.append(0)
                    self.features.append(0)
                else:
                    self.features.append(
                        min(self.ptm_pdbchain_feature[feature_name], self.mutation_pdbchain_feature[feature_name]))
                    self.features.append(
                        max(self.ptm_pdbchain_feature[feature_name], self.mutation_pdbchain_feature[feature_name]))
                    self.features.append((float(self.ptm_pdbchain_feature[feature_name]) + float(
                        self.mutation_pdbchain_feature[feature_name])) / 2)

    def pdbchain_feature_anm_cc(self, anm_cc_path):
        files = os.listdir(anm_cc_path)
        pdbChain = self.Pdb + '_' + self.Chain
        pdbChain_files = []
        for file in files:
            if pdbChain == file[:6]:
                pdbChain_files.append(file)
        for pdbChain_file in sorted(pdbChain_files):
            print(pdbChain_file)
            with open(anm_cc_path + '\\' + pdbChain_file, 'r') as f:
                datas = f.readlines()
                # feature_name = pdbChain_file.split('.')[0][7:]
                try:
                    self.features.append(
                        datas[self.PtmPdbPositionAbsolute - 1].strip('\n').split(':')[1].strip('[]').split(',')
                        [self.MutationPdbPositionAbsolute - 1].strip())
                except:
                    self.features.append('null')

    def pdbchain_feature_anm_prs(self, anm_prs_path):
        files = os.listdir(anm_prs_path)
        pdbChain = self.Pdb + '_' + self.Chain
        pdbChain_files = []
        for file in files:
            if pdbChain == file[:6]:
                pdbChain_files.append(file)
        for pdbChain_file in sorted(pdbChain_files):
            print(pdbChain_file)
            if 'prs' in pdbChain_file:
                with open(anm_prs_path + '\\' + pdbChain_file, 'r') as f:
                    datas = f.readlines()
                    feature_name = pdbChain_file.split('.')[0][7:]
                    try:
                        self.features.append(
                            datas[self.PtmPdbPositionAbsolute - 1].strip('\n').split(':')[1].strip('[]').split(',')
                            [self.MutationPdbPositionAbsolute - 1].strip())
                    except:
                        self.features.append('null')
            elif 'effectiveness' in pdbChain_file:
                with open(anm_prs_path + '\\' + pdbChain_file, 'r') as f:
                    datas = f.readlines()
                    feature_name = pdbChain_file.split('.')[0][7:]
                    self.ptm_pdbchain_feature[feature_name] = \
                        datas[self.PtmPdbPositionAbsolute - 1].strip('\n').split(':')[1]
                    self.mutation_pdbchain_feature[feature_name] = \
                        datas[self.MutationPdbPositionAbsolute - 1].strip('\n').split(':')[1]
                    if self.ptm_pdbchain_feature[feature_name] == 'NA' and self.mutation_pdbchain_feature[
                        feature_name] != 'NA':
                        self.features.append(0)
                        self.features.append(self.mutation_pdbchain_feature[feature_name])
                        self.features.append(float(self.mutation_pdbchain_feature[feature_name]) / 2)
                    elif self.ptm_pdbchain_feature[feature_name] != 'NA' and self.mutation_pdbchain_feature[
                        feature_name] == 'NA':
                        self.features.append(0)
                        self.features.append(self.ptm_pdbchain_feature[feature_name])
                        self.features.append(float(self.ptm_pdbchain_feature[feature_name]) / 2)
                    elif self.ptm_pdbchain_feature[feature_name] == 'NA' and self.mutation_pdbchain_feature[
                        feature_name] == 'NA':
                        self.features.append(0)
                        self.features.append(0)
                        self.features.append(0)
                    else:
                        self.features.append(
                            min(self.ptm_pdbchain_feature[feature_name], self.mutation_pdbchain_feature[feature_name]))
                        self.features.append(
                            max(self.ptm_pdbchain_feature[feature_name], self.mutation_pdbchain_feature[feature_name]))
                        self.features.append((float(self.ptm_pdbchain_feature[feature_name]) + float(
                            self.mutation_pdbchain_feature[feature_name])) / 2)
            elif 'sensitivity' in pdbChain_file:
                with open(anm_prs_path + '\\' + pdbChain_file, 'r') as f:
                    datas = f.readlines()
                    feature_name = pdbChain_file.split('.')[0][7:]
                    self.ptm_pdbchain_feature[feature_name] = \
                        datas[self.PtmPdbPositionAbsolute - 1].strip('\n').split(':')[1]
                    self.mutation_pdbchain_feature[feature_name] = \
                        datas[self.MutationPdbPositionAbsolute - 1].strip('\n').split(':')[1]
                    if self.ptm_pdbchain_feature[feature_name] == 'NA' and self.mutation_pdbchain_feature[
                        feature_name] != 'NA':
                        self.features.append(0)
                        self.features.append(self.mutation_pdbchain_feature[feature_name])
                        self.features.append(float(self.mutation_pdbchain_feature[feature_name]) / 2)
                    elif self.ptm_pdbchain_feature[feature_name] != 'NA' and self.mutation_pdbchain_feature[
                        feature_name] == 'NA':
                        self.features.append(0)
                        self.features.append(self.ptm_pdbchain_feature[feature_name])
                        self.features.append(float(self.ptm_pdbchain_feature[feature_name]) / 2)
                    elif self.ptm_pdbchain_feature[feature_name] == 'NA' and self.mutation_pdbchain_feature[
                        feature_name] == 'NA':
                        self.features.append(0)
                        self.features.append(0)
                        self.features.append(0)
                    else:
                        self.features.append(
                            min(self.ptm_pdbchain_feature[feature_name], self.mutation_pdbchain_feature[feature_name]))
                        self.features.append(
                            max(self.ptm_pdbchain_feature[feature_name], self.mutation_pdbchain_feature[feature_name]))
                        self.features.append((float(self.ptm_pdbchain_feature[feature_name]) + float(
                            self.mutation_pdbchain_feature[feature_name])) / 2)

    def pdbchain_feature_anm_sq(self, anm_sq_path):
        files = os.listdir(anm_sq_path)
        pdbChain = self.Pdb + '_' + self.Chain
        pdbChain_files = []
        for file in files:
            if pdbChain == file[:6]:
                pdbChain_files.append(file)
        for pdbChain_file in sorted(pdbChain_files):
            print(pdbChain_file)
            with open(anm_sq_path + '\\' + pdbChain_file, 'r') as f:
                datas = f.readlines()
                feature_name = pdbChain_file.split('.')[0][7:]
                self.ptm_pdbchain_feature[feature_name] = datas[self.PtmPdbPositionAbsolute - 1].strip('\n').split(':')[
                    1]
                self.mutation_pdbchain_feature[feature_name] = \
                    datas[self.MutationPdbPositionAbsolute - 1].strip('\n').split(':')[1]
                if self.ptm_pdbchain_feature[feature_name] == 'NA' and self.mutation_pdbchain_feature[
                    feature_name] != 'NA':
                    self.features.append(0)
                    self.features.append(self.mutation_pdbchain_feature[feature_name])
                    self.features.append(float(self.mutation_pdbchain_feature[feature_name]) / 2)
                elif self.ptm_pdbchain_feature[feature_name] != 'NA' and self.mutation_pdbchain_feature[
                    feature_name] == 'NA':
                    self.features.append(0)
                    self.features.append(self.ptm_pdbchain_feature[feature_name])
                    self.features.append(float(self.ptm_pdbchain_feature[feature_name]) / 2)
                elif self.ptm_pdbchain_feature[feature_name] == 'NA' and self.mutation_pdbchain_feature[
                    feature_name] == 'NA':
                    self.features.append(0)
                    self.features.append(0)
                    self.features.append(0)
                else:
                    self.features.append(
                        min(self.ptm_pdbchain_feature[feature_name], self.mutation_pdbchain_feature[feature_name]))
                    self.features.append(
                        max(self.ptm_pdbchain_feature[feature_name], self.mutation_pdbchain_feature[feature_name]))
                    self.features.append((float(self.ptm_pdbchain_feature[feature_name]) + float(
                        self.mutation_pdbchain_feature[feature_name])) / 2)

    def pdbchain_feature_anm_stiffness(self, anm_stiffness_path):
        files = os.listdir(anm_stiffness_path)
        pdbChain = self.Pdb + '_' + self.Chain
        pdbChain_files = []
        for file in files:
            if pdbChain == file[:6]:
                pdbChain_files.append(file)
        for pdbChain_file in sorted(pdbChain_files):
            print(pdbChain_file)
            with open(anm_stiffness_path + '\\' + pdbChain_file, 'r') as f:
                datas = f.readlines()
                feature_name = pdbChain_file.split('.')[0][7:]
                try:
                    self.features.append(
                        datas[self.PtmPdbPositionAbsolute - 1].strip('\n').split(':')[1].strip('[]').split(',')
                        [self.MutationPdbPositionAbsolute - 1].strip())
                except:
                    self.features.append('null')

    def pdbchain_feature_gnm_cc(self, gnm_cc_path):
        files = os.listdir(gnm_cc_path)
        pdbChain = self.Pdb + '_' + self.Chain
        pdbChain_files = []
        for file in files:
            if pdbChain == file[:6]:
                pdbChain_files.append(file)
        for pdbChain_file in sorted(pdbChain_files):
            print(pdbChain_file)
            with open(gnm_cc_path + '\\' + pdbChain_file, 'r') as f:
                datas = f.readlines()
                feature_name = pdbChain_file.split('.')[0][7:]
                try:
                    self.features.append(
                        datas[self.PtmPdbPositionAbsolute - 1].strip('\n').split(':')[1].strip('[]').split(',')
                        [self.MutationPdbPositionAbsolute - 1].strip())
                except:
                    self.features.append('null')

    def pdbchain_feature_gnm_eigenvector(self, gnm_eigenvector_path):
        files = os.listdir(gnm_eigenvector_path)
        pdbChain = self.Pdb + '_' + self.Chain
        pdbChain_files = []
        for file in files:
            if pdbChain == file[:6]:
                pdbChain_files.append(file)
        for pdbChain_file in sorted(pdbChain_files):
            print(pdbChain_file)
            with open(gnm_eigenvector_path + '\\' + pdbChain_file, 'r') as f:
                datas = f.readlines()
                feature_name = pdbChain_file.split('.')[0][7:]
                self.ptm_pdbchain_feature[feature_name] = datas[self.PtmPdbPositionAbsolute - 1].strip('\n').split(':')[
                    1]
                self.mutation_pdbchain_feature[feature_name] = \
                    datas[self.MutationPdbPositionAbsolute - 1].strip('\n').split(':')[1]
                if self.ptm_pdbchain_feature[feature_name] == 'NA' and self.mutation_pdbchain_feature[
                    feature_name] != 'NA':
                    self.features.append(0)
                    self.features.append(self.mutation_pdbchain_feature[feature_name])
                    self.features.append(float(self.mutation_pdbchain_feature[feature_name]) / 2)
                elif self.ptm_pdbchain_feature[feature_name] != 'NA' and self.mutation_pdbchain_feature[
                    feature_name] == 'NA':
                    self.features.append(0)
                    self.features.append(self.ptm_pdbchain_feature[feature_name])
                    self.features.append(float(self.ptm_pdbchain_feature[feature_name]) / 2)
                elif self.ptm_pdbchain_feature[feature_name] == 'NA' and self.mutation_pdbchain_feature[
                    feature_name] == 'NA':
                    self.features.append(0)
                    self.features.append(0)
                    self.features.append(0)
                else:
                    self.features.append(
                        min(self.ptm_pdbchain_feature[feature_name], self.mutation_pdbchain_feature[feature_name]))
                    self.features.append(
                        max(self.ptm_pdbchain_feature[feature_name], self.mutation_pdbchain_feature[feature_name]))
                    self.features.append((float(self.ptm_pdbchain_feature[feature_name]) + float(
                        self.mutation_pdbchain_feature[feature_name])) / 2)

    def pdbchain_feature_gnm_prs(self, gnm_prs_path):
        files = os.listdir(gnm_prs_path)
        pdbChain = self.Pdb + '_' + self.Chain
        pdbChain_files = []
        for file in files:
            if pdbChain == file[:6]:
                pdbChain_files.append(file)
        for pdbChain_file in sorted(pdbChain_files):
            print(pdbChain_file)
            if 'prs' in pdbChain_file:
                with open(gnm_prs_path + '\\' + pdbChain_file, 'r') as f:
                    datas = f.readlines()
                    feature_name = pdbChain_file.split('.')[0][7:]
                    try:
                        self.features.append(
                            datas[self.PtmPdbPositionAbsolute - 1].strip('\n').split(':')[1].strip('[]').split(',')
                            [self.MutationPdbPositionAbsolute - 1].strip())
                    except:
                        self.features.append('null')
            elif 'effectiveness' in pdbChain_file:
                with open(gnm_prs_path + '\\' + pdbChain_file, 'r') as f:
                    datas = f.readlines()
                    feature_name = pdbChain_file.split('.')[0][7:]
                    self.ptm_pdbchain_feature[feature_name] = \
                        datas[self.PtmPdbPositionAbsolute - 1].strip('\n').split(':')[1]
                    self.mutation_pdbchain_feature[feature_name] = \
                        datas[self.MutationPdbPositionAbsolute - 1].strip('\n').split(':')[1]
                    if self.ptm_pdbchain_feature[feature_name] == 'NA' and self.mutation_pdbchain_feature[
                        feature_name] != 'NA':
                        self.features.append(0)
                        self.features.append(self.mutation_pdbchain_feature[feature_name])
                        self.features.append(float(self.mutation_pdbchain_feature[feature_name]) / 2)
                    elif self.ptm_pdbchain_feature[feature_name] != 'NA' and self.mutation_pdbchain_feature[
                        feature_name] == 'NA':
                        self.features.append(0)
                        self.features.append(self.ptm_pdbchain_feature[feature_name])
                        self.features.append(float(self.ptm_pdbchain_feature[feature_name]) / 2)
                    elif self.ptm_pdbchain_feature[feature_name] == 'NA' and self.mutation_pdbchain_feature[
                        feature_name] == 'NA':
                        self.features.append(0)
                        self.features.append(0)
                        self.features.append(0)
                    else:
                        self.features.append(
                            min(self.ptm_pdbchain_feature[feature_name], self.mutation_pdbchain_feature[feature_name]))
                        self.features.append(
                            max(self.ptm_pdbchain_feature[feature_name], self.mutation_pdbchain_feature[feature_name]))
                        self.features.append((float(self.ptm_pdbchain_feature[feature_name]) + float(
                            self.mutation_pdbchain_feature[feature_name])) / 2)
            elif 'sensitivity' in pdbChain_file:
                with open(gnm_prs_path + '\\' + pdbChain_file, 'r') as f:
                    datas = f.readlines()
                    feature_name = pdbChain_file.split('.')[0][7:]
                    self.ptm_pdbchain_feature[feature_name] = \
                        datas[self.PtmPdbPositionAbsolute - 1].strip('\n').split(':')[1]
                    self.mutation_pdbchain_feature[feature_name] = \
                        datas[self.MutationPdbPositionAbsolute - 1].strip('\n').split(':')[1]
                    if self.ptm_pdbchain_feature[feature_name] == 'NA' and self.mutation_pdbchain_feature[
                        feature_name] != 'NA':
                        self.features.append(0)
                        self.features.append(self.mutation_pdbchain_feature[feature_name])
                        self.features.append(float(self.mutation_pdbchain_feature[feature_name]) / 2)
                    elif self.ptm_pdbchain_feature[feature_name] != 'NA' and self.mutation_pdbchain_feature[
                        feature_name] == 'NA':
                        self.features.append(0)
                        self.features.append(self.ptm_pdbchain_feature[feature_name])
                        self.features.append(float(self.ptm_pdbchain_feature[feature_name]) / 2)
                    elif self.ptm_pdbchain_feature[feature_name] == 'NA' and self.mutation_pdbchain_feature[
                        feature_name] == 'NA':
                        self.features.append(0)
                        self.features.append(0)
                        self.features.append(0)
                    else:
                        self.features.append(
                            min(self.ptm_pdbchain_feature[feature_name], self.mutation_pdbchain_feature[feature_name]))
                        self.features.append(
                            max(self.ptm_pdbchain_feature[feature_name], self.mutation_pdbchain_feature[feature_name]))
                        self.features.append((float(self.ptm_pdbchain_feature[feature_name]) + float(
                            self.mutation_pdbchain_feature[feature_name])) / 2)

    def pdbchain_feature_gnm_sq(self, gnm_sq_path):
        files = os.listdir(gnm_sq_path)
        pdbChain = self.Pdb + '_' + self.Chain
        pdbChain_files = []
        for file in files:
            if pdbChain == file[:6]:
                pdbChain_files.append(file)
        for pdbChain_file in sorted(pdbChain_files):
            print(pdbChain_file)
            with open(gnm_sq_path + '\\' + pdbChain_file, 'r') as f:
                datas = f.readlines()
                feature_name = pdbChain_file.split('.')[0][7:]
                self.ptm_pdbchain_feature[feature_name] = datas[self.PtmPdbPositionAbsolute - 1].strip('\n').split(':')[
                    1]
                self.mutation_pdbchain_feature[feature_name] = \
                    datas[self.MutationPdbPositionAbsolute - 1].strip('\n').split(':')[1]
                if self.ptm_pdbchain_feature[feature_name] == 'NA' and self.mutation_pdbchain_feature[
                    feature_name] != 'NA':
                    self.features.append(0)
                    self.features.append(self.mutation_pdbchain_feature[feature_name])
                    self.features.append(float(self.mutation_pdbchain_feature[feature_name]) / 2)
                elif self.ptm_pdbchain_feature[feature_name] != 'NA' and self.mutation_pdbchain_feature[
                    feature_name] == 'NA':
                    self.features.append(0)
                    self.features.append(self.ptm_pdbchain_feature[feature_name])
                    self.features.append(float(self.ptm_pdbchain_feature[feature_name]) / 2)
                elif self.ptm_pdbchain_feature[feature_name] == 'NA' and self.mutation_pdbchain_feature[
                    feature_name] == 'NA':
                    self.features.append(0)
                    self.features.append(0)
                    self.features.append(0)
                else:
                    self.features.append(
                        min(self.ptm_pdbchain_feature[feature_name], self.mutation_pdbchain_feature[feature_name]))
                    self.features.append(
                        max(self.ptm_pdbchain_feature[feature_name], self.mutation_pdbchain_feature[feature_name]))
                    self.features.append((float(self.ptm_pdbchain_feature[feature_name]) + float(
                        self.mutation_pdbchain_feature[feature_name])) / 2)

    '''
    Seq features
    uniprot_files(evol, extract features by uniprot and uniprotsite):
    # dirinfo
    entropy
    mifc
    mifn
    mutinfo
    occupancy
    omes
    sca
    '''

    def uninprot_feature_evol_dirinfo(self, evol_dirinfo_path):
        files = os.listdir(evol_dirinfo_path)
        p = self.PtmUniprotPosition
        m = self.MutationUniprotPosition
        for file in files:
            if self.UniprotId == file[:6]:
                print(file)
                with open(evol_dirinfo_path + '\\' + file, 'r') as f:
                    datas = f.readlines()
                    # ptm_lines = datas[p - 1]
                    # mutation_lines = datas[m - 1]
                    # ptm_nums = [line for line in ptm_lines.split(' ')]
                    # mutation_nums = [line for line in mutation_lines.split(' ')]
                    # ptm_result_all = 0
                    # for num in ptm_nums:
                    #     ptm_result_all += float(num)
                    # ptm_avg_all_dirinfo = ptm_result_all / len(ptm_nums)
                    # ptm_result_11 = 0
                    # for num in ptm_nums[p - 6:p + 5]:
                    #     ptm_result_11 += float(num)
                    # ptm_avg_11_dirinfo = ptm_result_11 / 11
                    # mutation_result_all = 0
                    # for num in mutation_nums:
                    #     mutation_result_all += float(num)
                    # mutation_avg_all_dirinfo = mutation_result_all / len(mutation_nums)
                    # mutation_result_11 = 0
                    # for num in mutation_nums[p - 6:p + 5]:
                    #     mutation_result_11 += float(num)
                    # mutation_avg_11_dirinfo = mutation_result_11 / 11
                    # self.ptm_uniprot_feature['ptm_evol_all_dirinfo'] = ptm_avg_all_dirinfo
                    # self.ptm_uniprot_feature['ptm_evol_11_dirinfo'] = ptm_avg_11_dirinfo
                    # self.mutation_uniprot_feature['mutation_evol_all_dirinfo'] = mutation_avg_all_dirinfo
                    # self.mutation_uniprot_feature['mutation_evol_11_dirinfo'] = mutation_avg_11_dirinfo
                    try:
                        self.features.append(datas[p - 1].strip('\n').split(' ')[m - 1])
                    except:
                        self.features.append('null')

    def uninprot_feature_evol_entropy(self, evol_entropy_path):
        files = os.listdir(evol_entropy_path)
        for file in files:
            if self.UniprotId == file[:6]:
                print(file)
                with open(evol_entropy_path + '\\' + file, 'r') as f:
                    datas = f.readlines()
                    feature_name = 'ptm_evol_entropy'
                    self.ptm_uniprot_feature[feature_name] = datas[self.PtmUniprotPosition - 1].strip('\n')
                    self.mutation_uniprot_feature[feature_name] = datas[self.MutationUniprotPosition - 1].strip('\n')
                    if self.ptm_uniprot_feature[feature_name] == 'NA' and self.mutation_uniprotfeature[
                        feature_name] != 'NA':
                        self.features.append(0)
                        self.features.append(self.mutation_uniprot_feature[feature_name])
                        self.features.append(float(self.mutation_uniprot_feature[feature_name]) / 2)
                    elif self.ptm_uniprot_feature[feature_name] != 'NA' and self.mutation_uniprot_feature[
                        feature_name] == 'NA':
                        self.features.append(0)
                        self.features.append(self.ptm_uniprot_feature[feature_name])
                        self.features.append(float(self.ptm_uniprot_feature[feature_name]) / 2)
                    elif self.ptm_uniprot_feature[feature_name] == 'NA' and self.mutation_uniprot_feature[
                        feature_name] == 'NA':
                        self.features.append(0)
                        self.features.append(0)
                        self.features.append(0)
                    else:
                        self.features.append(
                            min(self.ptm_uniprot_feature[feature_name], self.mutation_uniprot_feature[feature_name]))
                        self.features.append(
                            max(self.ptm_uniprot_feature[feature_name], self.mutation_uniprot_feature[feature_name]))
                        self.features.append((float(self.ptm_uniprot_feature[feature_name]) + float(
                            self.mutation_uniprot_feature[feature_name])) / 2)

    def uninprot_feature_evol_mifc(self, evol_mifc_path):
        files = os.listdir(evol_mifc_path)
        p = self.PtmUniprotPosition
        m = self.MutationUniprotPosition
        for file in files:
            if self.UniprotId == file[:6]:
                print(file)
                with open(evol_mifc_path + '\\' + file, 'r') as f:
                    datas = f.readlines()
                    '''
                    ptm_lines = datas[p - 1]
                    mutation_lines = datas[m - 1]
                    ptm_nums = [line for line in ptm_lines.split(' ')]
                    mutation_nums = [line for line in mutation_lines.split(' ')]
                    ptm_result_all = 0
                    for num in ptm_nums:
                        ptm_result_all += float(num)
                    ptm_avg_all_mifc = ptm_result_all / len(ptm_nums)
                    ptm_result_11 = 0
                    for num in ptm_nums[p - 6:p + 5]:
                        ptm_result_11 += float(num)
                    ptm_avg_11_mifc = ptm_result_11 / 11
                    mutation_result_all = 0
                    for num in mutation_nums:
                        mutation_result_all += float(num)
                    mutation_avg_all_mifc = mutation_result_all / len(mutation_nums)
                    mutation_result_11 = 0
                    for num in mutation_nums[p - 6:p + 5]:
                        mutation_result_11 += float(num)
                    mutation_avg_11_mifc = mutation_result_11 / 11
                    self.ptm_uniprot_feature['ptm_evol_all_mifc'] = ptm_avg_all_mifc
                    self.ptm_uniprot_feature['ptm_evol_11_mifc'] = ptm_avg_11_mifc
                    self.mutation_uniprot_feature['mutation_evol_all_mifc'] = mutation_avg_all_mifc
                    self.mutation_uniprot_feature['mutation_evol_11_mifc'] = mutation_avg_11_mifc
                    '''
                    try:
                        self.features.append(datas[p - 1].strip('\n').split(' ')[m - 1])
                    except:
                        self.features.append('null')

    def uninprot_feature_evol_mifn(self, evol_mifn_path):
        files = os.listdir(evol_mifn_path)
        p = self.PtmUniprotPosition
        m = self.MutationUniprotPosition
        for file in files:
            if self.UniprotId == file[:6]:
                print(file)
                with open(evol_mifn_path + '\\' + file, 'r') as f:
                    datas = f.readlines()
                    # ptm_lines = datas[p - 1]
                    # mutation_lines = datas[m - 1]
                    # ptm_nums = [line for line in ptm_lines.split(' ')]
                    # mutation_nums = [line for line in mutation_lines.split(' ')]
                    # ptm_result_all = 0
                    # for num in ptm_nums:
                    #     ptm_result_all += float(num)
                    # ptm_avg_all_mifn = ptm_result_all / len(ptm_nums)
                    # ptm_result_11 = 0
                    # for num in ptm_nums[p - 6:p + 5]:
                    #     ptm_result_11 += float(num)
                    # ptm_avg_11_mifn = ptm_result_11 / 11
                    # mutation_result_all = 0
                    # for num in mutation_nums:
                    #     mutation_result_all += float(num)
                    # mutation_avg_all_mifn = mutation_result_all / len(mutation_nums)
                    # mutation_result_11 = 0
                    # for num in mutation_nums[p - 6:p + 5]:
                    #     mutation_result_11 += float(num)
                    # mutation_avg_11_mifn = mutation_result_11 / 11
                    # self.ptm_uniprot_feature['ptm_evol_all_mifn'] = ptm_avg_all_mifn
                    # self.ptm_uniprot_feature['ptm_evol_11_mifn'] = ptm_avg_11_mifn
                    # self.mutation_uniprot_feature['mutation_evol_all_mifn'] = mutation_avg_all_mifn
                    # self.mutation_uniprot_feature['mutation_evol_11_mifn'] = mutation_avg_11_mifn
                    try:
                        self.features.append(datas[p - 1].strip('\n').split(' ')[m - 1])
                    except:
                        self.features.append('null')

    def uninprot_feature_evol_mutinfo(self, evol_mutinfo_path):
        files = os.listdir(evol_mutinfo_path)
        p = self.PtmUniprotPosition
        m = self.MutationUniprotPosition
        for file in files:
            if self.UniprotId == file[:6]:
                print(file)
                with open(evol_mutinfo_path + '\\' + file, 'r') as f:
                    datas = f.readlines()
                    # ptm_lines = datas[p - 1]
                    # mutation_lines = datas[m - 1]
                    # ptm_nums = [line for line in ptm_lines.split(' ')]
                    # mutation_nums = [line for line in mutation_lines.split(' ')]
                    # ptm_result_all = 0
                    # for num in ptm_nums:
                    #     ptm_result_all += float(num)
                    # ptm_avg_all_mutinfo = ptm_result_all / len(ptm_nums)
                    # ptm_result_11 = 0
                    # for num in ptm_nums[p - 6:p + 5]:
                    #     ptm_result_11 += float(num)
                    # ptm_avg_11_mutinfo = ptm_result_11 / 11
                    # mutation_result_all = 0
                    # for num in mutation_nums:
                    #     mutation_result_all += float(num)
                    # mutation_avg_all_mutinfo = mutation_result_all / len(mutation_nums)
                    # mutation_result_11 = 0
                    # for num in mutation_nums[p - 6:p + 5]:
                    #     mutation_result_11 += float(num)
                    # mutation_avg_11_mutinfo = mutation_result_11 / 11
                    # self.ptm_uniprot_feature['ptm_evol_all_mutinfo'] = ptm_avg_all_mutinfo
                    # self.ptm_uniprot_feature['ptm_evol_11_mutinfo'] = ptm_avg_11_mutinfo
                    # self.mutation_uniprot_feature['mutation_evol_all_mutinfo'] = mutation_avg_all_mutinfo
                    # self.mutation_uniprot_feature['mutation_evol_11_mutinfo'] = mutation_avg_11_mutinfo
                    try:
                        self.features.append(datas[p - 1].strip('\n').split(' ')[m - 1])
                    except:
                        self.features.append('null')

    def uninprot_feature_evol_occupancy(self, evol_occupancy_path):
        files = os.listdir(evol_occupancy_path)
        for file in files:
            if self.UniprotId == file[:6]:
                print(file)
                with open(evol_occupancy_path + '\\' + file, 'r') as f:
                    datas = f.readlines()
                    feature_name = 'ptm_evol_occupancy'
                    self.ptm_uniprot_feature[feature_name] = datas[
                        self.PtmUniprotPosition - 1].strip('\n')
                    self.mutation_uniprot_feature[feature_name] = datas[
                        self.MutationUniprotPosition - 1].strip('\n')
                    if self.ptm_uniprot_feature[feature_name] == 'NA' and self.mutation_uniprotfeature[
                        feature_name] != 'NA':
                        self.features.append(0)
                        self.features.append(self.mutation_uniprot_feature[feature_name])
                        self.features.append(float(self.mutation_uniprot_feature[feature_name]) / 2)
                    elif self.ptm_uniprot_feature[feature_name] != 'NA' and self.mutation_uniprot_feature[
                        feature_name] == 'NA':
                        self.features.append(0)
                        self.features.append(self.ptm_uniprot_feature[feature_name])
                        self.features.append(float(self.ptm_uniprot_feature[feature_name]) / 2)
                    elif self.ptm_uniprot_feature[feature_name] == 'NA' and self.mutation_uniprot_feature[
                        feature_name] == 'NA':
                        self.features.append(0)
                        self.features.append(0)
                        self.features.append(0)
                    else:
                        self.features.append(
                            min(self.ptm_uniprot_feature[feature_name], self.mutation_uniprot_feature[feature_name]))
                        self.features.append(
                            max(self.ptm_uniprot_feature[feature_name], self.mutation_uniprot_feature[feature_name]))
                        self.features.append((float(self.ptm_uniprot_feature[feature_name]) + float(
                            self.mutation_uniprot_feature[feature_name])) / 2)

    def uninprot_feature_evol_omes(self, evol_omes_path):
        files = os.listdir(evol_omes_path)
        p = self.PtmUniprotPosition
        m = self.MutationUniprotPosition
        for file in files:
            if self.UniprotId == file[:6]:
                print(file)
                with open(evol_omes_path + '\\' + file, 'r') as f:
                    datas = f.readlines()
                    # ptm_lines = datas[p - 1]
                    # mutation_lines = datas[m - 1]
                    # ptm_nums = [line for line in ptm_lines.split(' ')]
                    # mutation_nums = [line for line in mutation_lines.split(' ')]
                    # ptm_result_all = 0
                    # for num in ptm_nums:
                    #     ptm_result_all += float(num)
                    # ptm_avg_all_omes = ptm_result_all / len(ptm_nums)
                    # ptm_result_11 = 0
                    # for num in ptm_nums[p - 6:p + 5]:
                    #     ptm_result_11 += float(num)
                    # ptm_avg_11_omes = ptm_result_11 / 11
                    # mutation_result_all = 0
                    # for num in mutation_nums:
                    #     mutation_result_all += float(num)
                    # mutation_avg_all_omes = mutation_result_all / len(mutation_nums)
                    # mutation_result_11 = 0
                    # for num in mutation_nums[p - 6:p + 5]:
                    #     mutation_result_11 += float(num)
                    # mutation_avg_11_omes = mutation_result_11 / 11
                    # self.ptm_uniprot_feature['ptm_evol_all_omes'] = ptm_avg_all_omes
                    # self.ptm_uniprot_feature['ptm_evol_11_omes'] = ptm_avg_11_omes
                    # self.mutation_uniprot_feature['mutation_evol_all_omes'] = mutation_avg_all_omes
                    # self.mutation_uniprot_feature['mutation_evol_11_omes'] = mutation_avg_11_omes
                    try:
                        self.features.append(datas[p - 1].strip('\n').split(' ')[m - 1])
                    except:
                        self.features.append('null')

    def uninprot_feature_evol_sca(self, evol_sca_path):
        files = os.listdir(evol_sca_path)
        p = self.PtmUniprotPosition
        m = self.MutationUniprotPosition
        for file in files:
            if self.UniprotId == file[:6]:
                print(file)
                with open(evol_sca_path + '\\' + file, 'r') as f:
                    datas = f.readlines()
                    # ptm_lines = datas[p - 1]
                    # mutation_lines = datas[m - 1]
                    # ptm_nums = [line for line in ptm_lines.split(' ')]
                    # mutation_nums = [line for line in mutation_lines.split(' ')]
                    # ptm_result_all = 0
                    # for num in ptm_nums:
                    #     ptm_result_all += float(num)
                    # ptm_avg_all_sca = ptm_result_all / len(ptm_nums)
                    # ptm_result_11 = 0
                    # for num in ptm_nums[p - 6:p + 5]:
                    #     ptm_result_11 += float(num)
                    # ptm_avg_11_sca = ptm_result_11 / 11
                    # mutation_result_all = 0
                    # for num in mutation_nums:
                    #     mutation_result_all += float(num)
                    # mutation_avg_all_sca = mutation_result_all / len(mutation_nums)
                    # mutation_result_11 = 0
                    # for num in mutation_nums[p - 6:p + 5]:
                    #     mutation_result_11 += float(num)
                    # mutation_avg_11_sca = mutation_result_11 / 11
                    # self.ptm_uniprot_feature['ptm_evol_all_sca'] = ptm_avg_all_sca
                    # self.ptm_uniprot_feature['ptm_evol_11_sca'] = ptm_avg_11_sca
                    # self.mutation_uniprot_feature['mutation_evol_all_sca'] = mutation_avg_all_sca
                    # self.mutation_uniprot_feature['mutation_evol_11_sca'] = mutation_avg_11_sca
                    try:
                        self.features.append(datas[p - 1].strip('\n').split(' ')[m - 1])
                    except:
                        self.features.append('null')
