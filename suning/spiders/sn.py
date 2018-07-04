# -*- coding: utf-8 -*-
import scrapy
from copy import deepcopy

from suning.items import SuningItem
import re


class SnSpider(scrapy.Spider):
    name = "sn"
    allowed_domains = ["suning.com"]
    start_urls = [
        'http://snbook.suning.com/web/trd-fl/999999/0.htm'
    ]


    def parse(self, response):
        classfiy_list=response.xpath("//div[@class='detail-sort']/ul/li")
        for classfiy in classfiy_list:
            item=SuningItem()
            item["classify"]=classfiy.xpath(".//div[@class='second-sort']/a/text()").extract_first()
            classify_url=classfiy.xpath(".//div[@class='three-sort']/a")
            for href in classify_url:
                item["href"]=href.xpath("./@href").extract_first()
                item["classify_name"] = href.xpath("./text()").extract_first()
                if item["href"] is not None:
                    item["href"]="http://snbook.suning.com/"+item["href"]
                    yield scrapy.Request(
                        item["href"],
                        callback=self.detail_parse,
                        meta={"item": deepcopy(item)}
                    )




    def detail_parse(self,response):
        item=deepcopy(response.meta["item"])
        li_list = response.xpath("//div[@id='mainSearch']/div[1]/ul/li")
        for li in li_list:
            item["book_name"] = li.xpath(".//div[@class='book-title']/a/@title").extract_first()
            item["author"] = li.xpath(".//div[@class='book-author']/a/text()").extract_first()
            item["detail_url"] = li.xpath(".//div[@class='book-title']/a/@href").extract_first()

            yield scrapy.Request(
                item["detail_url"],
                callback=self.detail_price,
                meta={"item": deepcopy(item)}
            )

        pagecount = int(re.findall('var pagecount=(.*?);', response.body.decode())[0])
        currentPage = int(re.findall('var currentPage=(.*?);', response.body.decode())[0])

        if currentPage < pagecount:
            next_url = item["href"] + "pageNumber={}&sort=0".format(currentPage + 1)
            yield scrapy.Request(
                next_url,
                callback=self.parse,
                meta={"item": item}
            )


    def detail_price(self,response):
        item=response.meta["item"]
        book_id=re.findall(r'(\d+).htm$',str(item["detail_url"]))[0]
        price_url="http://snbook.suning.com/web/ebook/checkPriceShowNew.do?bookId={}&completeFlag=2".format(book_id)
        yield scrapy.Request(
            price_url,
            callback=self.get_price,
            meta={"item":item}
        )

    def get_price(self,response):
        price_list=response.xpath("//span/em")
        for price in price_list:
            item = response.meta["item"]
            item["price"]=price.xpath("./text()").extract_first()
            yield item