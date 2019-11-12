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
        base_url = 'https://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&ct=201326592&is=&fp=result&queryWord='
        with open(self.settings.get("QUERY_LIST_FILE_PATH"),"r") as query_file:
            lines=query_file.readlines()
            for line in lines:
                line=line.strip("\n").split(",")
                if len(line)==4:
                    data["queryWordindex"]=line[0]                    
                    data["queryWord"]=line[1]
                    data["word"]=line[2]
                    data["max_page"]=eval(line[3])
                    self.word=data["word"]
                    if not os.path.exists(os.path.join(self.settings.get("IMAGES_STORE"),data["word"])):
                        os.mkdir(os.path.join(self.settings.get("IMAGES_STORE"),data["word"]))
                    for page in range(1, data["max_page"] + 1):
                        data['pn'] = page * 30
                        url = base_url + quote(data['queryWord']) + '&cl=2&lm=-1&ie=utf-8&oe=utf-8&adpicid=&st=-1&z=&ic=0&word=' + \
                            quote(data['word']) + '&s=&se=&tab=&width=&height=&face=0&istype=2&qc=&nc=1&fr=&expermode=&pn=' + \
                            quote(str(data['pn'])) + '&rn=30&gsm=' + str(hex(data['pn']))
                        request=Request(url,callback=self.parse)
                        request.cb_kwargs["queryWordindex"]=data["queryWordindex"]
                        time.sleep(0.1)
                        yield request
                else:
                    print("invalid line {}".format(line))
                    continue