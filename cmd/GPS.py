""#line:6
import time #line:7
start_time =time .time ()#line:8
import sys ,os ,re #line:9
import pandas as pd #line:11
import numpy as np #line:12
import collections #line:13
from collections import Counter #line:14
import lightgbm as lgb #line:15
def getblosum62 ():#line:17
    O000OO0OOO0OO000O =open ('/home/biocucko/public_html/gps6/webcomp/models/pref/BLOSUM62','r')#line:18
    OOOOOO00O000O0O00 =[]#line:19
    OO0O0O00O0O0O00OO =[]#line:20
    OO0OO0000000O00O0 ={}#line:21
    for O0O00000O0O000O0O in O000OO0OOO0OO000O .readlines ():#line:22
        O000OO0OO00O0O00O =O0O00000O0O000O0O .split ()#line:23
        O00OOOO000OOO0OOO =O000OO0OO00O0O00O [0 ]#line:24
        OO0O0O00O0O0O00OO .append (O00OOOO000OOO0OOO )#line:25
    O000OO0OOO0OO000O .close ()#line:26
    O0OOOO0OOO00OO0OO =open ('/home/biocucko/public_html/gps6/webcomp/models/pref/BLOSUM62','r')#line:27
    O00O00OOOO0000O00 =0 #line:28
    for O0O00000O0O000O0O in O0OOOO0OOO00OO0OO .readlines ():#line:29
        O000OO0OO00O0O00O =O0O00000O0O000O0O .strip ()#line:30
        O000OO0OO00O0O00O =O0O00000O0O000O0O .split ()#line:31
        for OOO0O00O0O0000000 in range (len (O000OO0OO00O0O00O )):#line:32
            if OOO0O00O0O0000000 ==0 :#line:33
                continue #line:34
            else :#line:35
                OO00O0O00O000O0OO =float (O000OO0OO00O0O00O [OOO0O00O0O0000000 ])#line:36
                O000O0OO00O00OOOO =OO0O0O00O0O0O00OO [O00O00OOOO0000O00 ]+"_"+OO0O0O00O0O0O00OO [OOO0O00O0O0000000 -1 ]#line:37
                O000000O00O00OO00 =OO0O0O00O0O0O00OO [OOO0O00O0O0000000 -1 ]+"_"+OO0O0O00O0O0O00OO [O00O00OOOO0000O00 ]#line:38
                if O000O0OO00O00OOOO not in OOOOOO00O000O0O00 and O000000O00O00OO00 not in OOOOOO00O000O0O00 :#line:39
                    OOOOOO00O000O0O00 .append (O000O0OO00O00OOOO )#line:40
                    OO0OO0000000O00O0 [O000O0OO00O00OOOO ]=OO00O0O00O000O0OO #line:41
        O00O00OOOO0000O00 +=1 #line:42
    O0OOOO0OOO00OO0OO .close ()#line:43
    return OO0OO0000000O00O0 ,OOOOOO00O000O0O00 ,OO0O0O00O0O0O00OO #line:44
def getArray (O0000O0OO0O0O00O0 ):#line:46
    O0OO0O0O0OO0000OO =[]#line:47
    for O0O0O000O00OOOOOO in range (len (O0000O0OO0O0O00O0 )):#line:48
        O0OO0O0O0OO0000OO .append (0.0 )#line:49
    OOOO0OOO000OOOO0O =np .array (O0OO0O0O0OO0000OO )#line:50
    return OOOO0OOO000OOOO0O #line:51
