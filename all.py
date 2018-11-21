#! /usr/bin/env python

import os
import sys
import re
import draw_venn
from matplotlib_venn import venn2
from matplotlib import pyplot as plt


result_file = open("./venn_result/result.tsv", "w")
summary_file = open("./venn_result/gene_summary.tsv", "w")

result_file.write("id\tyokomon curation\tmatch\twatson\n")
summary_file.write("gene\tyokomon curation\tmatch\twatson\n")

y_all = 0
w_all = 0
match_all = 0

y_hash = {}
w_hash = {}
yw_hash = {}

for file in os.listdir("./manual/"):

    print file
    
    #r = re.compile('F-(.+)\.genomon_mutation\.result\.filt\.all\.combined_([0-9]+)_anno\.xlsx')
    #r = re.compile('(.+)\.genomon_mutation\.result\.filt\.all\.combined_([0-9]+)\.tsv')
    #m = r.search(file)
    #rimsid = m.group(1)
    #filepath = m.group(0)

    type = ""
    buf = file

    if buf.find(".genomon_mutation.result.filt.all.combined_20180711_anno.xlsx") != -1:
        buf = buf.replace(".genomon_mutation.result.filt.all.combined_20180711_anno.xlsx","")
        type = "0711"
    if buf.find(".genomon_mutation.result.filt.all.combined_20180720_anno.xlsx") != -1:
        buf = buf.replace(".genomon_mutation.result.filt.all.combined_20180720_anno.xlsx","")
        type = "0720"
    if buf.find(".genomon_mutation.result.filt.all.combined_20181105.xlsx") != -1:
        buf = buf.replace(".genomon_mutation.result.filt.all.combined_20181105.xlsx","")
        type = "1105"
    if buf.find(".genomon_mutation.result.filt.all.combined_20180711") != -1:
        buf = buf.replace(".genomon_mutation.result.filt.all.combined_20180711.xlsx","")
        type = "0711"

    #file = file.replace("./manual/","")
    rimsid = re.sub(r'^D-',"",buf)
    print rimsid
    venn = draw_venn.func(rimsid, file, type)


    #venn = draw_venn.func(rimsid, filepath)
    y_list = venn[0]
    yw_list = venn[1]
    w_list = venn[2]
    w_gene_list = venn[3]

    y = len(y_list)
    yw = len(yw_list)
    w = len(w_list)

    result_file.write(rimsid+"\t"+str(y)+"\t"+str(yw)+"\t"+str(w)+"\n")

    y_all += y
    w_all += w
    match_all += yw

    for gene in y_list:
        if not y_hash.has_key(gene):
            y_hash[gene] = 1
        else:
            y_hash[gene] += 1

    for gene in w_gene_list:
        if not w_hash.has_key(gene):
            w_hash[gene] = 1
        else:
            w_hash[gene] += 1

    for gene in yw_list:
        if not yw_hash.has_key(gene):
            yw_hash[gene] = 1
        else:
            yw_hash[gene] += 1


#print y_hash
#print w_hash
#print yw_hash

y_all = y_all - match_all
w_all = w_all - match_all



v = venn2(subsets=(y_all, w_all, match_all), set_labels = ('Human Curation', 'Watson Call'))
v.get_patch_by_id('10').set_color("#819FF7")
v.get_patch_by_id('01').set_color("#ffb6c1")
v.get_patch_by_id('11').set_color("#0000FF")

v.get_label_by_id('10').set_y('0.3')
v.get_label_by_id('10').set_x('-0.45')
v.get_label_by_id('11').set_y('0.3')
v.get_label_by_id('11').set_x('0')
v.get_label_by_id('01').set_y('0.3')
v.get_label_by_id('01').set_x('0.45')


plt.title("ALL")
plt.savefig("./venn_result/all.png")
plt.close()


gene_list = []
for gene in y_hash:
    if not gene in gene_list:
        gene_list.append(gene)

for gene in w_hash:
    if not gene in gene_list:
        gene_list.append(gene)

for gene in yw_hash:
    if not gene in gene_list:
        gene_list.append(gene)

print y_hash
print yw_hash
print w_hash


summary_str = ""
for gene in gene_list:
    y_num = ""
    yw_num = ""
    w_num = ""
    if not y_hash.has_key(gene):
        y_num = 0
    else:
        y_num = y_hash[gene]
    if not yw_hash.has_key(gene):
        yw_num = 0
    else:
        yw_num = yw_hash[gene]
    if not w_hash.has_key(gene):
        w_num = 0
    else:
        w_num = w_hash[gene]

    summary_str += gene+"\t"+str(y_num)+"\t"+str(yw_num)+"\t"+str(w_num)+"\n"


summary_file.write(summary_str)

