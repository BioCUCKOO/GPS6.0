"""
@author: mia
"""
import sys ,os ,re ,joblib 
import pandas as pd 
import numpy as np 
import collections 
from collections import Counter 
import lightgbm as lgb 
from keras .models import load_model 
def fasta2seq (OO0OOO00OO000O00O ,OO0000OOO00O000OO ,O000O00O0OOOO0OOO ="ST"):
    OO00OOOOO00O0OO00 =open (OO0OOO00OO000O00O ,'r')
    OO0OO000OOOOO00OO ={}
    global linename 
    for OOO0O0OOO0000OO0O in OO00OOOOO00O0OO00 :
        if OOO0O0OOO0000OO0O .startswith ('>'):
           linename =OOO0O0OOO0000OO0O .replace ('>','').strip ()
           OO0OO000OOOOO00OO [linename ]=''
        else :
           OO0OO000OOOOO00OO [linename ]+=OOO0O0OOO0000OO0O .strip ()
    print (OO0OO000OOOOO00OO )
    OOOOO00O0OO00OO00 =[]
    OOO00O0OO00000000 =[]
    OO0000OOO0OOOOO00 =[]
    for OO0OOO00OO000OO00 ,O00O00O0OOOO00OOO in OO0OO000OOOOO00OO .items ():
        O00O0OOOO00000OOO =[]
        O0000O00O0OO00OOO =[]
        O0OO0O000O0O0O000 ='******************************'
        for OO00O0OOO0O000OOO in range (len (O00O00O0OOOO00OOO )):
            if O000O00O0OOOO0OOO =="ST"and O00O00O0OOOO00OOO [OO00O0OOO0O000OOO ]!="S"and O00O00O0OOOO00OOO [OO00O0OOO0O000OOO ]!="T":
                pass 
            elif O000O00O0OOOO0OOO =="Y"and O00O00O0OOOO00OOO [OO00O0OOO0O000OOO ]!="Y":
                pass 
            else :
                if OO00O0OOO0O000OOO <30 :
                    OO0O0OO0000O00O00 =O0OO0O000O0O0O000 [:(30 -OO00O0OOO0O000OOO )]
                    OO0OOO0O0OO00O0O0 =O00O00O0OOOO00OOO [:OO00O0OOO0O000OOO +31 ]
                    OO0O0OO0000O00O00 =OO0O0OO0000O00O00 +OO0OOO0O0OO00O0O0 
                    if len (OO0O0OO0000O00O00 )<61 :
                        O0O00000OO0000O0O =O0OO0O000O0O0O000 [:(61 -len (OO0O0OO0000O00O00 ))]
                        OO0O0OO0000O00O00 =OO0O0OO0000O00O00 +O0O00000OO0000O0O 
                elif OO00O0OOO0O000OOO >=(len (O00O00O0OOOO00OOO )-30 ):
                    OO0O0OO0000O00O00 =O00O00O0OOOO00OOO [(OO00O0OOO0O000OOO -30 ):(len (O00O00O0OOOO00OOO ))]
                    OO0OOO0O0OO00O0O0 =O0OO0O000O0O0O000 [:(30 -(len (O00O00O0OOOO00OOO )-OO00O0OOO0O000OOO -1 ))]
                    OO0O0OO0000O00O00 =OO0O0OO0000O00O00 +OO0OOO0O0OO00O0O0 
                else :
                    OO0O0OO0000O00O00 =O00O00O0OOOO00OOO [OO00O0OOO0O000OOO -30 :OO00O0OOO0O000OOO +31 ]
                O00O0OOOO00000OOO .append (OO0O0OO0000O00O00 )
                O0000O00O0OO00OOO .append (OO00O0OOO0O000OOO )
        OOOOO00O0OO00OO00 .extend ([OO0OOO00OO000OO00 ]*len (O00O0OOOO00000OOO ))
        OOO00O0OO00000000 .extend (O00O0OOOO00000OOO )
        OO0000OOO0OOOOO00 .extend (O0000O00O0OO00OOO )
    OOOOOO00O0OOOOO0O =pd .DataFrame ({'ID':OOOOO00O0OO00OO00 ,'PSP':OOO00O0OO00000000 ,'loc':OO0000OOO0OOOOO00 })
    return OO0OO000OOOOO00OO ,OOOOOO00O0OOOOO0O 