def getMMScoreTest000 (O00O0OO0OO000O00O ,OOO0O00O0O0OO00O0 ,OOO000OO00O000000 ,O0OO0OO0OOO00000O ="ST"):#line:53
    O0OO0OOO0OOO0OO00 ,OOO00O0OOOOO00O00 ,OOO00OO0O000O00OO =getblosum62 ()#line:56
    if O0OO0OO0OOO00000O =="ST":#line:57
        OOOO00000OO000O0O =np .load ("/home/biocucko/public_html/gps6/webcomp/models/pref/stpos_smoscores.npy",allow_pickle =True )#line:58
    else :#line:59
        OOOO00000OO000O0O =np .load ("/home/biocucko/public_html/gps6/webcomp/models/pref/ypos_smoscores.npy",allow_pickle =True )#line:60
    O0O0OO00OO0000O0O =[]#line:62
    for OOOO00OOO0O0OO0O0 in O00O0OO0OO000O00O :#line:64
        OO0O0OOOO0O000O00 =getArray (OOO00O0OOOOO00O00 )#line:65
        for O0OOOOO0O0O0OOOO0 in range (len (OOOO00OOO0O0OO0O0 )):#line:66
            O0O0OO0O0O0OOO0OO =OOOO00OOO0O0OO0O0 [O0OOOOO0O0O0OOOO0 ]#line:67
            if O0O0OO0O0O0OOO0OO not in OOO00OO0O000O00OO :#line:68
                O0O0OO0O0O0OOO0OO ='*'#line:69
            OO00O000OO0O0OO00 =OOO00OO0O000O00OO .index (O0O0OO0O0O0OOO0OO )#line:70
            O0O0000OO0OOOO0O0 =OOOO00000OO000O0O [O0OOOOO0O0O0OOOO0 ][OO00O000OO0O0OO00 ]#line:71
            OO0O0OOOO0O000O00 =OO0O0OOOO0O000O00 +O0O0000OO0OOOO0O0 #line:72
        OO0O0OOOO0O000O00 =(OO0O0OOOO0O000O00 /(len (OOOO00000OO000O0O ))).tolist ()#line:74
        O0O0OO00OO0000O0O .append (OO0O0OOOO0O000O00 )#line:75
    O0O0OO00OO0000O0O =np .float16 (O0O0OO00OO0000O0O )#line:77
    return O0O0OO00OO0000O0O #line:79
def getMMScoreTest (O000OOOOO00OOO00O ,OOOO00O00O000O0O0 ="ST"):#line:81
    O00000O00O0O00000 ,OOO00O0OOOO00OOO0 ,O0OO0O0OO00O00OOO =getblosum62 ()#line:84
    OOO0O00OO0OOO00O0 =getArray (OOO00O0OOOO00OOO0 )#line:85
    O00O0OO0OOOO00OOO =[]#line:87
    if OOOO00O00O000O0O0 =="ST":#line:88
        O0OO00OO0OOOO0O00 =np .load ("/home/biocucko/public_html/gps6/webcomp/models/pref/stpos_smoscores.npy",allow_pickle =True )#line:89
        for O0OO0000O0O0O00OO in O000OOOOO00OOO00O :#line:93
            OOOO0000OO00O0O0O =OOO0O00OO0OOO00O0 #line:94
            for OOO00O00O00O0OO0O in range (61 ):#line:95
                O00000O0OO0OO00OO =O0OO0000O0O0O00OO [OOO00O00O00O0OO0O ]#line:96
                if O00000O0OO0OO00OO not in O0OO0O0OO00O00OOO :#line:97
                    O00000O0OO0OO00OO ='*'#line:98
                OOOO0OOO0O0OOOOO0 =O0OO0O0OO00O00OOO .index (O00000O0OO0OO00OO )#line:99
                OO0O0000OO00OO0O0 =O0OO00OO0OOOO0O00 [OOO00O00O00O0OO0O ][OOOO0OOO0O0OOOOO0 ]#line:100
                OOOO0000OO00O0O0O =OOOO0000OO00O0O0O +OO0O0000OO00OO0O0 #line:101
            OOOO0000OO00O0O0O =(OOOO0000OO00O0O0O /(len (O0OO00OO0OOOO0O00 ))).tolist ()#line:103
            O00O0OO0OOOO00OOO .append (OOOO0000OO00O0O0O )#line:104
        O00O0OO0OOOO00OOO =np .float16 (O00O0OO0OOOO00OOO )#line:106
    elif OOOO00O00O000O0O0 =="Y":#line:107
        O0OO00OO0OOOO0O00 =np .load ("/home/biocucko/public_html/gps6/webcomp/models/pref/ypos_smoscores.npy",allow_pickle =True )#line:108
        for O0OO0000O0O0O00OO in O000OOOOO00OOO00O :#line:112
            OOOO0000OO00O0O0O =OOO0O00OO0OOO00O0 #line:113
            for OOO00O00O00O0OO0O in range (61 ):#line:114
                O00000O0OO0OO00OO =O0OO0000O0O0O00OO [OOO00O00O00O0OO0O ]#line:115
                if O00000O0OO0OO00OO not in O0OO0O0OO00O00OOO :#line:116
                    O00000O0OO0OO00OO ='*'#line:117
                OOOO0OOO0O0OOOOO0 =O0OO0O0OO00O00OOO .index (O00000O0OO0OO00OO )#line:118
                OO0O0000OO00OO0O0 =O0OO00OO0OOOO0O00 [OOO00O00O00O0OO0O ][OOOO0OOO0O0OOOOO0 ]#line:119
                OOOO0000OO00O0O0O =OOOO0000OO00O0O0O +OO0O0000OO00OO0O0 #line:120
            OOOO0000OO00O0O0O =(OOOO0000OO00O0O0O /(len (O0OO00OO0OOOO0O00 ))).tolist ()#line:122
            O00O0OO0OOOO00OOO .append (OOOO0000OO00O0O0O )#line:123
        O00O0OO0OOOO00OOO =np .float16 (O00O0OO0OOOO00OOO )#line:125
    return O00O0OO0OOOO00OOO #line:162
