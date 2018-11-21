#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os,sys
import json
import glob
import sqlite3
import re
#import plyvel
#import leveldb
#import jsontree

reload(sys)
sys.setdefaultencoding('utf8')


result_file = open("./watson_drug_count.csv", "w")
result_hash = {}

gene_hash = {}





def find_text(key, dict):
    text = ""
    if dict.has_key(key):
        text = dict[key]

    return text


def build_sql(col, obj, sql_hash):
    text = find_text(col, obj)
    text = text.replace("'", "''").replace('"', '\"')
    sql_hash[col] = text


def get_gene_json(serialno, json_dict):

    #col = ["serialno","GeneName","GeneSummary","Chromosome","PrimaryTranscript","Position","GeneAnnotation",
    #    "Variant","VariantId","VariantType","ChromosomeLocationChange","AminoAcid","DNACoding",
    #    "Classification","ClassificationSource","Effect","InputValue","TranscriptId","AlleleFrequency",
    #    "SequencingDepth","AnnotationText","OtherDatabaseIds"
    #]

    sql_hash = {
        "serialno": serialno,
        "GeneName": "",
        "GeneSummary": "",
        "Chromosome": "",
        "PrimaryTranscript": "",
        "Position": "",
        "GeneAnnotation": "",
        "Variant": "",
        "VariantId": "",
        "VariantType": "",
        "ChromosomeLocationChange": "",
        "AminoAcid": "",
        "DNACoding": "",
        "Classification": "",
        "ClassificationSource": "",
        "Effect": "",
        "InputValue": "",
        "TranscriptId": "",
        "AlleleFrequency": "",
        "SequencingDepth": "",
        "AnnotationText": "",
        "OtherDatabaseIds": ""
    }

    #db = plyvel.DB('./watson.ldb', create_if_missing=True)
    #print db.get("gene").get("Metadata")
    #print db.get("Metadata")
    #sys.exit()


    conn = sqlite3.connect("./watson_data.db")

    if json_dict.has_key("Genes"):
        gene_list = json_dict["Genes"]
        gene_hash[serialno] = {}

        for gl in gene_list:
            GN = build_sql("GeneName", gl, sql_hash)
            GS = build_sql("GeneSummary", gl, sql_hash)
            CS = build_sql("Chromosome", gl, sql_hash)
            PT = build_sql("PrimaryTranscript", gl, sql_hash)
            PS = build_sql("Position", gl, sql_hash)
            GA = build_sql("GeneAnnotation", gl, sql_hash)


            gene_t = find_text("GeneName", gl)
            gene_s = find_text("GeneSummary", gl)

            gene_hash[serialno][gene_t] = gene_s
            continue


            for vas in find_text("Variants", gl):
                VT = build_sql("Variant", vas, sql_hash)
                VID = build_sql("VariantId", vas, sql_hash)
                VTYPE = build_sql("VariantType",vas, sql_hash)
                CLC = build_sql("ChromosomeLocationChange", vas, sql_hash)
                AA = build_sql("AminoAcid", vas, sql_hash)
                DNAC = build_sql("DNACoding", vas, sql_hash)
                CF = build_sql("Classification", vas, sql_hash)
                CFS = build_sql("ClassificationSource", vas, sql_hash)
                EF = build_sql("Effect", vas, sql_hash)
                #IV = build_sql("InputValue", vas)
                TI = build_sql("TranscriptId", vas, sql_hash)
                AF = build_sql("AlleleFrequency", vas, sql_hash)
                SD = build_sql("SequencingDepth", vas, sql_hash)

                IV_LOG2 = ""
                if vas.has_key("InputValue"):
                    if vas["InputValue"].has_key("Unit"):
                        unit = vas["InputValue"]["Unit"]
                        if unit == "log2":
                            IV_LOG2 = vas["InputValue"]["Value"]
                            sql_hash["InputValue"] = IV_LOG2


                AT = ""
                if vas.has_key("AlterationSummary"):
                    if vas["AlterationSummary"].has_key("WfGAnnotations"):
                        vas2 = vas["AlterationSummary"]["WfGAnnotations"][0]
                        AT = build_sql("AnnotationText", vas2, sql_hash)

                ODI = ""
                if vas.has_key("OtherDatabaseIds"):
                    for odi in find_text("OtherDatabaseIds", vas):
                        ODI += odi["Source"]+":"+odi["Id"] + "|"
                        sql_hash["OtherDatabaseIds"] = ODI


                result_sql = "insert into Gene "
                col_sql = ""
                val_sql = ""
                for key, value in sql_hash.items():
                    col_sql += key + ","
                    val_sql += "'" + str(value) + "'" + ","

                result_sql += "(" + col_sql.rstrip(",") + ") values (" + val_sql.rstrip(",") + ");"

                conn.execute(result_sql)
                conn.commit()

    conn.close()