def getblosum62 ():
    OO0OO0O00OOO00OOO =open ('/data/www/gps6/webcomp/models/pref/BLOSUM62','r')
    OO00O0O00O000O00O =[]
    O0OOOO0O00OOO0O00 =[]
    O00OOOOO0O0O000O0 ={}
    for O0000OO0O000O0OOO in OO0OO0O00OOO00OOO .readlines ():
        OO0O0O0O00OOOOO0O =O0000OO0O000O0OOO .split ()
        O0O00OO0OO00OOO00 =OO0O0O0O00OOOOO0O [0 ]
        O0OOOO0O00OOO0O00 .append (O0O00OO0OO00OOO00 )
    OO0OO0O00OOO00OOO .close ()
    OO00OOO000000OOO0 =open ('/data/www/gps6/webcomp/models/pref/BLOSUM62','r')
    OOOOOO0O000OOO0O0 =0 
    for O0000OO0O000O0OOO in OO00OOO000000OOO0 .readlines ():
        OO0O0O0O00OOOOO0O =O0000OO0O000O0OOO .strip ()
        OO0O0O0O00OOOOO0O =O0000OO0O000O0OOO .split ()
        for OO0000O0O00000OOO in range (len (OO0O0O0O00OOOOO0O )):
            if OO0000O0O00000OOO ==0 :
                continue 
            else :
                OOOO0O0O0OOOOOO0O =float (OO0O0O0O00OOOOO0O [OO0000O0O00000OOO ])
                OO000O000OOOOOO0O =O0OOOO0O00OOO0O00 [OOOOOO0O000OOO0O0 ]+"_"+O0OOOO0O00OOO0O00 [OO0000O0O00000OOO -1 ]
                OOOO0OO0000OO0O0O =O0OOOO0O00OOO0O00 [OO0000O0O00000OOO -1 ]+"_"+O0OOOO0O00OOO0O00 [OOOOOO0O000OOO0O0 ]
                if OO000O000OOOOOO0O not in OO00O0O00O000O00O and OOOO0OO0000OO0O0O not in OO00O0O00O000O00O :
                    OO00O0O00O000O00O .append (OO000O000OOOOOO0O )
                    O00OOOOO0O0O000O0 [OO000O000OOOOOO0O ]=OOOO0O0O0OOOOOO0O 
        OOOOOO0O000OOO0O0 +=1 
    OO00OOO000000OOO0 .close ()
    return O00OOOOO0O0O000O0 ,OO00O0O00O000O00O ,O0OOOO0O00OOO0O00 
def getArray (O00O00OO0000OO00O ):
    OOOO0000O00000O0O =[]
    for OO0000OO00OOO0OO0 in range (len (O00O00OO0000OO00O )):
        OOOO0000O00000O0O .append (0.0 )
    O0OO0OOO0000O0O00 =np .array (OOOO0000O00000O0O )
    return O0OO0OOO0000O0O00 
def getMMScoreTest (OOO0OOO0O00OOO000 ,OOOOOO00000OO0O0O ,O0O0O0O00OOO00OOO ,O00OOO000OOOO00O0 ="ST"):
    OO0O0O00OOOO00OO0 ,OOOO00OOOO0O0O00O ,OOO0O000OOOOO00OO =getblosum62 ()
    if O00OOO000OOOO00O0 =="ST":
        O0O00O0OO0OO0O0O0 =np .load ("/data/www/gps6/webcomp/models/pref/stpos_smoscores.npy",allow_pickle =True )
    else :
        O0O00O0OO0OO0O0O0 =np .load ("/data/www/gps6/webcomp/models/pref/ypos_smoscores.npy",allow_pickle =True )
    O00OO000OOO0O0O00 =[]
    for OO0O00OOOOO00OOOO in OOO0OOO0O00OOO000 :
        O000O00O00000000O =getArray (OOOO00OOOO0O0O00O )
        for OO00000O0OO000OOO in range (len (OO0O00OOOOO00OOOO )):
            OO0000000OOO0O0OO =OO0O00OOOOO00OOOO [OO00000O0OO000OOO ]
            if OO0000000OOO0O0OO not in OOO0O000OOOOO00OO :
                OO0000000OOO0O0OO ='*'
            OOOOO0O000OO000OO =OOO0O000OOOOO00OO .index (OO0000000OOO0O0OO )
            OOOO000O00OO0O0O0 =O0O00O0OO0OO0O0O0 [OO00000O0OO000OOO ][OOOOO0O000OO000OO ]
            O000O00O00000000O =O000O00O00000000O +OOOO000O00OO0O0O0 
        O000O00O00000000O =(O000O00O00000000O /(len (O0O00O0OO0OO0O0O0 ))).tolist ()
        O00OO000OOO0O0O00 .append (O000O00O00000000O )
    O00OO000OOO0O0O00 =np .float16 (O00OO000OOO0O0O00 )
    np .save (O0O0O0O00OOO00OOO +'SMO',O00OO000OOO0O0O00 )
def is_aa (OO0OO0000OO00000O ):
    O0O00O0000OOOOO00 =['A','R','N','D','C','Q','E','G','H','I','L','K','M','F','P','S','T','W','Y','V','*']
    if OO0OO0000OO00000O in O0O00O0000OOOOO00 :
        return OO0OO0000OO00000O 
    else :
        return '*'
def window_slide (OOOO0OO0O00000000 ):
    O00O0OO0O00OO00OO =[]
    O0O000OOO00O0O0OO =['A','R','N','D','C','Q','E','G','H','I','L','K','M','F','P','S','T','W','Y','V','*']
    OO00OOO0O00OOOOO0 =collections .OrderedDict ()
    OO00OOO0O00OOOOO0 =OO00OOO0O00OOOOO0 .fromkeys (O0O000OOO00O0O0OO ,0 )
    OOOO0OO0O00000000 =list (OOOO0OO0O00000000 .replace (" ",""))
    for O000O000OOOO00000 in range (len (OOOO0OO0O00000000 )):
        if OOOO0OO0O00000000 [O000O000OOOO00000 ]not in O0O000OOO00O0O0OO :
            OOOO0OO0O00000000 [O000O000OOOO00000 ]='*'
    OOOO0OO0O00000000 =list (map (is_aa ,OOOO0OO0O00000000 ))
    for O000O000OOOO00000 in range (len (OOOO0OO0O00000000 )):
        if O000O000OOOO00000 <57 :
            O000OO0O00OOO0000 =list (OOOO0OO0O00000000 [O000O000OOOO00000 :O000O000OOOO00000 +5 ])
            OOO00O0O0O0OO0000 =Counter (O000OO0O00OOO0000 )
            O0OOO0O0O0O0O0OOO ={**OO00OOO0O00OOOOO0 ,**OOO00O0O0O0OO0000 }
            OO0OO0OOO00OO00O0 =list (O0OOO0O0O0O0O0OOO .values ())
            OO0OO0OOO00OO00O0 =list (map (lambda OO0000O00O0000O0O :(OO0000O00O0000O0O /5 ),OO0OO0OOO00OO00O0 ))
            O00O0OO0O00OO00OO =O00O0OO0O00OO00OO +OO0OO0OOO00OO00O0 
        else :
            break 
    return O00O0OO0O00OO00OO 
