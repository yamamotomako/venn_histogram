#! /usr/bin/env python

import os,sys

result_file = open("./human_vs_watson_drug_count.csv", "w")

manual_gene = {}
watson_gene = {}

with open("./human_drug_count.csv", "r") as f:
    lines = f.read().strip().split("\n")
    for line in lines:
        data = line.split(",")
        if data[0] == "LIMSID":
            continue

        gene = data[1]
        count = data[2]
        
        if gene not in manual_gene:
            manual_gene[gene] = 0

        print count
        manual_gene[gene] += int(count)

print manual_gene

with open("./watson_drug_count.csv", "r") as f:
    lines = f.read().strip().split("\n")
    for line in lines:
        data = line.split(",")

        if data[0] == "LIMSID":
            continue

        print data
        gene = data[1]
        count_a = data[2]
        count_i = data[3]
        count_o = data[4]

        count = int(count_a)+int(count_i)+int(count_o)

        if gene not in watson_gene:
            watson_gene[gene] = 0

        watson_gene[gene] += int(count)

print watson_gene



result_file.write("Gene,Human_drug,Watson_drug\n")

result_str = ""
flag = []
for gene in manual_gene:
    if gene in watson_gene:
        result_str += gene+","+str(manual_gene[gene])+","+str(watson_gene[gene])+"\n"
    else:
        result_str += gene+","+str(manual_gene[gene])+","+"0"+"\n"
    flag.append(gene)

for gene in watson_gene:
    if gene not in manual_gene:
        result_str += gene+","+"0,"+str(watson_gene[gene])+"\n"

result_file.write(result_str)


result_file.close()