def get_drug_json(serialno, json_dict):

    #col = ["serialno","DrugName","HighestEvidenceLevel","Category","ApprovalStatus","MOA"]

    sql_hash = {
        "serialno": serialno,
        "DrugName": "",
        "HighestEvidenceLevel": "",
        "Category": "",
        "ApprovalStatus": "",
        "MOA": ""
    }

    conn = sqlite3.connect("./watson_data.db")

    if json_dict.has_key("Drugs"):
        drug_list = json_dict["Drugs"]

        for dl in drug_list:
            DN = build_sql("DrugName", dl, sql_hash)
            HEL = build_sql("HighestEvidenceLevel", dl, sql_hash)
            CG = build_sql("Category", dl, sql_hash)
            AS = build_sql("ApprovalStatus", dl, sql_hash)
            MOA = build_sql("MOA", dl, sql_hash)

            #data_arr = [serialno,DN,HEL,CG,AS,MOA]
            
            #sql = "insert into Drug values (" + ",".join(data_arr).rstrip(",") + "); "

            result_sql = "insert into Drug "
            col_sql = ""
            val_sql = ""
            for key, value in sql_hash.items():
                col_sql += key + ","
                val_sql += "'" + str(value) + "'" + ","

            result_sql += "(" + col_sql.rstrip(",") + ") values (" + val_sql.rstrip(",") + ");"

            conn.execute(result_sql)
            conn.commit()

    conn.close()





def get_summaryinfo_json(serialno, user, folder, files, caseid, json_dict):

    #col = ["serialno","Diagnosis","Age","Gender","Folder","Files","CaseId","CaseName","SampleName"]

    sql_hash = {
        "serialno": serialno,
        "UserId": user,
        "AnalysisDate": "",
        "Version": "",
        "ConditionId": "",
        "ConditionName": "",
        "Age": "",
        "Gender": "",
        "Folder": folder,
        "Files": files,
        "CaseId": caseid,
        "CaseName": "",
        "SampleName": "",
        "CaseSummary": ""
    }

    conn = sqlite3.connect("./watson_data.db")

    if json_dict.has_key("SampleInfo"):
        si = json_dict["SampleInfo"]

        if si.has_key("ConditionId"):
            sql_hash["ConditionId"] = si["ConditionId"]
        if si.has_key("ConditionName"):
            sql_hash["ConditionName"] = si["ConditionName"]
        if si.has_key("Age"):
            sql_hash["Age"] = si["Age"]
        if si.has_key("Gender"):
            sql_hash["Gender"] = si["Gender"]


    if json_dict.has_key("UserId"):
        sql_hash["UserId"] = json_dict["UserId"]
    if json_dict.has_key("AnalysisDate"):
        sql_hash["AnalysisDate"] = json_dict["AnalysisDate"]
    if json_dict.has_key("Version"):
        sql_hash["Version"] = json_dict["Version"]
    if json_dict.has_key("CaseName"):
        sql_hash["CaseName"] = json_dict["CaseName"]
    if json_dict.has_key("SampleName"):
        sql_hash["SampleName"] = json_dict["SampleName"]
    if json_dict.has_key("CaseSummary"):
        str = ""
        for key in json_dict["CaseSummary"]:
            str += key+": "+json_dict["CaseSummary"][key]+"\n"
        sql_hash["CaseSummary"] = str


    #data_arr = [serialno,casename,Diagnosis,Age,Gender,folder,files,caseid,casename,samplename]
    #sql = "insert into SampleInfo values (" + ",".join(data_arr).rstrip(",") + "); "

    result_sql = "insert into SampleInfo "
    col_sql = ""
    val_sql = ""
    for key, value in sql_hash.items():
        col_sql += key + ","
        val_sql += "'" + value + "'" + ","

    result_sql += "(" + col_sql.rstrip(",") + ") values (" + val_sql.rstrip(",") + ");"

    conn.execute(result_sql)
    conn.commit()

    conn.close()


   



