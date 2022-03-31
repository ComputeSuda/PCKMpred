# -*- coding: utf-8 -*-

from prody import *
from pylab import *
from Bio import AlignIO
import os

# ion()
from numpy import *
from matplotlib.pylab import *
import pickle

blast_omega_aln_path = '../../Dataprocess/clustal-omega/uniprot_aln/'
out_put_path = './results/'
aln_files = sorted(os.listdir(blast_omega_aln_path))
print(len(aln_files))

# uniprot = {'O00429': '4H1U'}
# for aln_file in aln_files:
error_muti_seq = []
error_uniprot = []
error_blast_fasta = []
for i in range(len(aln_files)):
    aln_file = aln_files[i]
    print(aln_file)
    print(i)
    # pfam = list(searchPfam(i).keys())
    # print('pfam: ', pfam[0])  # PF00017
    # pf_msa = fetchPfamMSA(pfam[0])
    # print('pf_msa: ', pf_msa)  # .\PF00017_full.sth
    input_file = blast_omega_aln_path + aln_file
    # output_file = out_put_path + aln_file[:6]
    print(input_file)
    msa = parseMSA(input_file)
    # print(msa.getIndex())
    # print('msa: ', msa)  # MSA PF00017_full
    with open(input_file, 'r') as f:
        lines = f.readlines()
        if '|' in lines[0]:
            labels = lines[0].split('|')
            print(labels[1])
            label_1 = labels[1]
        else:
            labels = lines[0].split('.')
            label_1 = labels[0][1:] + '.' + labels[1][0]
        print(label_1)
        for line in lines[1:]:
            if label_1 in line:
                error_muti_seq.append(input_file)
    # print(error_muti_seq)
    # print(len(set(error_muti_seq)))
    try:
        msa_refine = refineMSA(msa, label=label_1, rowocc=0.6, seqid=1)
    except:
        error_uniprot.append(input_file)
        continue
    # print(type(msa_refine))
    # msa_refine = msa_refine[:, 36:761]
    # print(type(msa_refine_1))

    occupancy = calcMSAOccupancy(msa_refine, occ='res')
    output_occupancy_file = out_put_path+'occupancy/'+aln_file[:6]
    name_1 = output_occupancy_file + '_occupancy.txt'
    np.savetxt(name_1, occupancy)

    entropy = calcShannonEntropy(msa_refine)
    output_entropy_file = out_put_path + 'entropy/' + aln_file[:6]
    name_2 = output_entropy_file + '_entropy.txt'
    np.savetxt(name_2, entropy)

    mutinfo = buildMutinfoMatrix(msa_refine)
    output_mutinfo_file = out_put_path + 'mutinfo/' + aln_file[:6]
    name_3 = output_mutinfo_file + '_mutinfo.txt'
    writeArray(name_3, mutinfo)

    omes = buildOMESMatrix(msa_refine)
    output_omes_file = out_put_path + 'omes/' + aln_file[:6]
    name_4 = output_omes_file + '_omes.txt'
    writeArray(name_4, omes)

    sca = buildSCAMatrix(msa_refine)
    output_sca_file = out_put_path + 'sca/' + aln_file[:6]
    name_5 = output_sca_file + '_sca.txt'
    writeArray(name_5, sca)

    # output_dirinfo_file = out_put_path + 'dirinfo/' + aln_file[:6]
    # name_6 = output_dirinfo_file + '_dirinfo.txt'
    # dirinfo = buildDirectInfoMatrix(msa_refine)
    # writeArray(name_6, dirinfo)

    output_msa_file = out_put_path + 'msa/' + aln_file[:6]
    name_7 = output_msa_file + '_msa.fasta'
    writeMSA(name_7, msa_refine)

    mifc = applyMutinfoCorr(mutinfo, corr='apc')
    output_mifc_file = out_put_path + 'mifc/' + aln_file[:6]
    name_8 = output_mifc_file + '_mifc.txt'
    writeArray(name_8, mifc)

    mifn = applyMutinfoNorm(mutinfo, entropy, norm='minent')
    output_mifn_file = out_put_path + 'mifn/' + aln_file[:6]
    name_9 = output_mifn_file + '_mifn.txt'
    writeArray(name_9, mifn)

with open('error.txt', 'w') as f:
    for item in error_uniprot:
        f.write(item + '\n')
