from pathlib import Path

import scrapy
import json
import csv


class hnSpider(scrapy.Spider):
    name = "harveys"

    def start_requests(self):
        urls = [
            f"https://www.harveynorman.co.nz/whiteware/refrigeration/side-by-side/",
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        p_info_json  = response.xpath('//span[@class="price-num"]').get()
        print(p_info_json)