def getMMScoreTest_sty (OO0O00OO0000O00OO ,O0OOOO00O000000OO ,OOO00O00OO0O0OOO0 ="STY"):#line:164
    O0OO0OO0O00O0O0O0 ,OOO0O00O00OOOO000 ,O0OO0O00O000OOO00 =getblosum62 ()#line:167
    OOOO0000OO00000O0 =getArray (OOO0O00O00OOOO000 )#line:168
    OO000O00O00000OO0 =np .load ("/home/biocucko/public_html/gps6/webcomp/models/pref/stpos_smoscores.npy",allow_pickle =True )#line:170
    OO0OOO0O0O00O0OO0 =np .load ("/home/biocucko/public_html/gps6/webcomp/models/pref/ypos_smoscores.npy",allow_pickle =True )#line:171
    O00OO00O00OO0OOOO =[]#line:172
    OO0000000O000000O =[]#line:173
    O000OOOOO0O00O0O0 =[]#line:174
    OOOO00OOOO0OOO0O0 =[]#line:175
    O0O0O00O00OOO00O0 =[]#line:176
    O00O0OO0OOO0O0OO0 =[]#line:177
    for O0OO0O00000000O00 in range (len (OO0O00OO0000O00OO )):#line:179
        O00OOO00O0O00OO0O =OO0O00OO0000O00OO [O0OO0O00000000O00 ]#line:180
        if O00OOO00O0O00OO0O [30 ]=='Y':#line:181
            O00OO0000OO00OOOO =OOOO0000OO00000O0 #line:184
            for O0OOO000000O0OOO0 in range (61 ):#line:185
                OOO00O00O00O00O0O =O00OOO00O0O00OO0O [O0OOO000000O0OOO0 ]#line:186
                if OOO00O00O00O00O0O not in O0OO0O00O000OOO00 :#line:187
                    OOO00O00O00O00O0O ='*'#line:188
                OO00O0OO00OOOOO00 =O0OO0O00O000OOO00 .index (OOO00O00O00O00O0O )#line:189
                O000OOO00OO0O00O0 =OO0OOO0O0O00O0OO0 [O0OOO000000O0OOO0 ][OO00O0OO00OOOOO00 ]#line:190
                O00OO0000OO00OOOO =O00OO0000OO00OOOO +O000OOO00OO0O00O0 #line:191
            O00OO0000OO00OOOO =(O00OO0000OO00OOOO /(len (OO0OOO0O0O00O0OO0 ))).tolist ()#line:193
            O00OO00O00OO0OOOO .append (O00OO0000OO00OOOO )#line:194
            OOOO00OOOO0OOO0O0 .append (O0OOOO00O000000OO [O0OO0O00000000O00 ])#line:195
            O00O0OO0OOO0O0OO0 .append (O00OOO00O0O00OO0O )#line:196
        else :#line:197
            O00OO0000OO00OOOO =OOOO0000OO00000O0 #line:200
            for OO00O0OO0O0OOO0O0 in range (61 ):#line:201
                OOO00O00O00O00O0O =O00OOO00O0O00OO0O [OO00O0OO0O0OOO0O0 ]#line:202
                if OOO00O00O00O00O0O not in O0OO0O00O000OOO00 :#line:203
                    OOO00O00O00O00O0O ='*'#line:204
                OO00O0OO00OOOOO00 =O0OO0O00O000OOO00 .index (OOO00O00O00O00O0O )#line:205
                O000OOO00OO0O00O0 =OO000O00O00000OO0 [OO00O0OO0O0OOO0O0 ][OO00O0OO00OOOOO00 ]#line:206
                O00OO0000OO00OOOO =O00OO0000OO00OOOO +O000OOO00OO0O00O0 #line:207
            O00OO0000OO00OOOO =(O00OO0000OO00OOOO /(len (OO000O00O00000OO0 ))).tolist ()#line:209
            OO0000000O000000O .append (O00OO0000OO00OOOO )#line:210
            O000OOOOO0O00O0O0 .append (O0OOOO00O000000OO [O0OO0O00000000O00 ])#line:211
            O0O0O00O00OOO00O0 .append (O00OOO00O0O00OO0O )#line:212
    OO0000000O000000O =np .float16 (OO0000000O000000O )#line:215
    O00OO00O00OO0OOOO =np .float16 (O00OO00O00OO0OOOO )#line:217
    return OO0000000O000000O ,O00OO00O00OO0OOOO ,O000OOOOO0O00O0O0 ,OOOO00OOOO0OOO0O0 ,O0O0O00O00OOO00O0 ,O00O0OO0OOO0O0OO0 #line:218