def get_EAAC (O000OO0O00O0O0O0O ,OOO0O000OO00O00O0 ):
    OOOOOO00OOOOOOO00 =list (map (window_slide ,O000OO0O00O0O0O0O ))
    O0OOOO00O0OOOOOOO =np .array (OOOOOO00OOOOOOO00 )
    np .save (OOO0O000OO00O00O0 +'EAAC',O0OOOO00O0OOOOOOO )
def seq2Z (OO0OOO0OOO0OO00OO ):
    O0O0O0OO00O00O00O =[0.24 ,-2.32 ,0.60 ,-0.14 ,1.30 ]
    O0OOO00OOOOOOOOOO =[-2.85 ,-0.22 ,0.47 ,1.94 ,-0.98 ]
    OO00O00OO000O00OO =[0.84 ,-1.67 ,3.71 ,0.18 ,-2.65 ]
    OO0OOO0O0OOO000OO =[3.05 ,1.60 ,1.04 ,-1.15 ,1.61 ]
    OOOOOOOO00OOOOO0O =[3.98 ,0.93 ,1.93 ,-2.46 ,0.75 ]
    O0OO00OOO0OO0O000 =[-1.66 ,0.27 ,1.84 ,0.70 ,2.00 ]
    O00O0OOO0O00OOO0O =[3.11 ,0.26 ,-0.11 ,-3.04 ,-0.25 ]
    O00O0O000OO0000O0 =[1.75 ,0.50 ,-1.44 ,-1.34 ,0.66 ]
    O00000000O0OOO0O0 =[-4.22 ,1.94 ,1.06 ,0.54 ,-0.62 ]
    O0O0O0O0O0O000OOO =[3.52 ,2.50 ,-3.50 ,1.99 ,-0.17 ]
    O0O0O000OOOO00O0O =[2.05 ,4.06 ,0.36 ,-0.82 ,-0.38 ]
    O00O0O0OOOO00O0OO =[2.39 ,-1.07 ,1.15 ,-1.39 ,0.67 ]
    O0O0O00O00O000O00 =[2.47 ,1.95 ,0.26 ,3.90 ,0.09 ]
    O000OOO0OOO0OOOOO =[0.75 ,-2.18 ,-1.12 ,-1.46 ,-0.40 ]
    OO0O0OO000O000O0O =[-3.89 ,-1.73 ,-1.71 ,-0.84 ,0.26 ]
    O0O0OO0000O0O00O0 =[-2.59 ,-2.64 ,-1.54 ,-0.85 ,-0.02 ]
    O00O0OO0OO000OOOO =[2.29 ,0.89 ,-2.49 ,1.49 ,0.31 ]
    O00O0O0OOOOO0000O =[-4.36 ,3.94 ,0.59 ,3.44 ,-1.59 ]
    OOOO000O0O0000000 =[-4.28 ,-1.30 ,-1.49 ,-0.72 ,0.84 ]
    O0OOOOOO0O0OO000O =[-2.54 ,2.44 ,0.43 ,0.04 ,-1.47 ]
    O0OOO0OOO00O0O0O0 =[0 ,0 ,0 ,0 ,0 ]
    O000OO00O0O0O00O0 =['A','R','N','D','C','Q','E','G','H','I','L','K','M','F','P','S','T','W','Y','V']
    OOO000O0OO0000000 ={'A':O0O0O0OO00O00O00O ,'M':O0OOO00OOOOOOOOOO ,'C':OO00O00OO000O00OO ,'N':OO0OOO0O0OOO000OO ,'D':OOOOOOOO00OOOOO0O ,'P':O0OO00OOO0OO0O000 ,'E':O00O0OOO0O00OOO0O ,'Q':O00O0O000OO0000O0 ,'F':O00000000O0OOO0O0 ,'R':O0O0O0O0O0O000OOO ,'G':O0O0O000OOOO00O0O ,'S':O00O0O0OOOO00O0OO ,'H':O0O0O00O00O000O00 ,'T':O000OOO0OOO0OOOOO ,'I':OO0O0OO000O000O0O ,'V':O0O0OO0000O0O00O0 ,'K':O00O0OO0OO000OOOO ,'W':O00O0O0OOOOO0000O ,'L':OOOO000O0O0000000 ,'Y':O0OOOOOO0O0OO000O ,'*':O0OOO0OOO00O0O0O0 }
    O00000000OO00O0O0 =[]
    OO0OOO0OOO0OO00OO =OO0OOO0OOO0OO00OO .strip ()
    for O000O0OO00O0O0O00 in OO0OOO0OOO0OO00OO :
        if O000O0OO00O0O0O00 not in O000OO00O0O0O00O0 :
            O000O0OO00O0O0O00 ='*'
        O0OOOOO0OO000000O =OOO000O0OO0000000 [O000O0OO00O0O0O00 ]
        O00000000OO00O0O0 =O00000000OO00O0O0 +O0OOOOO0OO000000O 
    return O00000000OO00O0O0 
