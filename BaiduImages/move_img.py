import os
import shutil
import json

query_dict={}
with open("BaiduImages/query_list.txt","r") as query_list_file:
    lines=query_list_file.readlines()
    for line in lines:
        line=line.strip("\n").split(",")
        query_dict[line[0]]=line[2]
query_json=json.load(open("BaiduImages/query.json","r"))
for json_item in query_json:
    img_path="BaiduImages/images/"+json_item["path"]
    shutil.move(img_path,"BaiduImages/images/"+query_dict[json_item["queryWordindex"]])
