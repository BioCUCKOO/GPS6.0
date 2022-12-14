# -*- coding: utf-8 -*-

"""
@author: mia
"""

import sys,os,re,joblib

import pandas as pd
import numpy as np
import collections
from collections import Counter
import lightgbm as lgb
from keras.models import load_model
def fasta2seq(input,outpath,KN="ST"):


    f_fas = open(input, 'r') 
    id_seq = {}
    global linename
    for line in f_fas:
        if line.startswith('>'):
           linename = line.replace('>', '').strip()
           id_seq[linename] = ''
        else:
           id_seq[linename] += line.strip()
    print(id_seq)
    ids = []
    psp61 = []
    locss = []
    for k,v in id_seq.items():

        psps = []
        locs = []
        proposal_psp = '******************************'  # 30个
        for i in range(len(v)):
            if KN=="ST" and v[i] != "S" and v[i] != "T" :
                
                pass
            elif KN=="Y" and v[i] != "Y":
                pass
            else:
                if i < 30:
             
                    psp = proposal_psp[:(30 - i)]
                    tem = v[:i + 31]
                    psp = psp + tem
                    if len(psp) < 61:
                        tem2 = proposal_psp[:(61 - len(psp))]
                        psp = psp + tem2
       
                elif i >= (len(v) - 30):
                    psp = v[(i - 30):(len(v))]
                    tem = proposal_psp[:(30 - (len(v) - i - 1))]
                    psp = psp + tem
                else:
                    psp = v[i - 30:i + 31]
                psps.append(psp)
                locs.append(i)
        ids.extend([k]*len(psps))
        psp61.extend(psps)
        locss.extend(locs)
    # print(ids)
    # print(psp61)
    # print(locss)

    df = pd.DataFrame({'ID':ids,
                       'PSP':psp61,
                       'loc':locss
                       })
    # df.to_csv(outpath + 'psp.csv',index = False) 
    return id_seq, df

def getblosum62():
    f1 = open('/data/www/gps6/webcomp/models/pref/BLOSUM62', 'r')
    l_AAS = []
    AAs = []
    scores = {}
    for line in f1.readlines():
        sp = line.split()
        aa = sp[0]
        AAs.append(aa)
    f1.close()
    f2 = open('/data/www/gps6/webcomp/models/pref/BLOSUM62', 'r')
    num = 0
    for line in f2.readlines():
        sp = line.strip()
        sp = line.split()
        for i in range(len(sp)):
            if i == 0:
                continue
            else:
                score = float(sp[i])
                aas = AAs[num] + "_" + AAs[i-1]
                aas2 = AAs[i-1] + "_" + AAs[num]
                if aas not in l_AAS and aas2 not in l_AAS:
                    l_AAS.append(aas)   
                    scores[aas] = score
        num += 1        
    f2.close()
    return scores,l_AAS,AAs

def getArray(l_AAs):
    score = []
    for i in range(len(l_AAs)):
        score.append(0.0)
    scoreary = np.array(score)
    return scoreary

def getMMScoreTest(seq, weights, out_path,KN="ST"):


    AAscores, l_aas, AAs = getblosum62()
    if KN =="ST":
        scores_test = np.load("/data/www/gps6/webcomp/models/pref/stpos_smoscores.npy",allow_pickle=True)
    else:
        scores_test = np.load("/data/www/gps6/webcomp/models/pref/ypos_smoscores.npy",allow_pickle=True)
  
    l_scores = []

    for pep in seq:
        score = getArray(l_aas)
        for i in range(len(pep)):
            aa = pep[i]
            if aa not in AAs:
                aa = '*'
            index = AAs.index(aa)
            scoreary = scores_test[i][index]
            score = score + scoreary

        score = (score / (len(scores_test))).tolist()
        l_scores.append(score)

    l_scores = np.float16(l_scores)
    np.save(out_path + 'SMO', l_scores)
   
def is_aa(x):
    aa_order = ['A', 'R', 'N', 'D', 'C', 'Q', 'E', 'G', 'H', 'I', 'L', 'K', 'M', 'F', 'P', 'S', 'T', 'W', 'Y', 'V', '*']
    if x in aa_order:
        return x
    else:
        return '*'