def get_ZScale (O00000OO000O00000 ,OOOO0O0OOOOOO0O0O ):
    O0O00OOOOOO0000O0 =list (map (seq2Z ,O00000OO000O00000 ))
    O000000OOOO00OO00 =np .array (O0O00OOOOOO0000O0 )
    np .save (OOOO0O0OOOOOO0O0O +'ZScale',O000000OOOO00OO00 )
def seq2index (OOOO000O0O0O00O0O ):
    OOOOO0O0OOO0O00OO =np .load ('/data/www/gps6/webcomp/models/pref/aaidx_dic.npy',allow_pickle =True )
    OOOOO0O0OOO0O00OO =OOOOO0O0OOO0O00OO .item ()
    OOO0OO0O00O0OO00O =[]
    O0OOO00O00OOO00OO =['A','R','N','D','C','Q','E','G','H','I','L','K','M','F','P','S','T','W','Y','V']
    for OOOO00OO00OO0OO00 in OOOO000O0O0O00O0O :
        if OOOO00OO00OO0OO00 not in O0OOO00O00OOO00OO :
            OOOO00OO00OO0OO00 ='*'
        OO0OO00OOOO0000O0 =OOOOO0O0OOO0O00OO [OOOO00OO00OO0OO00 ]
        OOO0OO0O00O0OO00O =OOO0OO0O00O0OO00O +OO0OO00OOOO0000O0 
    return OOO0OO0O00O0OO00O 
def get_AAIndex (OO0OO0O00OO0OOO00 ,O0OO0OO0OOO0OO0O0 ):
    OOOO000O0O000O000 =list (map (seq2index ,OO0OO0O00OO0OOO00 ))
    OO00OOO0OO0OO0OO0 =np .array (OOOO000O0O000O000 )
    np .save (O0OO0OO0OOO0OO0O0 +'AAIndex',OO00OOO0OO0OO0OO0 )
def seq2bit (O0OOOO00O00000O0O ):
    O000O00OOOO0O0OOO =['A','R','N','D','C','Q','E','G','H','I','L','K','M','F','P','S','T','W','Y','V']
    OOOOO0O00OO0OOO0O =np .load ('/data/www/gps6/webcomp/models/pref/opf71_dic.npy',allow_pickle =True )
    OOOOO0O00OO0OOO0O =OOOOO0O00OO0OOO0O .item ()
    O0OO0O0OO0O000OO0 =[]
    for OO0000O000000O00O in O0OOOO00O00000O0O :
        if OO0000O000000O00O not in O000O00OOOO0O0OOO :
            OO0O00OO0O0O00000 =[0 ,0 ,0 ,0 ,0 ,0 ,0 ]
        else :
            OO0O00OO0O0O00000 =OOOOO0O00OO0OOO0O [OO0000O000000O00O ]
        O0OO0O0OO0O000OO0 =O0OO0O0OO0O000OO0 +OO0O00OO0O0O00000 
    return O0OO0O0OO0O000OO0 
def get_OPF_7bit_1 (OOO000OO00O00O0O0 ,OO0O00O0O00000000 ):
    OOO000O00000O00O0 =list (map (seq2bit ,OOO000OO00O00O0O0 ))
    O00O000000000OO0O =np .array (OOO000O00000O00O0 )
    np .save (OO0O00O0O00000000 +'OPF_7bit_type1',O00O000000000OO0O )
def onehot (O0000OOOOOO000O00 ):
    O000000O0O0OO0000 =['*','A','B','C','D','E','F','G','H','I','K','L','M','N','P','Q','R','S','T','V','W','X','Y','Z']
    OO0OOOO0O0OO000O0 =np .load ("/data/www/gps6/webcomp/models/pref/bny_dic.npy",allow_pickle =True )
    OO0OOOO0O0OO000O0 =OO0OOOO0O0OO000O0 .item ()
    O0000OOOOOO000O00 =list (O0000OOOOOO000O00 )
    for OO0OO0O00OO0O0O00 in range (len (O0000OOOOOO000O00 )):
        if O0000OOOOOO000O00 [OO0OO0O00OO0O0O00 ]not in O000000O0O0OO0000 :
            O0000OOOOOO000O00 [OO0OO0O00OO0O0O00 ]='*'
    O0000OOOOOO000O00 ="".join (O0000OOOOOO000O00 )
    OOOOOO0OOO0O000OO =[OO0OOOO0O0OO000O0 [O0000OOOOO00000O0 ]for O0000OOOOO00000O0 in O0000OOOOOO000O00 ]
    OOOO00O0O00O00O00 =list ()
    for OO0OOOOO000O0OO00 in OOOOOO0OOO0O000OO :
        OO00000OO0O0O0O00 =[0 for _OOOOOOOOOOO00000O in range (len (O000000O0O0OO0000 ))]
        OO00000OO0O0O0O00 [OO0OOOOO000O0OO00 ]=1 
        OOOO00O0O00O00O00 =OOOO00O0O00O00O00 +OO00000OO0O0O0O00 
    return OOOO00O0O00O00O00 