def fasta2seq (OOO000OOOO000O00O ,O00OO0OO0OO0O00O0 ):#line:220
    O0O0OO0000OOOOOO0 =open (OOO000OOOO000O00O ,'r')#line:222
    OO0OOO0OO0OOOOOOO ={}#line:223
    global linename #line:224
    for OO0OOOO0OO00OOO00 in O0O0OO0000OOOOOO0 :#line:225
        if OO0OOOO0OO00OOO00 .startswith ('>'):#line:226
           linename =OO0OOOO0OO00OOO00 .replace ('>','').strip ()#line:227
           OO0OOO0OO0OOOOOOO [linename ]=''#line:228
        else :#line:229
           OO0OOO0OO0OOOOOOO [linename ]+=OO0OOOO0OO00OOO00 .strip ()#line:230
    O0OOOO000OO00O00O =[]#line:231
    O0OO00OO00O0O000O =[]#line:232
    OOO0O0000OO00O000 =[]#line:233
    for O0OO00OOO0O0O0O0O ,OOOOO0OO0O0O0O0O0 in OO0OOO0OO0OOOOOOO .items ():#line:234
        O0000000OO00OOOOO =[]#line:236
        OO0O0000OOOO0OOO0 ='******************************'#line:238
        for O0OO0000OO0O0O000 in range (len (OOOOO0OO0O0O0O0O0 )):#line:239
            if O00OO0OO0OO0O00O0 =="ST"and OOOOO0OO0O0O0O0O0 [O0OO0000OO0O0O000 ]!="S"and OOOOO0OO0O0O0O0O0 [O0OO0000OO0O0O000 ]!="T":#line:240
                continue #line:242
            elif O00OO0OO0OO0O00O0 =="Y"and OOOOO0OO0O0O0O0O0 [O0OO0000OO0O0O000 ]!="Y":#line:243
                continue #line:244
            elif O00OO0OO0OO0O00O0 =="STY"and OOOOO0OO0O0O0O0O0 [O0OO0000OO0O0O000 ]!="S"and OOOOO0OO0O0O0O0O0 [O0OO0000OO0O0O000 ]!="T"and OOOOO0OO0O0O0O0O0 [O0OO0000OO0O0O000 ]!="Y":#line:245
                continue #line:246
            else :#line:249
                if O0OO0000OO0O0O000 <30 :#line:250
                    O0O0O000OO00OOOO0 =OO0O0000OOOO0OOO0 [:(30 -O0OO0000OO0O0O000 )]#line:252
                    O0O000OO000O0OOO0 =OOOOO0OO0O0O0O0O0 [:O0OO0000OO0O0O000 +31 ]#line:253
                    O0O0O000OO00OOOO0 =O0O0O000OO00OOOO0 +O0O000OO000O0OOO0 #line:254
                    if len (O0O0O000OO00OOOO0 )<61 :#line:255
                        OO00000O000OO0O0O =OO0O0000OOOO0OOO0 [:(61 -len (O0O0O000OO00OOOO0 ))]#line:256
                        O0O0O000OO00OOOO0 =O0O0O000OO00OOOO0 +OO00000O000OO0O0O #line:257
                elif O0OO0000OO0O0O000 >=(len (OOOOO0OO0O0O0O0O0 )-30 ):#line:259
                    O0O0O000OO00OOOO0 =OOOOO0OO0O0O0O0O0 [(O0OO0000OO0O0O000 -30 ):(len (OOOOO0OO0O0O0O0O0 ))]#line:260
                    O0O000OO000O0OOO0 =OO0O0000OOOO0OOO0 [:(30 -(len (OOOOO0OO0O0O0O0O0 )-O0OO0000OO0O0O000 -1 ))]#line:261
                    O0O0O000OO00OOOO0 =O0O0O000OO00OOOO0 +O0O000OO000O0OOO0 #line:262
                else :#line:263
                    O0O0O000OO00OOOO0 =OOOOO0OO0O0O0O0O0 [O0OO0000OO0O0O000 -30 :O0OO0000OO0O0O000 +31 ]#line:264
                O0000000OO00OOOOO .append (O0O0O000OO00OOOO0 )#line:265
                OOO0O0000OO00O000 .append (O0OO0000OO0O0O000 )#line:266
        O0OOOO000OO00O00O .extend ([O0OO00OOO0O0O0O0O ]*len (O0000000OO00OOOOO ))#line:267
        O0OO00OO00O0O000O .extend (O0000000OO00OOOOO )#line:268
    return OO0OOO0OO0OOOOOOO ,O0OOOO000OO00O00O ,O0OO00OO00O0O000O ,OOO0O0000OO00O000 #line:274
