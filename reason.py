#! /usr/bin/env python

import os
import sys
import re
import pandas

result_hash = {}
all_count = [0,0,0,0,0,0,0,0,0]


def func(rimsid, filepath, type):
    y_path = filepath

    #col_arr = []
    #if type == "0711":
    #    col_arr = [0,1,15,16,17,23,26,203,204]
    #if type == "0720":
    #    col_arr = [0,1,15,16,17,23,26,203,204]
        #col_arr = [0,1,14,15,16,20,23,199,200]
    #if type == "1105":
    #    col_arr = [0,1,12,13,14,20,23,156,157]

    #y_path = "./final/F-"+rimsid+".genomon_mutation.result.filt.all.combined_20180720.xlsx"
    df = pandas.read_excel(y_path,
        usecols=[0,1,2,3,7,8],
        #usecols=[0,14,15,16,20,23,199,200],
        sheet_name=1
    )

    LOG = open("./log.txt", "a")

    df = df.fillna(0)

    arr = [0,0,0,0,0,0,0,0,0]

    for index, row in df.iterrows():
        drug = int(row[0])
        w_drug = int(row[1])
        m_final = row[2]

        print row[3]
        if row[3] == 0:
            print "continue"
            continue

        reason = str(row[3]).split(",")
        print reason

        gene = row[4]
        gene_m = row[5]
        

        if gene == "U2AF1;U2AF1L5":
            gene = "U2AF1"

        for r in reason:
            #print r
            index = int(float(r))-1
            #print index

            before = arr[index]
            arr[index] = int(before) + 1

            before = all_count[index]
            all_count[index] = int(before) + 1


    result_hash[rimsid] = arr
    print arr




import glob

files = glob.glob("./manual/*")

for buf in files:
    file = buf
    type = ""

    #if buf == "./manual/D-B008-115-2016-MM-Tu1.genomon_mutation.result.filt.all.combined_20180711_anno.xlsx":
    #    continue

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


result_file = open("./all_count_rimsid.csv", "w")
header = ["rimsid","1","2","3","4","5","6","7","8","9"]
result_file.write(",".join(header)+"\n")

for rimsid in result_hash:
    arr = result_hash[rimsid]
    arr_str = [str(n) for n in arr]
    result_file.write(rimsid+","+",".join(arr_str)+"\n")


result_file = open("./all_count.txt", "w")
for count in all_count:
    index = all_count.index(count)
    result_file.write(str(index)+","+str(count)+"\n")


# sys.exit()