def get_binary (O0OO0O00OOOOOO0O0 ,OOOOO00O00OOOOO0O ):
    O00OO000OOO00000O =list (map (onehot ,O0OO0O00OOOOOO0O0 ))
    O000OO0OOO0OO0OOO =np .array (O00OO000OOO00000O )
    np .save (OOOOO00O00OOOOO0O +'binary',O000OO0OOO0OO0OOO )
def seq2bit5 (OO000OOOO0OOOO00O ):
    OOO00OO0O00000O00 ={'A':[0 ,0 ,0 ,1 ,1 ],'C':[0 ,0 ,1 ,0 ,1 ],'D':[0 ,0 ,1 ,1 ,0 ],'E':[0 ,0 ,1 ,1 ,1 ],'F':[0 ,1 ,0 ,0 ,1 ],'G':[0 ,1 ,0 ,1 ,0 ],'H':[0 ,1 ,0 ,1 ,1 ],'I':[0 ,1 ,1 ,0 ,0 ],'K':[0 ,1 ,1 ,0 ,1 ],'L':[0 ,1 ,1 ,1 ,0 ],'M':[1 ,0 ,0 ,0 ,1 ],'N':[1 ,0 ,0 ,1 ,0 ],'P':[1 ,0 ,0 ,1 ,1 ],'Q':[1 ,0 ,1 ,0 ,0 ],'R':[1 ,0 ,1 ,0 ,1 ],'S':[1 ,0 ,1 ,1 ,0 ],'T':[1 ,1 ,0 ,0 ,0 ],'V':[1 ,1 ,0 ,0 ,1 ],'W':[1 ,1 ,0 ,1 ,0 ],'Y':[1 ,1 ,1 ,0 ,0 ],'*':[0 ,0 ,0 ,0 ,0 ]}
    OO000OOOO0OOOO00O =OO000OOOO0OOOO00O .strip ()
    OOO0O0OOOOOO0OO0O =[]
    for O0OOO0OO0O000O0OO in OO000OOOO0OOOO00O :
        if O0OOO0OO0O000O0OO not in OOO00OO0O00000O00 .keys ():
            O0OOO0OO0O000O0OO ='*'
        O000OO0O0OO0O0OOO =OOO00OO0O00000O00 [O0OOO0OO0O000O0OO ]
        OOO0O0OOOOOO0OO0O =OOO0O0OOOOOO0OO0O +O000OO0O0OO0O0OOO 
    return OOO0O0OOOOOO0OO0O 
def get_binary5bit2 (O0000OOO000000OO0 ,O0O00O0O00OO0OOOO ):
    OO0O0OO0OO0O0O00O =list (map (seq2bit5 ,O0000OOO000000OO0 ))
    O0000OO0OO0O000O0 =np .array (OO0O0OO0OO0O0O00O )
    np .save (O0O00O0O00OO0OOOO +'binary5bit2',O0000OO0OO0O000O0 )
def seq2AESNN3 (O00O00000OOO0000O ):
    O00O00OOO0O0O0O00 ={'A':[-0.99 ,-0.61 ,0.00 ],'R':[0.28 ,-0.99 ,-0.22 ],'N':[0.77 ,-0.24 ,0.59 ],'D':[0.74 ,-0.72 ,-0.35 ],'C':[0.34 ,0.88 ,0.35 ],'Q':[0.12 ,-0.99 ,-0.99 ],'E':[0.59 ,-0.55 ,-0.99 ],'G':[-0.79 ,-0.99 ,0.10 ],'H':[0.08 ,-0.71 ,0.68 ],'I':[-0.77 ,0.67 ,-0.37 ],'L':[-0.92 ,0.31 ,-0.99 ],'K':[-0.63 ,0.25 ,0.50 ],'M':[-0.80 ,0.44 ,-0.71 ],'F':[0.87 ,0.65 ,-0.53 ],'P':[-0.99 ,-0.99 ,-0.99 ],'S':[0.99 ,0.40 ,0.37 ],'T':[0.42 ,0.21 ,0.97 ],'W':[-0.13 ,0.77 ,-0.90 ],'Y':[0.59 ,0.33 ,-0.99 ],'V':[-0.99 ,0.27 ,-0.52 ],'*':[0 ,0 ,0 ]}
    O00O00000OOO0000O =O00O00000OOO0000O .strip ()
    OO00O0O0O0O00O00O =[]
    for OO00OO0O0O00O0OOO in O00O00000OOO0000O :
        if OO00OO0O0O00O0OOO not in O00O00OOO0O0O0O00 .keys ():
            OO00OO0O0O00O0OOO ='*'
        OO000O0OO0OO0O0O0 =O00O00OOO0O0O0O00 [OO00OO0O0O00O0OOO ]
        OO00O0O0O0O00O00O =OO00O0O0O0O00O00O +OO000O0OO0OO0O0O0 
    return OO00O0O0O0O00O00O 