def test_predict (OOO0O000OOOOO0OO0 ,OOO00OO00O0O0OO00 ):#line:276
    O00O00O0OOOO0O0O0 =OOO00OO00O0O0OO00 +'SMO.txt'#line:280
    O0OO000OO0OO0OOOO =lgb .Booster (model_file =O00O00O0OOOO0O0O0 )#line:281
    O00O000OO00OOO00O =O0OO000OO0OO0OOOO .predict (OOO0O000OOOOO0OO0 )#line:282
    return O00O000OO00OOO00O #line:284
def out_format (OOOO0O00O0OO0O0O0 ,O000O00OO0OOO000O ,O00O0O000O00OOO0O ,OO0O00O0O0O00O0O0 ,OO000OOOO0OOOO00O ,O00O000OOOO0OOOOO ,O00O0O0O00OO0O000 ,O0O0OOO0OO00O00OO ,OO0O000O0OOO0OO0O ):#line:286
    ""#line:307
    O0OO000OO0O000O00 =open (OO0O000O0OOO0OO0O ,'a+')#line:308
    O000O00O0O00OOOO0 =os .path .getsize (OO0O000O0OOO0OO0O )#line:309
    if O000O00O0O00OOOO0 ==0 :#line:310
        O0OO000OO0O000O00 .write ("ID\tPosition\tCode\tKinase\tPeptide\tScore\tCutoff\n")#line:311
    OOO00O0O0000OOO0O =OO000OOOO0OOOO00O [0 ].strip ()#line:314
    O0O00O0OOOOO0O0OO =ids2ppi (O00O000OOOO0OOOOO ,OOO00O0O0000OOO0O )#line:315
    OOO0O0OOOO0OO0000 =O00O0O0O00OO0O000 [OOO00O0O0000OOO0O ]#line:317
    for O0OO000O00OO0OOO0 in range (len (O000O00OO0OOO000O )):#line:318
        if O000O00OO0OOO000O [O0OO000O00OO0OOO0 ]:#line:319
            O0O0000O0OOOOOO00 =psp2source (OO0O00O0O0O00O0O0 [O0OO000O00OO0OOO0 ],O00O000OOOO0OOOOO ,OOO00O0O0000OOO0O )#line:320
            O0O0OO0OO0000O0OO =OOO00O0O0000OOO0O +'\t'+str (O0O0OOO0OO00O00OO [O0OO000O00OO0OOO0 ]+1 )+'\t'+OO0O00O0O0O00O0O0 [O0OO000O00OO0OOO0 ][30 ]+'\t'+O00O000OOOO0OOOOO +'\t'+OO0O00O0O0O00O0O0 [O0OO000O00OO0OOO0 ][23 :38 ]+'\t'+'{:.4f}'.format (OOOO0O00O0OO0O0O0 [O0OO000O00OO0OOO0 ])+'\t'+str (O00O0O000O00OOO0O )+'\t'+OOO0O0OOOO0OO0000 +'\t'+OO0O00O0O0O00O0O0 [O0OO000O00OO0OOO0 ]+'\t'+O0O0000O0OOOOOO00 +'\t'+O0O00O0OOOOO0O0OO +'\n'#line:325
            O0OO000OO0O000O00 .write (O0O0OO0OO0000O0OO )#line:327
    O0OO000OO0O000O00 .close ()#line:328
