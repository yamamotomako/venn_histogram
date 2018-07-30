#! /usr/bin/env python

import os
import sys
import re
import pandas


def func(rimsid, filepath):
    y_path = "./final/"+filepath
    #y_path = "./final/F-"+rimsid+".genomon_mutation.result.filt.all.combined_20180720.xlsx"
    df = pandas.read_excel(y_path,
        usecols=[0,14,15,16,20,23,199,200],
        sheet_name=0
    )

    LOG = open("./log.txt", "a")

    df = df.fillna(0)

    y_result = {}
    #y_remove = {}
    for index, row in df.iterrows():
        #r_flag = False
        
        final = int(row[0])
        LOG.write(rimsid+","+str(final)+"\n")
        if final != 1 and final != 2:
            continue

        chr = row[1]
        c_start = row[2]
        c_end = row[3]
        gene = row[4].encode("utf-8")
        amino = row[5]
        data_format = row[6]
        
        data = row[7].split(":")

        DP = data[2]
        VF = data[4]

        if gene == "U2AF1;U2AF1L5":
            gene = "U2AF1"

        #remove criteria
        #if final == 0:
        #    r_flag = True

        arr = [final,chr,c_start,c_end,gene,amino,DP,VF]
        #if r_flag:
        #    y_remove[gene+"_"+DP] = arr
        #else:
        y_result[gene+"_"+DP] = arr



    w_result = {}
    #w_remove = {}
    with open("./watson_call/"+rimsid+".tsv", "r") as g:
        lines = g.read().rstrip("\n").split("\n")

        for line in lines:
            d = line.split("\t")

            if d[0] == "sample":
                continue

            #r_flag = False
            chr = d[1]
            pos = d[2]
            gene = d[3]
            variantId = d[4]
            r = re.compile('.+\.(.+)')
            m = r.search(variantId)
            amino = m.group(1)
            vus = d[5]
            AF = d[8].replace("AF=","")
            DP = d[9].replace("DP=","")

            #remove criteria
            if "loss" in amino:
                continue

            if vus == "vus":
                continue
                #r_flag = True

            if AF == "" or DP == "":
                continue
                #r_flag = True

            arr = [chr,pos,gene,amino,vus,DP,AF]
            #if r_flag:
            #    w_remove[gene+"_"+DP] = arr
            #else:
            w_result[gene+"_"+DP] = arr



    KAKNIN = open("./kaknin.txt", "a")
    w_path = "./w_final/W-"+rimsid+".xlsx"
    kaknin_result = {}

    if os.path.exists(w_path):
        df = pandas.read_excel(w_path,
            sheet_name=0,
            header=None
        )

        df = df.fillna(0)

        for index, row in df.iterrows():
            flag = int(row[0])
            chr = row[2]
            pos = row[3]
            gene = row[4]
            variantId = row[5]
            vus = row[6]

            if vus == "vus":
                continue

            if row[9] == 0:
                continue

            AF = row[9].replace("AF=","")
            DP = row[10].replace("DP=","")

            kaknin_result[gene+"_"+DP] = flag
            print gene+"_"+DP

    else:
        KAKNIN.write(rimsid+" no file\n")

    #kakunin
    for key,value in kaknin_result.items():
        if value == 0:
            if w_result.has_key(key):
                if y_result.has_key(key):
                    KAKNIN.write(rimsid+":"+key+":"+str(value)+":"+"0 but w_result has.\n")

        else:
            if not w_result.has_key(key):
                if y_result.has_key(key):
                    KAKNIN.write(rimsid+":"+key+":"+str(value)+":"+"1 but w_result doesnt have.\n")

    KAKNIN.close()


    y_venn = []
    w_venn = []
    w_venn_gene = []
    yw_match = []
    for gene_dp in y_result:
        y_venn.append(y_result[gene_dp][4])

        if gene_dp in w_result:
            yw_match.append(y_result[gene_dp][4])

    for gene_dp in w_result:
        gene = w_result[gene_dp][2]
        w_venn_gene.append(w_result[gene_dp][2])

        if gene_dp in w_venn:
            index = w_venn.index(gene)
            gene = gene+"."+w_result[gene_dp][3]
            w_venn[index] = gene
        
        w_venn.append(gene)




    from matplotlib import pyplot as plt
    import numpy as np
    from matplotlib_venn import venn3, venn3_circles
    from matplotlib_venn import venn2


    A = set(y_venn)
    B = set(w_venn)

    v = venn2([A,B], ("Manual Curation","Watson Call"))

    if not v.get_label_by_id('11') == None:
        v.get_label_by_id('11').set_text('\n'.join(A&B))
        v.get_patch_by_id('11').set_color("#0000FF")
        #v.get_label_by_id('11').set_fontsize(8)

    v.get_label_by_id('10').set_text('\n'.join(A-B))
    v.get_label_by_id('01').set_text('\n'.join(B-A))

    #v.get_label_by_id('10').set_fontsize(8)
    #v.get_label_by_id('01').set_fontsize(8)

    v.get_patch_by_id('10').set_color("#819FF7")
    v.get_patch_by_id('01').set_color("#F3F781")


    #plt.show()
    plt.title(rimsid)
    plt.savefig("./venn_result/"+rimsid+".png")
    plt.close()

    print "yokomon",y_venn
    print "watson",w_venn
    print "match",yw_match

    return [y_venn, yw_match, w_venn, w_venn_gene]



#input_sheet_name = input_book.sheet_names
#num_sheet = len(input_sheet_name)

#input_sheet_df = input_book.parse(input_sheet_name[0],parse_cols = "A:X,GR:GS")

#with open("./F-3_S3.genomon_mutation.result.filt.all.combined_20180720.tsv", "r") as f:
#    lines = f.read().rstrip("\n").split("\n")
#    for line in lines:
#        d = line.split("\t")
#
#        final = d[0]
#        MYC = d[1]
#        chr = d[14]
#        c_start = d[15]
#        c_end = d[16]
#        gene = d[20]
#        amino = d[22]
#        data_format = d[199].split(":")
#        data = d[200].split(":")
#
#        DP = data[2]
#        VF = data[4]
#
#        y_result[gene+"_"+DP] = [final,MYC,chr,c_start,c_end,gene,amino,DP,VF]
#


#func("B001-08-2014-CML-BM1")