def get_AESNN3 (OOOO0O0O0O00OOOO0 ,O00O0O0OO0O0OOOOO ):
    O0000OO0O00OO0000 =list (map (seq2AESNN3 ,OOOO0O0O0O00OOOO0 ))
    O0000OOOOOOOOOOOO =np .array (O0000OO0O00OO0000 )
    np .save (O00O0O0OO0O0OOOOO +'AESNN3',O0000OOOOOOOOOOOO )
def seq2opf10 (O0OO0OO0OO0OOO0OO ):
    OOOOO000O0O0000OO =np .load ('/data/www/gps6/webcomp/models/pref/opf10dic.npy',allow_pickle =True )
    OOOOO000O0O0000OO =OOOOO000O0O0000OO .item ()
    O00O0O0OO000000O0 =['A','R','N','D','C','Q','E','G','H','I','L','K','M','F','P','S','T','W','Y','V']
    O0000OOO0OO0O00OO =[]
    for OOO000O0O0OO00000 in O0OO0OO0OO0OOO0OO :
        if OOO000O0O0OO00000 not in O00O0O0OO000000O0 :
            OO00OOOO0OOOOOO0O =[0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ]
        else :
            OO00OOOO0OOOOOO0O =OOOOO000O0O0000OO [OOO000O0O0OO00000 ]
        O0000OOO0OO0O00OO =O0000OOO0OO0O00OO +OO00OOOO0OOOOOO0O 
    return O0000OOO0OO0O00OO 
def get_opf10bit (OOOO00O00O0O00OO0 ,O0OO0O0O000OO00O0 ):
    OO0OO000O0OO0OO0O =list (map (seq2opf10 ,OOOO00O00O0O00OO0 ))
    O0000OOO0OO0O0O0O =np .array (OO0OO000O0OO0OO0O )
    np .save (O0OO0O0O000OO00O0 +'OPF10bit',O0000OOO0OO0O0O0O )
    
def seq2opf7_3 (OOOOO00O00OO0OOOO ):
    O0O000OOO0OOO00O0 =np .load ('/data/www/gps6/webcomp/models/pref/opf7_3dic.npy',allow_pickle =True )
    O0O000OOO0OOO00O0 =O0O000OOO0OOO00O0 .item ()
    OO0OOOOO000OOOO0O =OO0OOOOO000OOOO0O =['A','R','N','D','C','Q','E','G','H','I','L','K','M','F','P','S','T','W','Y','V']
    O0O000OOOOOO000OO =[]
    for OOO0O0000O0O0000O in OOOOO00O00OO0OOOO :
        if OOO0O0000O0O0000O not in OO0OOOOO000OOOO0O :
            OOO0O0OO00OOOO000 =[0 ,0 ,0 ,0 ,0 ,0 ,0 ]
        else :
            OOO0O0OO00OOOO000 =O0O000OOO0OOO00O0 [OOO0O0000O0O0000O ]
        O0O000OOOOOO000OO =O0O000OOOOOO000OO +OOO0O0OO00OOOO000 
    return O0O000OOOOOO000OO 
def get_opf7bit3 (O0OOO0OO00000OOOO ,O000OO00OO000O00O ):
    O00OOOO0OO000OO00 =list (map (seq2opf7_3 ,O0OOO0OO00000OOOO ))
    O00OOOO0O0O00OOOO =np .array (O00OOOO0OO000OO00 )
    np .save (O000OO00OO000O00O +'OPF_7bit_type3',O00OOOO0O0O00OOOO )
def seq2fts (O000O0O0OO0O00000 ,OOOO000O0OO0O00O0 ,OOO0OOOO00000O000 ,O0O0O0O0O00O0O000 ):
    get_EAAC (O000O0O0OO0O00000 ,OOO0OOOO00000O000 )
    get_AAIndex (O000O0O0OO0O00000 ,OOO0OOOO00000O000 )
    get_OPF_7bit_1 (O000O0O0OO0O00000 ,OOO0OOOO00000O000 )
    get_ZScale (O000O0O0OO0O00000 ,OOO0OOOO00000O000 )
    get_binary (O000O0O0OO0O00000 ,OOO0OOOO00000O000 )
    get_binary5bit2 (O000O0O0OO0O00000 ,OOO0OOOO00000O000 )
    get_opf7bit3 (O000O0O0OO0O00000 ,OOO0OOOO00000O000 )
    get_opf10bit (O000O0O0OO0O00000 ,OOO0OOOO00000O000 )
    get_AESNN3 (O000O0O0OO0O00000 ,OOO0OOOO00000O000 )
    getMMScoreTest (O000O0O0OO0O00000 ,OOOO000O0OO0O00O0 ,OOO0OOOO00000O000 ,O0O0O0O0O00O0O000 )

