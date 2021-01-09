import os
import shutil
import json

query_dict={}
with open("query_list.txt","r",encoding="utf-8") as query_list_file:
    lines=query_list_file.readlines()
    for line in lines:
        line=line.strip("\n").split(",")
        query_dict[line[0]]=line[1]
query_json=json.load(open("query.json","r",encoding="utf-8"))
for json_item in query_json:
    img_path=os.path.join("images",json_item['path'])
    dst_path=os.path.join("images",query_dict[json_item["queryWordindex"]],json_item['path'])
    if os.path.exists(dst_path):
        os.remove(dst_path)
    shutil.move(img_path,dst_path)
