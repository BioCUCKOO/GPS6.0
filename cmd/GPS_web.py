# -*- coding: utf-8 -*-

"""
@author: mia
"""
import sys,os,re
import pandas as pd
import numpy as np
import collections
from collections import Counter
import lightgbm as lgb

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
    f2 = f1
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

    return l_scores

def fasta2seq(input,outpath,KN):
    f_fas = open(input, 'r') 
    id_seq = {}
    global linename
    for line in f_fas:
        if line.startswith('>'):
           linename = line.replace('>', '').strip()
           id_seq[linename] = ''
        else:
           id_seq[linename] += line.strip()
    ids = []
    psp61 = []

    for k,v in id_seq.items():
        # print(k,v)
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
    df = pd.DataFrame({'ID':ids,
                       'PSP':psp61,
                       'loc':locs
                       })
    # df.to_csv(outpath + 'psp.csv',index = False) 
    return id_seq, df
    
def test_predict(feature, model_path):
    fn='SMO'
    model = model_path + fn + '.txt'
    m1 = lgb.Booster(model_file=model)
    table = m1.predict(feature)
    pred=table    
    return pred

def out_format(pred_score,pred_type,threshold,psps,ids,kn,sitedic,locs,outf):
   
    out1 = open(outf, 'a+')
    size = os.path.getsize(outf)
    if size == 0 :
        out1.write("ID\tPosition\tCode\tKinase\tPeptide\tScore\tCutoff\n")

    id2 = ids[0].strip()
    ppi = ids2ppi(kn, id2)
    epsdlink = "<a href =http://epsd.biocuckoo.cn/View.php?id=%s target='_blank'>%s</ a></font></td>"%(sitedic[id2],sitedic[id2])

    for i in range(len(pred_type)):
        if pred_type[i]:
            source = psp2source(psps[i], kn,id2)
            tem1 = id2+'\t'+str(locs[i]+1)+'\t'+psps[i][30]+'\t'+kn+ '\t'+psps[i][23:38]+'\t'+ '{:.4f}'.format(pred_score[i])+'\t'+str(threshold)+'\t'+epsdlink+'\t' + psps[i]+ '\t'+source+ '\t'+ ppi+'\n'
   
            out1.write(tem1)
    out1.close()

def psp2source(psp,kn,id2):
    kn = kn.replace("/","_")
    df = pd.read_csv("/data/www/gps6/psp_source2.txt",header=None)
    psps =df[0].tolist()

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
                # print("https://pubmed.ncbi.nlm.nih.gov/" +ss+"/")       return "<a href =https://pubmed.ncbi.nlm.nih.gov/%s/  target='_blank'>Exp.</ a></font></td>"%ss
            elif ss=="UniProt":
           
                return "<a href =https://www.uniprot.org/uniprotkb?query=%s target='_blank'>Exp.</ a></font></td>"%id2
            else:
            
                return "<a href =https://www.phosphosite.org/simpleSearchSubmitAction.action?searchStr=%s target='_blank'>Exp.</ a></font></td>"%id2

def ids2ppi(id1,id2):

    if '/' in id1:
        kn = id1.rsplit("/",1)[1]
    else:
        kn = id1
    df = pd.read_csv("/data/www/gps6/webcomp/kn_b_vname2.txt",sep='\t',header=0)
    df1 = df[(df['KN']==kn) & (df['B'].str.contains(id2))]
    if len(df1) > 0 :
 
        return "<a href =https://pubmed.ncbi.nlm.nih.gov/%s/  target='_blank'>&radic;</ a></font></td>"%df1['PMID'].tolist()[0]
    else:
        return "<a href =https://thebiogrid.org/  target='_blank'>--</ a></font></td>"
    # return "--"

if __name__ == '__main__':
    
    threshold= sys.argv[1]  
    treeNode = sys.argv[2] 

    G0 = treeNode.split("/,")[0]

    KN="ST"
    if (G0 == "TK") or (G0.startswith("Dual") and not G0.startswith("Dual/TK")) :
        KN="Y"
 
    upfile =sys.argv[3]     
    outpath =sys.argv[4]
    outf = outpath
    outpath = outpath.rsplit('/', 1)[0] + '/'

    weights = np.load('/data/www/gps6/webcomp/models/pref/stpwd_weight_norm.npy')
    model_path = "/data/www/gps6/webcomp/models/ALL/ST/"
    if KN =="Y":
        weights = np.load('/data/www/gps6/webcomp/models/pref/ypwd_weight_norm.npy')
        model_path = "/data/www/gps6/webcomp/models/ALL/Y/"
    id_seq, df = fasta2seq(upfile, outpath,KN)
    seq = df['PSP'].tolist()
    ids = df['ID'].tolist()
    locs = df['loc'].tolist()
    np_results =getMMScoreTest(seq,weights,outpath,KN)



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
    print(sitedic)

    treeNodes = treeNode.split(",")
    for k in treeNodes:
        if k=="Dual/" or k=="Atypical/" or k=="Other/" or k=="Dual/Atypical/" or k=="Dual/Other/":
            pass
        elif k=="TK/" or ( k.startswith("Dual") and k!= "Dual/TK/"):
            KN="Y"
            model_path = "/data/www/gps6/webcomp/models/ALL/Y/"
            treeN = k.rsplit("/", 1)[0]
  
            knpath = model_path + k
            thre_path = model_path.replace("ALL", "GPS") + k
 
            zhibiao = pd.read_csv(thre_path + "zhibiao_smo.txt", sep="\t", header=None)
            pred_comb = test_predict(np_results, knpath)

            if threshold == "a":
                thd = "Null"
                pred_type = [1] * len(pred_comb)
                out_format(pred_comb, pred_type, thd, seq, ids, treeN, sitedic, locs, outf)
            else:
                if threshold == "h":
                    thd = round(float(zhibiao.iloc[0, 1]), 4)
                elif threshold == "m":
                    thd = round(float(zhibiao.iloc[1, 1]), 4)
                elif threshold == "l":
                    thd = round(float(zhibiao.iloc[2, 1]), 4)

                pred_type = (pred_comb >= thd).astype(bool)
                out_format(pred_comb, pred_type, thd, seq, ids, treeN, sitedic, locs, outf)
        else:
            treeN = k.rsplit("/",1)[0]
   
            knpath = model_path+ k
            thre_path = model_path.replace("ALL","GPS") + k
            zhibiao = pd.read_csv(thre_path+"zhibiao_smo.txt",sep="\t",header=None)
            pred_comb = test_predict(np_results, knpath)
    
    
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
          