def window_slide(row):
    A = []
    aa_order = ['A', 'R', 'N', 'D', 'C', 'Q', 'E', 'G', 'H', 'I', 'L', 'K', 'M', 'F', 'P', 'S', 'T', 'W', 'Y', 'V', '*']
    num_aa = collections.OrderedDict()
    num_aa = num_aa.fromkeys(aa_order, 0)
    row = list(row.replace(" ", ""))
    for i in range(len(row)):
        if row[i] not in aa_order:
            row[i] = '*'
    row = list(map(is_aa, row))
    for i in range(len(row)):
        if i < 57:
            list1 = list(row[i:i + 5])
            B = Counter(list1)
            C = {**num_aa, **B}
            D = list(C.values())
            D = list(map(lambda x: (x / 5), D))
            A = A + D
        else:
            break
    return A

def get_EAAC(seq, outpath):
    results = list(map(window_slide, seq))

    np_results = np.array(results)
    np.save(outpath + 'EAAC', np_results)





def seq2Z(seq):
    A = [0.24, -2.32, 0.60, -0.14, 1.30]
    M = [-2.85, -0.22, 0.47, 1.94, -0.98]
    C = [0.84, -1.67, 3.71, 0.18, -2.65]
    N = [3.05, 1.60, 1.04, -1.15, 1.61]
    D = [3.98, 0.93, 1.93, -2.46, 0.75]
    P = [-1.66, 0.27, 1.84, 0.70, 2.00]
    E = [3.11, 0.26, -0.11, -3.04, -0.25]
    Q = [1.75, 0.50, -1.44, -1.34, 0.66]
    F = [-4.22, 1.94, 1.06, 0.54, -0.62]
    R = [3.52, 2.50, -3.50, 1.99, -0.17]
    G = [2.05, 4.06, 0.36, -0.82, -0.38]
    S = [2.39, -1.07, 1.15, -1.39, 0.67]
    H = [2.47, 1.95, 0.26, 3.90, 0.09]
    T = [0.75, -2.18, -1.12, -1.46, -0.40]
    I = [-3.89, -1.73, -1.71, -0.84, 0.26]
    V = [-2.59, -2.64, -1.54, -0.85, -0.02]
    K = [2.29, 0.89, -2.49, 1.49, 0.31]
    W = [-4.36, 3.94, 0.59, 3.44, -1.59]
    L = [-4.28, -1.30, -1.49, -0.72, 0.84]
    Y = [-2.54, 2.44, 0.43, 0.04, -1.47]
    zero = [0, 0, 0, 0, 0]
    aalist = ['A', 'R', 'N', 'D', 'C', 'Q', 'E', 'G', 'H', 'I', 'L', 'K', 'M', 'F', 'P', 'S', 'T', 'W', 'Y', 'V']
    aa_dic = {'A': A, 'M': M, 'C': C, 'N': N, 'D': D, 'P': P, 'E': E, 'Q': Q, 'F': F, 'R': R, 'G': G, 'S': S, 'H': H,
              'T': T, 'I': I, 'V': V, 'K': K, 'W': W, 'L': L, 'Y': Y, '*': zero}
    zscale = []
    seq = seq.strip()
    for aa in seq:
        if aa not in aalist:
            aa = '*'
        tl = aa_dic[aa]
        zscale = zscale + tl

    return zscale
def get_ZScale(seq, outpath):
    results = list(map(seq2Z, seq))
 
    np_results = np.array(results)
    np.save(outpath + 'ZScale', np_results)


def seq2index(seq):
    dic = np.load('/data/www/gps6/webcomp/models/pref/aaidx_dic.npy',allow_pickle=True)
    
    dic = dic.item()
    index = []
    aas = ['A', 'R', 'N', 'D', 'C', 'Q', 'E', 'G', 'H', 'I', 'L', 'K', 'M', 'F', 'P', 'S', 'T', 'W', 'Y', 'V']
    for aa in seq:
        if aa not in aas:
            aa = '*'
        list_tem = dic[aa]
        index = index + list_tem
    return index
def get_AAIndex(seq, outpath):
    results = list(map(seq2index, seq))
    np_results = np.array(results)
   
    np.save(outpath + 'AAIndex', np_results)


