#! /usr/bin/env python

import os
import sys
import re
import pandas


result_file = open("./human_drug_count.csv", "w")
result_file.write("LIMSID,gene,count\n")

drug_dict = {}
with open("./human_drug_dict.txt", "r") as f:
    lines = f.read().strip().split("\n")
    for line in lines:
        data = line.split(",")
        drug_dict[data[0]] = data[1]



def func(rimsid, filepath, type):
    y_path = filepath

    col_arr = []
    if type == "0711":
        col_arr = [0,1,15,16,17,23,26,203,204]
    if type == "0720":
        col_arr = [0,1,15,16,17,23,26,203,204]
        #col_arr = [0,1,14,15,16,20,23,199,200]
    if type == "1105":
        col_arr = [0,1,12,13,14,20,23,156,157]

    #y_path = "./final/F-"+rimsid+".genomon_mutation.result.filt.all.combined_20180720.xlsx"
    df = pandas.read_excel(y_path,
        usecols=col_arr,
        #usecols=[0,14,15,16,20,23,199,200],
        sheet_name=0
    )

    LOG = open("./log.txt", "a")

    df = df.fillna(0)

    y_result = {}
    #y_remove = {}


    print "------------------------------"
    for index, row in df.iterrows():
        drug = int(row[0])
        final = int(row[1])
        gene = row[5]

        if gene == "U2AF1;U2AF1L5":
            gene = "U2AF1"

        if final != 1:
            continue


        drug_count = 0
        if gene in drug_dict:
            drug_count = drug_dict[gene]

        print drug, gene, drug_count
        #LOG.write(rimsid+","+str(final)+"\n")
        result_file.write(rimsid+","+gene+","+str(drug_count)+"\n")



import glob

files = glob.glob("./manual/*")

for buf in files:
    file = buf
    type = ""
    print buf

    if file.find(".genomon_mutation.result.filt.all.combined_20180711_anno.xlsx") != -1:
        file = file.replace(".genomon_mutation.result.filt.all.combined_20180711_anno.xlsx","")
        type = "0711"
    if file.find(".genomon_mutation.result.filt.all.combined_20180720_anno.xlsx") != -1:
        file = file.replace(".genomon_mutation.result.filt.all.combined_20180720_anno.xlsx","")
        type = "0720"
    if file.find(".genomon_mutation.result.filt.all.combined_20181105.xlsx") != -1:
        file = file.replace(".genomon_mutation.result.filt.all.combined_20181105.xlsx","")
        type = "1105"
    if file.find(".genomon_mutation.result.filt.all.combined_20180711") != -1:
        file = file.replace(".genomon_mutation.result.filt.all.combined_20180711.xlsx","")
        type = "0711"

    file = file.replace("./manual/","")
    rimsid = re.sub(r'^D-',"",file)
    print rimsid
    func(rimsid, buf, type)

# sys.exit()