def test_predict (OOO00OOO000OO000O ,O0OO0O000OOOO00O0 ):
    OO00O0OO0OO00O0OO =['OPF_7bit_type1','ZScale','EAAC','AAIndex','AESNN3','binary','binary5bit2','OPF_7bit_type3','OPF10bit','SMO']
    OO0OOOO0O0O0000O0 =[]
    for O0O00O000OOOOOOO0 in OO00O0OO0OO00O0OO :
        OO0O0OO0O0000OO00 =np .load (OOO00OOO000OO000O +O0O00O000OOOOOOO0 +".npy")
        OO0OO0000000OO0OO =O0OO0O000OOOO00O0 +O0O00O000OOOOOOO0 +'.txt'
        OOOOOO0OO0000OOO0 =lgb .Booster (model_file =OO0OO0000000OO0OO )
        OO00OO00OOOO000O0 =OOOOOO0OO0000OOO0 .predict (OO0O0OO0O0000OO00 )
        OO0OOOO0O0O0000O0 .append (OO00OO00OOOO000O0 )
        O0O0O000O00OO00O0 =O0OO0O000OOOO00O0 +O0O00O000OOOOOOO0 +'.model'
        OO0O0OOOO00O0000O =load_model (O0O0O000O00OO00O0 )
        OO000O0O000OO0O0O =OO0O0OOOO00O0000O .predict (OO0O0OO0O0000OO00 )
        OO0OOOO0O0O0000O0 .append (OO000O0O000OO0O0O )
    OO0OOOO0O0O0000O0 =[[O0OO0OOO0O0000OO0 [O000O000O0O0OOO00 ]for O0OO0OOO0O0000OO0 in OO0OOOO0O0O0000O0 ]for O000O000O0O0OOO00 in range (len (OO0OOOO0O0O0000O0 [0 ]))]
    OO0OOOO0O0O0000O0 =np .array (OO0OOOO0O0O0000O0 )
    OOOOOOOOO0O0OO00O =O0OO0O000OOOO00O0 +'comb_LRM'+'.pkl'
    O00000OOO0OO000O0 =joblib .load (OOOOOOOOO0O0OO00O )
    OO0O000OOOOO000O0 =O00000OOO0OO000O0 .predict_proba (OO0OOOO0O0O0000O0 )[:,1 ]
    return OO0O000OOOOO000O0 
def psp2source (O0OO00000OOO00OOO ,OOO0000OO0O00O0O0 ):
    OOO0000OO0O00O0O0 =OOO0000OO0O00O0O0 .replace ("/","_")
    OO0OOOOO0O00O00O0 =pd .read_csv ("/data/www/gps6/psp_source2.txt",header =None )
    O0000OOO0OO00OO00 =OO0OOOOO0O00O00O0 [0 ].tolist ()
    if O0OO00000OOO00OOO not in set (O0000OOO0OO00OO00 ):
        return "Pred."
    else :
        OOOOOOO0O00000OOO =OO0OOOOO0O00O00O0 .loc [OO0OOOOO0O00O00O0 [0 ]==O0OO00000OOO00OOO ]
        OOOOOOO0O00000OOO =OOOOOOO0O00000OOO [OOOOOOO0O00000OOO [1 ].str .contains (OOO0000OO0O00O0O0 )]
        O00O00OO00O0O00O0 =OOOOOOO0O00000OOO [2 ].tolist ()
        if len (O00O00OO00O0O00O0 )==0 :
            return "Pred."
        else :
            O00O00OO00O0O00O0 =O00O00OO00O0O00O0 [0 ]
            if O00O00OO00O0O00O0 .isdigit ():
                return "<a href =https://pubmed.ncbi.nlm.nih.gov/%s/  target='_blank'>Exp.</ a></font></td>"%O00O00OO00O0O00O0 
            elif O00O00OO00O0O00O0 =="UniProt":
                return "<a href =https://www.uniprot.org/uniprotkb?query=%s target='_blank'>Exp.</ a></font></td>"%O00O00OO00O0O00O0 
            else :
                return "<a href =https://www.phosphosite.org/simpleSearchSubmitAction.action?searchStr=%s target='_blank'>Exp.</ a></font></td>"%O00O00OO00O0O00O0 
def ids2ppi (OO00O0OOO000OO0OO ,OOOO0OOO0O0O0OOOO ):
    O0O0OO000OO0000O0 =OO00O0OOO000OO0OO 
    if '/'in OO00O0OOO000OO0OO :
        O0O0OO000OO0000O0 =OO00O0OOO000OO0OO .rsplit ("/",1 )[1 ]
    OO000OOO00O00OOO0 =pd .read_csv ("/data/www/gps6/webcomp/kn_b_vname2.txt",sep ='\t',header =0 )
    OOO0O00OOO0O00O00 =OO000OOO00O00OOO0 [(OO000OOO00O00OOO0 ['KN']==O0O0OO000OO0000O0 )&(OO000OOO00O00OOO0 ['B'].str .contains (OOOO0OOO0O0O0OOOO ))]
    if len (OOO0O00OOO0O00O00 )>0 :
        return "<a href =https://pubmed.ncbi.nlm.nih.gov/%s/  target='_blank'>&radic;</ a></font></td>"%OOO0O00OOO0O00O00 ['PMID'].tolist ()[0 ]
    else :
        return "<a href =https://thebiogrid.org/  target='_blank'>--</ a></font></td>"