def seq2bit(seq):
    aas = ['A', 'R', 'N', 'D', 'C', 'Q', 'E', 'G', 'H', 'I', 'L', 'K', 'M', 'F', 'P', 'S', 'T', 'W', 'Y', 'V']
    # aa_opf = np.load('/home/biocucko/public_html/gps/webcomp/models/pref/opf71_dic.npy',allow_pickle=True)
    aa_opf = np.load('/data/www/gps6/webcomp/models/pref/opf71_dic.npy',allow_pickle=True)
   
    aa_opf = aa_opf.item()
    bit7 = []
    for aa in seq:
        if aa not in aas:
            list_tem = [0, 0, 0, 0, 0, 0, 0]
        else:
            list_tem = aa_opf[aa]
        bit7 = bit7 + list_tem
    return bit7
def get_OPF_7bit_1(seq, outpath):
    results = list(map(seq2bit, seq))

    np_results = np.array(results)
    np.save(outpath + 'OPF_7bit_type1', np_results)
def onehot(psp):

    AAs=['*', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'W', 'X', 'Y', 'Z']
    char_to_int = np.load("/data/www/gps6/webcomp/models/pref/bny_dic.npy",allow_pickle=True)
    char_to_int = char_to_int.item()
    # integer encode input data
    psp = list(psp)
    for i in range(len(psp)):
        if psp[i] not in AAs:
            psp[i] = '*'

    psp = "".join(psp)
    seq2int = [char_to_int[char] for char in psp]
    # one hot encode
    onehot_encoded = list()

    for v in seq2int:
        letter = [0 for _ in range(len(AAs))]
        letter[v] = 1
        onehot_encoded = onehot_encoded + letter
    return onehot_encoded

def get_binary(seqs, outpath):
    results = list(map(onehot, seqs))
    # df_results = pd.DataFrame(results)
    # df_results.to_csv(outpath + 'binary.csv', index=False)
    np_results = np.array(results)
    np.save(outpath + 'binary', np_results)
def seq2bit5(psp):
    dic = {'A': [0, 0, 0, 1, 1], 'C': [0, 0, 1, 0, 1], 'D': [0, 0, 1, 1, 0], 'E': [0, 0, 1, 1, 1], 'F': [0, 1, 0, 0, 1],
           'G': [0, 1, 0, 1, 0],
           'H': [0, 1, 0, 1, 1], 'I': [0, 1, 1, 0, 0], 'K': [0, 1, 1, 0, 1], 'L': [0, 1, 1, 1, 0], 'M': [1, 0, 0, 0, 1],
           'N': [1, 0, 0, 1, 0],
           'P': [1, 0, 0, 1, 1], 'Q': [1, 0, 1, 0, 0], 'R': [1, 0, 1, 0, 1], 'S': [1, 0, 1, 1, 0], 'T': [1, 1, 0, 0, 0],
           'V': [1, 1, 0, 0, 1],
           'W': [1, 1, 0, 1, 0], 'Y': [1, 1, 1, 0, 0], '*': [0, 0, 0, 0, 0]}
    psp = psp.strip()
    bn5 = []
    for aa in psp:
        if aa not in dic.keys():
            aa = '*'
        tl = dic[aa]
        bn5 = bn5 + tl
    return bn5

def get_binary5bit2(seqs, outpath):
    # df = pd.read_csv(file_path,header=0)
    results = list(map(seq2bit5, seqs))
    # df_results = pd.DataFrame(results)
    # df_results['Label'] = df['Label'].tolist()
    # df_results.to_csv(outpath + 'binary5bit2.csv', index=False)
    np_results = np.array(results)
    np.save(outpath + 'binary5bit2', np_results)
def seq2AESNN3(psp):
    dic = {'A': [-0.99, -0.61, 0.00],
           'R': [0.28, -0.99, -0.22],
           'N': [0.77, -0.24, 0.59],
           'D': [0.74, -0.72, -0.35],
           'C': [0.34, 0.88, 0.35],
           'Q': [0.12, -0.99, -0.99],
           'E': [0.59, -0.55, -0.99],
           'G': [-0.79, -0.99, 0.10],
           'H': [0.08, -0.71, 0.68],
           'I': [-0.77, 0.67, -0.37],
           'L': [-0.92, 0.31, -0.99],
           'K': [-0.63, 0.25, 0.50],
           'M': [-0.80, 0.44, -0.71],
           'F': [0.87, 0.65, -0.53],
           'P': [-0.99, -0.99, -0.99],
           'S': [0.99, 0.40, 0.37],
           'T': [0.42, 0.21, 0.97],
           'W': [-0.13, 0.77, -0.90],
           'Y': [0.59, 0.33, -0.99],
           'V': [-0.99, 0.27, -0.52],
           '*': [0, 0, 0]}
    psp = psp.strip()
    opf7 = []
    for aa in psp:
        if aa not in dic.keys():
            aa = '*'
        tl = dic[aa]
        opf7 = opf7 + tl
    return opf7