def psp2source (O00OO00OOOOO00OOO ,O0OOO000O00O0O0O0 ,O0O0000O0O0O00O00 ):#line:330
    O0OOO000O00O0O0O0 =O0OOO000O00O0O0O0 .replace ("/","_")#line:331
    OO000000OOOO0O00O =pd .read_csv ("/home/biocucko/public_html/gps6/psp_source2.txt",header =None )#line:332
    OOOOO0O0O00O00OO0 =OO000000OOOO0O00O [0 ].tolist ()#line:333
    if O00OO00OOOOO00OOO not in set (OOOOO0O0O00O00OO0 ):#line:336
        return "Pred."#line:337
    else :#line:338
        OOO00OO00OOOO0O00 =OO000000OOOO0O00O .loc [OO000000OOOO0O00O [0 ]==O00OO00OOOOO00OOO ]#line:340
        OOO00OO00OOOO0O00 =OOO00OO00OOOO0O00 [OOO00OO00OOOO0O00 [1 ].str .contains (O0OOO000O00O0O0O0 )]#line:342
        O0000O0O0O00O00O0 =OOO00OO00OOOO0O00 [2 ].tolist ()#line:343
        if len (O0000O0O0O00O00O0 )==0 :#line:344
            return "Pred."#line:345
        else :#line:346
            O0000O0O0O00O00O0 =O0000O0O0O00O00O0 [0 ]#line:347
            if O0000O0O0O00O00O0 .isdigit ():#line:348
                return "<a href =https://pubmed.ncbi.nlm.nih.gov/%s/  target='_blank'>Exp.</ a></font></td>"%O0000O0O0O00O00O0 #line:350
            elif O0000O0O0O00O00O0 =="UniProt":#line:351
                return "<a href =https://www.uniprot.org/uniprotkb?query=%s target='_blank'>Exp.</ a></font></td>"%O0O0000O0O0O00O00 #line:353
            else :#line:354
                return "<a href =https://www.phosphosite.org/simpleSearchSubmitAction.action?searchStr=%s target='_blank'>Exp.</ a></font></td>"%O0O0000O0O0O00O00 #line:356
def ids2ppi (O0OOO0O00OOOO0O0O ,O0OOO0O0O0OO0000O ):#line:358
    if '/'in O0OOO0O00OOOO0O0O :#line:361
        O00OOOO0O0O0OO0OO =O0OOO0O00OOOO0O0O .rsplit ("/",1 )[1 ]#line:362
    else :#line:363
        O00OOOO0O0O0OO0OO =O0OOO0O00OOOO0O0O #line:364
    OOOO0O0OO0000OO0O =pd .read_csv ("/home/biocucko/public_html/gps6/webcomp/kn_b_vname2.txt",sep ='\t',header =0 )#line:365
    O0OOO0O0O0000O000 =OOOO0O0OO0000OO0O [(OOOO0O0OO0000OO0O ['KN']==O00OOOO0O0O0OO0OO )&(OOOO0O0OO0000OO0O ['B'].str .contains (O0OOO0O0O0OO0000O ))]#line:366
    if len (O0OOO0O0O0000O000 )>0 :#line:367
        return "<a href =https://pubmed.ncbi.nlm.nih.gov/%s/  target='_blank'>&radic;</ a></font></td>"%O0OOO0O0O0000O000 ['PMID'].tolist ()[0 ]#line:369
    else :#line:370
        return "<a href =https://thebiogrid.org/  target='_blank'>--</ a></font></td>"#line:371