def out_format (OO00OO0O0000OO0O0 ,OOOO00O00OOO0OO00 ,O0O00000OO0O00OOO ,OOO0OO0OOOO0O00OO ,O0O0OO0OOO0000O00 ,O000O0O0000O0O0O0 ,OOO000OOOOOO00O00 ,OOOOO0OOO0O00000O ,O0O00OOO0O0OO0O00 ):
    O0O00OO00OO0OO00O =open (O0O00OOO0O0OO0O00 ,'a+')
    O00O0O00O0000OO0O =os .path .getsize (O0O00OOO0O0OO0O00 )
    if O00O0O00O0000OO0O ==0 :
        O0O00OO00OO0OO00O .write ("ID\tPosition\tCode\tKinase\tPeptide\tScore\tCutoff\n")
    OO0OO0O00O00OOOO0 =O0O0OO0OOO0000O00 [0 ].strip ()
    O0OO00000O000000O =ids2ppi (O000O0O0000O0O0O0 ,OO0OO0O00O00OOOO0 )
    O0OOO00000O0O000O ="<a href =http://epsd.biocuckoo.cn/View.php?id=%s target='_blank'>%s</ a></font></td>"%(OOO000OOOOOO00O00 [OO0OO0O00O00OOOO0 ],OOO000OOOOOO00O00 [OO0OO0O00O00OOOO0 ])
    for OO00O0OO0O0OO0000 in range (len (OOOO00O00OOO0OO00 )):
        if OOOO00O00OOO0OO00 [OO00O0OO0O0OO0000 ]:
            O0000OOOO0OOO00OO =psp2source (OOO0OO0OOOO0O00OO [OO00O0OO0O0OO0000 ],O000O0O0000O0O0O0 )
            OOOO0O0O0O0OOO000 =O0O0OO0OOO0000O00 [OO00O0OO0O0OO0000 ].strip ()+'\t'+str (OOOOO0OOO0O00000O [OO00O0OO0O0OO0000 ]+1 )+'\t'+OOO0OO0OOOO0O00OO [OO00O0OO0O0OO0000 ][30 ]+'\t'+O000O0O0000O0O0O0 +'\t'+OOO0OO0OOOO0O00OO [OO00O0OO0O0OO0000 ][23 :38 ]+'\t'+'{:.4f}'.format (OO00OO0O0000OO0O0 [OO00O0OO0O0OO0000 ])+'\t'+str (O0O00000OO0O00OOO )+'\t'+O0OOO00000O0O000O +'\t'+OOO0OO0OOOO0O00OO [OO00O0OO0O0OO0000 ]+'\t'+O0000OOOO0OOO00OO +'\t'+O0OO00000O000000O +'\n'
            O0O00OO00OO0OO00O .write (OOOO0O0O0O0OOO000 )
    O0O00OO00OO0OO00O .close ()

if __name__ =='__main__':
    threshold =sys .argv [1 ]
    treeNode =sys .argv [2 ]
    KN ="ST"
    G0 =treeNode .split ("/,")[0 ]
    if (G0 =="TK")or (G0 .startswith ("Dual")and not G0 .startswith ("Dual/TK")):
        KN ="Y"
    upfile =sys .argv [3 ]
    outpath =sys .argv [4 ]
    outf =outpath 
    outpath =outpath .rsplit ('/',1 )[0 ]+'/'
    weights =np .load ('/data/www/gps6/webcomp/models/pref/stpwd_weight_norm.npy')
    model_path ="/data/www/gps6/webcomp/models/ALL/ST/"
    if KN =="Y":
        weights =np .load ('/data/www/gps6/webcomp/models/pref/ypwd_weight_norm.npy')
        model_path ="/data/www/gps6/webcomp/models/ALL/Y/"
    id_seq ,df =fasta2seq (upfile ,outpath ,KN )
    seq =df ['PSP'].tolist ()
    ids =df ['ID'].tolist ()
    locs =df ['loc'].tolist ()
    sitedic ={}
    epsd =pd .read_csv ("/data/www/gps6/epsd",header =0 )
    for k ,v in id_seq .items ():
        if k in sitedic .keys ():
            break 
        epsd_seqs =epsd ["seq"].tolist ()
        if v in epsd_seqs :
            ep_index =epsd_seqs .index (v )
            sitedic [k ]=epsd .loc [ep_index ,'id']
        else :
            sitedic [k ]=''
    seq2fts (seq ,weights ,outpath ,KN )
    treeNodes =treeNode .split (",")
    for k in treeNodes :
        if k =="Dual/"or k =="Atypical/"or k =="Other/"or k =="Dual/Atypical/"or k =="Dual/Other/":
            pass 
        else :
            treeN =k .rsplit ("/",1 )[0 ]
            knpath =model_path +k 
            pred_comb =test_predict (outpath ,knpath )
            if threshold =="a":
                thd ="Null"
                pred_type =[1 ]*len (pred_comb )
                out_format (pred_comb ,pred_type ,thd ,seq ,ids ,treeN ,sitedic ,locs ,outf )
            else :
                zhibiao =pd .read_csv (knpath +"zhibiao.txt",sep ="\t",header =None )
                if threshold =="a":
                    thd ="Null"
                    pred_type =[1 ]*len (pred_comb )
                    out_format (pred_comb ,pred_type ,thd ,seq ,ids ,treeN ,sitedic ,locs ,outf )
                else :
                    if threshold =="h":
                        thd =round (float (zhibiao .iloc [0 ,1 ]),4 )
                    elif threshold =="m":
                        thd =round (float (zhibiao .iloc [1 ,1 ]),4 )
                    elif threshold =="l":
                        thd =round (float (zhibiao .iloc [2 ,1 ]),4 )
                pred_type =(pred_comb >=thd ).astype (bool )
                out_format (pred_comb ,pred_type ,thd ,seq ,ids ,treeN ,sitedic ,locs ,outf )