def get_AESNN3(seqs, outpath):
    # df = pd.read_csv(file_path,header=0)
    results = list(map(seq2AESNN3, seqs))
    # df_results = pd.DataFrame(results)
    # df_results['Label'] = df['Label'].tolist()
    # df_results.to_csv(outpath + 'AESNN3.csv', index=False)  
    np_results = np.array(results)
    np.save(outpath + 'AESNN3', np_results)
def seq2opf10(psp):
    aa_opf = np.load('/data/www/gps6/webcomp/models/pref/opf10dic.npy', allow_pickle=True)
    # aa_opf = np.load('/home/biocucko/public_html/sumo/gyj/gps6/for_web_test/models/opf10dic.npy', allow_pickle=True)

    aa_opf = aa_opf.item()
    aas = ['A', 'R', 'N', 'D', 'C', 'Q', 'E', 'G', 'H', 'I', 'L', 'K', 'M', 'F', 'P', 'S', 'T', 'W', 'Y', 'V']
    bit10 = []
    for aa in psp:
        if aa not in aas:
            list_tem = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        else:
            list_tem = aa_opf[aa]
        bit10 = bit10 + list_tem
    return bit10
def get_opf10bit(seqs, outpath):
    # df = pd.read_csv(file_path,header=0)
    results = list(map(seq2opf10, seqs))

    # df_results = pd.DataFrame(results)
    # df_results['Label'] = df['Label'].tolist()
    # df_results.to_csv(outpath + 'OPF10bit.csv', index=False)
    np_results = np.array(results)
    np.save(outpath + 'OPF10bit', np_results)

def seq2opf7_3(psp):
    aa_opf = np.load('/data/www/gps6/webcomp/models/pref/opf7_3dic.npy', allow_pickle=True)
    # aa_opf = np.load('/home/biocucko/public_html/sumo/gyj/gps6/for_web_test/models/opf7_3dic.npy', allow_pickle=True)

    aa_opf = aa_opf.item()
    aas = aas = ['A', 'R', 'N', 'D', 'C', 'Q', 'E', 'G', 'H', 'I', 'L', 'K', 'M', 'F', 'P', 'S', 'T', 'W', 'Y', 'V']
    bit7 = []
    for aa in psp:
        if aa not in aas:
            list_tem = [0, 0, 0, 0, 0, 0, 0]
        else:
            list_tem = aa_opf[aa]
        bit7 = bit7 + list_tem
    return bit7

def get_opf7bit3(seqs, outpath):
    # df = pd.read_csv(file_path,header=0)
    results = list(map(seq2opf7_3, seqs))

    # df_results = pd.DataFrame(results)
    # df_results['Label'] = df['Label'].tolist()
    # df_results.to_csv(outpath + 'OPF_7bit_type3.csv', index=False)    
    np_results = np.array(results)
    np.save(outpath + 'OPF_7bit_type3', np_results)
def seq2fts(seq, weights, outpath,KN):
    get_EAAC(seq, outpath)
    get_AAIndex(seq, outpath)
    get_OPF_7bit_1(seq, outpath)
    get_ZScale(seq, outpath)
    get_binary(seq, outpath)
    get_binary5bit2(seq, outpath)
    get_opf7bit3(seq, outpath)
    get_opf10bit(seq, outpath)
    get_AESNN3(seq, outpath)
    getMMScoreTest(seq, weights, outpath,KN)
   
    