if __name__ =='__main__':#line:374
    threshold =sys .argv [1 ]#line:376
    treeNode =sys .argv [2 ]#line:377
    GS =treeNode .split (",")#line:380
    GS =[OO0O0O0OO00000000 for OO0O0O0OO00000000 in GS if OO0O0O0OO00000000 !="Dual/"]#line:381
    G0 =GS [0 ]#line:382
    ydual =["Dual/AGC/","Dual/Atypical/","Dual/CAMK/","Dual/CK1/","Dual/CMGC/","Dual/STE/","Dual/TKL/","Dual/Other/"]#line:384
    KN ="ST"#line:385
    kst =[]#line:386
    ky =[]#line:387
    if (G0 =="TK/")or (G0 .startswith ("Dual/")and (G0 !="Dual/TK/")):#line:388
        KN ="Y"#line:389
    elif "TK/"in GS :#line:392
        KN ="STY"#line:394
        idx_spl =GS .index ("TK/")#line:395
        kst =GS [:idx_spl ]#line:396
        ky =GS [idx_spl :]#line:397
    elif len ([OO0O00OOOO000OO00 for OO0O00OOOO000OO00 in GS if OO0O00OOOO000OO00 in ydual ])>0 :#line:398
        KN ="STY"#line:400
        vv =[OO00OOO0O00OOO000 for OO00OOO0O00OOO000 in GS if OO00OOO0O00OOO000 in ydual ][0 ]#line:401
        idx_spl =GS .index (vv )#line:402
        kst =GS [:idx_spl ]#line:403
        ky =GS [idx_spl :]#line:404
    upfile =sys .argv [3 ]#line:410
    outpath =sys .argv [4 ]#line:411
    outf =outpath #line:412
    outpath =outpath .rsplit ('/',1 )[0 ]+'/'#line:413
    if KN =="ST"or KN =="Y":#line:415
        id_seq ,ids ,seq ,locs =fasta2seq (upfile ,KN )#line:418
        np_results =getMMScoreTest (seq ,KN )#line:419
        sitedic ={}#line:422
        epsd =pd .read_csv ("/home/biocucko/public_html/gps6/epsd",header =0 )#line:424
        for k ,v in id_seq .items ():#line:425
            if k in sitedic .keys ():#line:426
                break #line:427
            epsd_seqs =epsd ["seq"].tolist ()#line:428
            if v in epsd_seqs :#line:429
                ep_index =epsd_seqs .index (v )#line:430
                sitedic [k ]="<a href =http://epsd.biocuckoo.cn/View.php?id=%s target='_blank'>%s</ a></font></td>"%(epsd .loc [ep_index ,'id'],epsd .loc [ep_index ,'id'])#line:432
            else :#line:435
                sitedic [k ]='--'#line:436
        for k in GS :#line:439
            if k =="Dual/"or k =="Atypical/"or k =="Other/"or k =="Dual/Atypical/"or k =="Dual/Other/":#line:440
                continue #line:441
            else :#line:442
                treeN =k .rsplit ("/",1 )[0 ]#line:443
                knpath ="/home/biocucko/public_html/gps6/webcomp/models/ALL/"+KN +"/"+k #line:445
                zhibiao =pd .read_csv ("/home/biocucko/public_html/gps6/webcomp/models/GPS/"+KN +"/"+k +"zhibiao_smo.txt",sep ="\t",header =None )#line:448
                pred_comb =test_predict (np_results ,knpath )#line:449
                if threshold =="a":#line:451
                    thd ="Null"#line:452
                    pred_type =[1 ]*len (pred_comb )#line:453
                    out_format (pred_comb ,pred_type ,thd ,seq ,ids ,treeN ,sitedic ,locs ,outf )#line:454
                else :#line:455
                    thd =0 #line:456
                    if threshold =="h":#line:457
                        thd =round (float (zhibiao .iloc [0 ,1 ]),4 )#line:458
                    elif threshold =="m":#line:459
                        thd =round (float (zhibiao .iloc [1 ,1 ]),4 )#line:460
                    elif threshold =="l":#line:461
                        thd =round (float (zhibiao .iloc [2 ,1 ]),4 )#line:462
                    pred_type =(pred_comb >=thd ).astype (bool )#line:465
                    out_format (pred_comb ,pred_type ,thd ,seq ,ids ,treeN ,sitedic ,locs ,outf )#line:467
    else :#line:469
        id_seq ,ids ,seq ,locs =fasta2seq (upfile ,KN )#line:471
        np_results_st ,np_results_y ,locst ,locy ,seqst ,seqy =getMMScoreTest_sty (seq ,locs ,KN )#line:473
        sitedic ={}#line:476
        epsd =pd .read_csv ("/home/biocucko/public_html/gps6/epsd",header =0 )#line:478
        for k ,v in id_seq .items ():#line:479
            if k in sitedic .keys ():#line:480
                break #line:481
            epsd_seqs =epsd ["seq"].tolist ()#line:482
            if v in epsd_seqs :#line:483
                ep_index =epsd_seqs .index (v )#line:484
                sitedic [k ]="<a href =http://epsd.biocuckoo.cn/View.php?id=%s target='_blank'>%s</ a></font></td>"%(epsd .loc [ep_index ,'id'],epsd .loc [ep_index ,'id'])#line:486
            else :#line:489
                sitedic [k ]='--'#line:490
        for k in kst :#line:492
            KN ='ST'#line:493
            if k =="Dual/"or k =="Atypical/"or k =="Other/"or k =="Dual/Atypical/"or k =="Dual/Other/":#line:494
                continue #line:495
            else :#line:496
                treeN =k .rsplit ("/",1 )[0 ]#line:497
                knpath ="/home/biocucko/public_html/gps6/webcomp/models/ALL/"+KN +"/"+k #line:499
                zhibiao =pd .read_csv ("/home/biocucko/public_html/gps6/webcomp/models/GPS/"+KN +"/"+k +"zhibiao_smo.txt",sep ="\t",header =None )#line:502
                pred_comb =test_predict (np_results_st ,knpath )#line:503
                if threshold =="a":#line:505
                    thd ="Null"#line:506
                    pred_type =[1 ]*len (pred_comb )#line:507
                    out_format (pred_comb ,pred_type ,thd ,seqst ,ids ,treeN ,sitedic ,locst ,outf )#line:508
                else :#line:509
                    thd =0 #line:510
                    if threshold =="h":#line:511
                        thd =round (float (zhibiao .iloc [0 ,1 ]),4 )#line:512
                    elif threshold =="m":#line:513
                        thd =round (float (zhibiao .iloc [1 ,1 ]),4 )#line:514
                    elif threshold =="l":#line:515
                        thd =round (float (zhibiao .iloc [2 ,1 ]),4 )#line:516
                    pred_type =(pred_comb >=thd ).astype (bool )#line:519
                    out_format (pred_comb ,pred_type ,thd ,seqst ,ids ,treeN ,sitedic ,locst ,outf )#line:521
        for k in ky :#line:523
            KN ='Y'#line:524
            if k =="Dual/Atypical/"or k =="Dual/Other/":#line:525
                continue #line:526
            else :#line:527
                treeN =k .rsplit ("/",1 )[0 ]#line:528
                knpath ="/home/biocucko/public_html/gps6/webcomp/models/ALL/"+KN +"/"+k #line:530
                zhibiao =pd .read_csv ("/home/biocucko/public_html/gps6/webcomp/models/GPS/"+KN +"/"+k +"zhibiao_smo.txt",sep ="\t",header =None )#line:533
                pred_comb =test_predict (np_results_y ,knpath )#line:534
                if threshold =="a":#line:536
                    thd ="Null"#line:537
                    pred_type =[1 ]*len (pred_comb )#line:538
                    out_format (pred_comb ,pred_type ,thd ,seqy ,ids ,treeN ,sitedic ,locy ,outf )#line:539
                else :#line:540
                    thd =0 #line:541
                    if threshold =="h":#line:542
                        thd =round (float (zhibiao .iloc [0 ,1 ]),4 )#line:543
                    elif threshold =="m":#line:544
                        thd =round (float (zhibiao .iloc [1 ,1 ]),4 )#line:545
                    elif threshold =="l":#line:546
                        thd =round (float (zhibiao .iloc [2 ,1 ]),4 )#line:547
                    pred_type =(pred_comb >=thd ).astype (bool )#line:550
                    out_format (pred_comb ,pred_type ,thd ,seqy ,ids ,treeN ,sitedic ,locy ,outf )#line:552
