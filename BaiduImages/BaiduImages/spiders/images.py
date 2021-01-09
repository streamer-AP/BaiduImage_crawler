# -*- coding: utf-8 -*-
from scrapy import Spider, Request
from urllib.parse import quote
from BaiduImages.items import BaiduimagesItem
import json
import time
import os
class ImagesSpider(Spider):
    name = 'images'
    allowed_domains = ['images.baidu.com']
    start_urls = ['https://images.baidu.com/']
    def parse(self, response,queryWordindex):
        images = json.loads(response.body)['data']
        for image in images:
            item = BaiduimagesItem()
            try:
                item['url'] = image.get('thumbURL')
                item['queryWordindex'] = queryWordindex
                item["path"]=item["url"].split('/')[-1]
                yield item
            except Exception as e:
                print("------")
                print(e)
        pass

    def start_requests(self):
        data = {'queryWord': '', 'word': '','max_page':30}
        with open(self.setting.get("OUTPUT_FILE_PATH"),"w",encoding="utf-8") as json_file:
           print("create new query json file") 
        with open(self.settings.get("QUERY_LIST_FILE_PATH"),"r",encoding="utf-8") as query_file:
            lines=query_file.readlines()
            for line in lines:
                line=line.strip("\n").split(",")
                if len(line)==3:
                    data["queryWordindex"]=line[0]                    
                    data["queryWord"]=line[1]
                    data["max_page"]=eval(line[2])
                    self.word=data["word"]
                    if not os.path.exists(os.path.join(self.settings.get("IMAGES_STORE"),data["word"])):
                        os.mkdir(os.path.join(self.settings.get("IMAGES_STORE"),data["word"]))

                    for page in range(1, data["max_page"] + 1):
                        data['pn'] = page * 30
                        url =f"https://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&word={quote(data['queryWord'])}&pn={page*30}"
                        request=Request(url,callback=self.parse)
                        request.cb_kwargs["queryWordindex"]=data["queryWordindex"]
                        time.sleep(1)
                        yield request
                else:
                    print("invalid line {}".format(line))
                    continue