def test_predict(feature_path, model_path):
    feature_list = ['OPF_7bit_type1', 'ZScale', 'EAAC', 'AAIndex', 'AESNN3', 'binary', 'binary5bit2', 'OPF_7bit_type3','OPF10bit', 'SMO']  # 
    pred = [] 
    # num = 0
    for fn in feature_list:

        # if fn == 'SMO':
        #     smo = np.load(feature_path + "SMO.npy")
        #     model = model_path + fn + '.txt'
        #     m1 = lgb.Booster(model_file=model)
        #     table = m1.predict(smo)
        #     pred.append(table)  
        #     # num +=1
        #     mdnn = model_path + fn + '.model'
        #     m2 = load_model(mdnn)
        #     table2 = m2.predict(smo)
        #     pred.append(table2)
        #     # roc_plot(label, np.array(table2), path_roc, feature_name, fn+"dnn", num)
        #     # num +=1 
        # else:
        # feature = pd.read_csv(feature_path + fn + '.csv', header=0)
        f = np.load(feature_path + fn+".npy")
        model = model_path + fn + '.txt'
        m1 = lgb.Booster(model_file=model)
        # print("consume time of lgbload:%.2f" % (time.time() - start_time))
        # f = feature.iloc[:, :]
        table = m1.predict(f)

        pred.append(table)        
        # num +=1 
        mdnn = model_path + fn + '.model'
        m2 = load_model(mdnn)
        # print("consume time of dnn:%.2f" % (time.time() - start_time))
        table2 = m2.predict(f)
        pred.append(table2)
            # num +=1 
            
    pred = [[r[col] for r in pred] for col in range(len(pred[0]))]
    pred = np.array(pred)
    comb_ml = model_path + 'comb_LRM' + '.pkl'
    comb_model = joblib.load(comb_ml)
    pred_comb = comb_model.predict_proba(pred)[:, 1]
    
    return pred_comb

def psp2source(psp,kn):
    kn = kn.replace("/","_")
    df = pd.read_csv("/data/www/gps6/psp_source2.txt",header=None)
    psps =df[0].tolist()
    # ks =df[1].tolist()
    # source =df[2].tolist()
    if psp not in set(psps):
        return "Pred."
    else:
      
        df1 = df.loc[df[0]==psp]

        df1 = df1[df1[1].str.contains(kn)]
        ss = df1[2].tolist()
        if len(ss) ==0:
            return "Pred."
        else:
            ss = ss[0]
            if ss.isdigit():
                return "<a href =https://pubmed.ncbi.nlm.nih.gov/%s/  target='_blank'>Exp.</ a></font></td>"%ss
            elif ss == "UniProt":
                return "<a href =https://www.uniprot.org/uniprotkb?query=%s target='_blank'>Exp.</ a></font></td>" % ss
            else:
                return "<a href =https://www.phosphosite.org/simpleSearchSubmitAction.action?searchStr=%s target='_blank'>Exp.</ a></font></td>" % ss


def ids2ppi(id1,id2):
]
    kn = id1
    if '/' in id1:
        kn = id1.rsplit("/", 1)[1]
    df = pd.read_csv("/data/www/gps6/webcomp/kn_b_vname2.txt",sep='\t',header=0)
    df1 = df[(df['KN']==kn) & (df['B'].str.contains(id2))]
    if len(df1) > 0 :
        # print(df2['PMID'].tolist()[0])
        return "<a href =https://pubmed.ncbi.nlm.nih.gov/%s/  target='_blank'>&radic;</ a></font></td>"%df1['PMID'].tolist()[0]
    else:
        return "<a href =https://thebiogrid.org/  target='_blank'>--</ a></font></td>"


def out_format(pred_score,pred_type,threshold,psps,ids,kn,sitedic,locs,outf):
  
    out1 = open(outf, 'a+')
    size = os.path.getsize(outf)
    if size == 0 :
        out1.write("ID\tPosition\tCode\tKinase\tPeptide\tScore\tCutoff\n")
    id2 = ids[0].strip()
    ppi = ids2ppi(kn, id2)
    epsdlink = "<a href =http://epsd.biocuckoo.cn/View.php?id=%s target='_blank'>%s</ a></font></td>" %(sitedic[id2], sitedic[id2])

    for i in range(len(pred_type)):
        if pred_type[i]:
            # epsdlink = "<a href =http://epsd.biocuckoo.cn/View.php?id=%s target='_blank'>%s</ a></font></td>"%(sitedic[ids[i]],sitedic[ids[i]])
            # tem1 = ids[i].strip()+'\t'+str(locs[i]+1)+'\t'+psps[i][30]+'\t'+kn+ '\t'+psps[i][23:38]+'\t'+ '{:.4f}'.format(pred_score[i])+'\t'+str(threshold)+'\t'+epsdlink+'\t' + psps[i]+'\n'
            source = psp2source(psps[i], kn)
            # id2 = ids[i].strip().split('_')[0]
            # ppi = ids2ppi(kn, id2)
            # epsdlink = "<a href =http://epsd.biocuckoo.cn/View.php?id=%s target='_blank'>%s</ a></font></td>" % (sitedic[ids[i]], sitedic[ids[i]])
            tem1 = ids[i].strip() + '\t' + str(locs[i] + 1) + '\t' + psps[i][30] + '\t' + kn + '\t' + psps[i][23:38] + '\t' + '{:.4f}'.format(pred_score[i]) + '\t' + str(threshold) + '\t' + epsdlink +'\t' + psps[i]+ '\t'+source+ '\t'+ ppi+'\n'
            out1.write(tem1)
    out1.close()