def get_ct_json(serialno, json_dict):

    #col = ["serialno","NCTId","Title","Phase","RecruitingStatus","CountryList"]

    sql_hash = {
        "serialno": serialno,
        "NCTId": "",
        "Title": "",
        "Phase": "",
        "RecruitingStatus": "",
        "CountryList": ""
    }

    conn = sqlite3.connect("./watson_data.db")

    if json_dict.has_key("ClinicalTrials"):
        ct_list = json_dict["ClinicalTrials"]

        for ct in ct_list:
            NCTId = build_sql("NCTId", ct, sql_hash)
            Title = build_sql("Title", ct, sql_hash)
            Phase = build_sql("Phase", ct, sql_hash)
            RS = build_sql("RecruitingStatus", ct, sql_hash)

            cl_arr = []
            for cl in ct["CountryList"]:
                cl_arr.append(cl["Name"])
            CL = "|".join(cl_arr)

            #data_arr = [serialno,NCTId,Title,Phase,RS,CL]
            #sql = "insert into ClinicalTrials values (" + ",".join(data_arr).rstrip(",") + "); "

            result_sql = "insert into ClinicalTrials "
            col_sql = ""
            val_sql = ""
            for key, value in sql_hash.items():
                col_sql += key + ","
                val_sql += "'" + str(value) + "'" + ","

            result_sql += "(" + col_sql.rstrip(",") + ") values (" + val_sql.rstrip(",") + ");"


            conn.execute(result_sql)
            conn.commit()

    conn.close()




