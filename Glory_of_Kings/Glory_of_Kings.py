# !/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2021-01-31 08:55:49
# Project: Glory_of_Kings

from pyspider.libs.base_handler import *
from lxml import etree
import time

class Handler(BaseHandler):
    crawl_config = {
    }
    path = r'G:/python培训/王者荣耀图像/'
    @every(minutes=0, seconds=10)
    def on_start(self):
        self.crawl('https://pvp.qq.com/web201605/herolist.shtml', callback=self.index_page, validate_cert=False,fetch_type='js')

    @config(age=60)
    def index_page(self, response):
        html = etree.HTML(response.text)
        img_urls = html.xpath('//ul[@class="herolist clearfix"]/li/a/img/@src')
        heros = html.xpath('//ul[@class="herolist clearfix"]/li/a/text()')
        for name,url in zip(heros,img_urls):
            names = name+'.jpg'
            urls = "http:"+url
            self.crawl(urls,callback=self.detail_page,save={"name":names})

    @config(priority=2)
    def detail_page(self, response):
        #print(self.path+response.save["name"])
        with open(self.path+response.save["name"],"wb") as f:
            f.write(response.content)