if __name__ == '__main__':
    
    threshold= sys.argv[1]  
    treeNode = sys.argv[2]  
    KN="ST"
    G0 = treeNode.split("/,")[0]
    if (G0 == "TK") or (G0.startswith("Dual") and not G0.startswith("Dual/TK")):
        KN = "Y"
    # if G0 =="TK":
    #     KN="Y"
    # if  G1.startswith("Dual") and G1 != "Dual/TK/":
    #     KN="Y"
    upfile =sys.argv[3]     #上传的fasta文件 的路径
    # upfile = "/data/www/gps/webcomp/"  +upfile
    outpath =sys.argv[4]
    # outpath = "/data/www/gps/webcomp/"  +outpath
    outf = outpath
    outpath = outpath.rsplit('/', 1)[0] + '/'
      
    # weights = np.load('/home/biocucko/public_html/gps/webcomp/models/pref/stpwd_weight_norm.npy')
    weights = np.load('/data/www/gps6/webcomp/models/pref/stpwd_weight_norm.npy')
    # model_path = "/home/biocucko/public_html/gps/webcomp/models/ST/"
    model_path = "/data/www/gps6/webcomp/models/ALL/ST/"
    if KN =="Y":
        # weights = np.load('/home/biocucko/public_html/gps/webcomp/models/pref/ypwd_weight_norm.npy')
        # model_path = "/home/biocucko/public_html/gps/webcomp/models/Y/"
        weights = np.load('/data/www/gps6/webcomp/models/pref/ypwd_weight_norm.npy')
        model_path = "/data/www/gps6/webcomp/models/ALL/Y/"
    id_seq, df = fasta2seq(upfile, outpath,KN)

    seq = df['PSP'].tolist()
    ids = df['ID'].tolist()
    locs = df['loc'].tolist()

  

    sitedic = {}

    epsd = pd.read_csv("/data/www/gps6/epsd",header=0)
    for k, v in id_seq.items():

        if k in sitedic.keys():
            break
        epsd_seqs = epsd["seq"].tolist()
        if v in epsd_seqs:
            ep_index = epsd_seqs.index(v)
            sitedic[k] = epsd.loc[ep_index,'id']
        else:
            sitedic[k] = ''


    
    seq2fts(seq,weights,outpath,KN)

    treeNodes = treeNode.split(",")


    
    for k in treeNodes:
        if k == "Dual/" or k == "Atypical/" or k == "Other/" or k == "Dual/Atypical/" or k == "Dual/Other/":
            pass
        else:
            treeN = k.rsplit("/",1)[0]
            knpath = model_path + k
     
            pred_comb = test_predict(outpath, knpath)
    
            if threshold =="a":
                thd = "Null"
            
                pred_type = [1]*len(pred_comb)
                out_format(pred_comb,pred_type,thd, seq, ids,treeN,sitedic,locs,outf)

            else:
                zhibiao = pd.read_csv(knpath+"zhibiao.txt",sep="\t",header=None)
                if threshold == "a":
                    thd = "Null"
                    pred_type = [1] * len(pred_comb)
                    out_format(pred_comb, pred_type, thd, seq, ids, treeN, sitedic, locs, outf)
                else:
                    if threshold == "h":
                        thd = round(float(zhibiao.iloc[0,1]),4)
                    elif threshold == "m":
                        thd = round(float(zhibiao.iloc[1,1]),4)
                    elif threshold == "l":
                        thd = round(float(zhibiao.iloc[2,1]),4)


  

                pred_type = (pred_comb >= thd).astype(bool)
                out_format(pred_comb,pred_type,thd, seq, ids,treeN,sitedic,locs,outf)
        