def get_relation_json(serialno, json_dict):

    col = ["serialno","GeneName","DrugName","Type","TrialPhase","EvidenceLevel","Evidence","EvidenceSummary"]
    conn = sqlite3.connect("./watson_data.db")

    data_arr = []

    result_hash[serialno] = {}

    if json_dict.has_key("Relations"):
        if json_dict["Relations"].has_key("GeneDrugEvidenceLevels"):
            GDEL_list = json_dict["Relations"]["GeneDrugEvidenceLevels"]
            for gdel in GDEL_list:
                GeneName = find_text("GeneName", gdel)
                print GeneName

                result_hash[serialno][GeneName] = {
                    "ApprovedSameCancerDrugs": 0,
                    "InvestigationalSameCancerDrugs": 0,
                    "ApprovedOtherCancerDrugs": 0
                }


                if gene_hash[serialno][GeneName].find("loss") != -1:
                    continue

                TYPE = "ApprovedSameCancerDrugs"
                for dl in find_text(TYPE, gdel):
                    DN = find_text("DrugName", dl)
                    EL = find_text("EvidenceLevel", dl)
                    TP = find_text("TrialPhase", dl)
                    #E = find_text("Evidences", dl)
                    #ES = find_text("EvidenceSummary", dl)

                    print "----ApprovedSameCancerDrugs-----"
                    print DN
                    result_hash[serialno][GeneName]["ApprovedSameCancerDrugs"] += 1
                    

                    data_arr = [serialno,GeneName,DN,TYPE,str(TP),str(EL),"",""]
                    #data_arr = [serialno,GeneName,DN,TYPE,str(TP),str(EL),E,ES]
                    data_arr = ['"'+i+'"' for i in data_arr]

                    sql = "insert into GeneDrugEvidenceLevels values (" + ",".join(data_arr).rstrip(",") + ");"
                    #print "--------ApprovedSameCancerDrugs-------------------"
                    #print sql
                    conn.execute(sql)
                    conn.commit()

                TYPE = "InvestigationalSameCancerDrugs"
                for dl in find_text(TYPE, gdel):
                    DN = []
                    EL = []
                    TP = find_text("TrialPhase", dl)
                    E = []
                    ES = []

                    for d in find_text("Drugs", dl):
                        DN.append(find_text("DrugName", d))
                        EL.append(find_text("EvidenceLevel", d))

                        e_summary = ""
                        e_num = ""

                        if d.has_key("Evidences"):
                            buf = d["Evidences"]
                            if buf[0].has_key("Summary"):
                                e_summary = buf[0]["Summary"]
                            if buf[0].has_key("Evidence"):
                                e_num = buf[0]["Evidence"]

                        E.append(e_summary)
                        ES.append(e_num)

                    print "---------InvestigationalSameCancerDrugs---------------"
                    print len(DN),DN
                    result_hash[serialno][GeneName]["InvestigationalSameCancerDrugs"] += len(DN)


                    
                    data_arr = [serialno,GeneName,"|".join(DN),TYPE,str(TP),"","",""]
                    #data_arr = [serialno,GeneName,"|".join(DN),TYPE,str(TP),"|".join(EL),"|".join(E),"|".join(ES)]
                    data_arr = ['"'+i+'"' for i in data_arr]

                    #print "--------ApprovedSameCancerDrugs-------------------"
                    sql = "insert into GeneDrugEvidenceLevels values (" + ",".join(data_arr).rstrip(",") + ");"
                    conn.execute(sql)
                    conn.commit()


                TYPE = "ApprovedOtherCancerDrugs"
                for dl in find_text(TYPE, gdel):
                    DN = find_text("DrugName", dl)
                    EL = find_text("EvidenceLevel", dl)
                    TP = find_text("TrialPhase", dl)
                    #E = find_text("Evidences", dl)
                    #ES = find_text("EvidenceSummary", dl)

                    print "----ApprovedOtherCancerDrugs-----"
                    print len(DN),DN
                    result_hash[serialno][GeneName]["ApprovedOtherCancerDrugs"] += 1


                    data_arr = [serialno,GeneName,DN,TYPE,str(TP),str(EL),"",""]
                    #data_arr = [serialno,GeneName,DN,TYPE,str(TP),str(EL),E,ES]
                    data_arr = ['"'+i+'"' for i in data_arr]

                    sql = "insert into GeneDrugEvidenceLevels values (" + ",".join(data_arr).rstrip(",") + ");"
                    conn.execute(sql)
                    conn.commit()


                print result_hash[serialno]


    conn.close()




def func(serialno, user, folder, files, caseid):

    #file = glob.glob("./wfg_api/output/"+user+"/download/"+serialno+"/"+folder+"/*/*/standard_report.json")[0]

    file = "./json/"+serialno+".json"

    with open(file, "r") as f:
        json_dict = json.load(f)

        get_gene_json(serialno, json_dict)
        #get_drug_json(serialno, json_dict)
        #get_summaryinfo_json(serialno, user, folder, files, caseid, json_dict)
        #get_ct_json(serialno, json_dict)
        get_relation_json(serialno, json_dict)


import glob

files = glob.glob("./manual/*")

for buf in files:
    file = buf
    type = ""

    #if buf != "./manual/D-B001-119-2012-LPL-Te1.genomon_mutation.result.filt.all.combined_20180720_anno.xlsx":
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
    user = ""
    folder = ""
    files = ""
    caseid = ""

    func(rimsid, user, folder, files, caseid)



header = ["LIMSID","Gene","ApprovedSameCancerDrugs","InvestigationalSameCancerDrugs","ApprovedOtherCancerDrugs"]
result_file.write(",".join(header)+"\n")
result_str = ""

for limsid in result_hash:
    arr = result_hash[limsid]
    for gene in arr:
        result_str += limsid+","+gene+","+str(arr[gene]["ApprovedSameCancerDrugs"])+","+str(arr[gene]["InvestigationalSameCancerDrugs"])+","+str(arr[gene]["ApprovedOtherCancerDrugs"])+"\n"



result_file.write(result_str)
result_file.close()


