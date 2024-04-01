from pathlib import Path

import scrapy
import json
import csv


class hnSpider(scrapy.Spider):
    name = "harveys"
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
    }

    def start_requests(self):
        urls = [
            f"https://www.harveynorman.co.nz/whiteware/refrigeration/side-by-side/",
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        print(response.text)
        p_info_json  = response.xpath('//span[@class="price-num"]').getall()
        print(p_info_json)