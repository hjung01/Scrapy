from pathlib import Path

import scrapy
import json
import csv


class hnSpider(scrapy.Spider):
    name = "harveys"
    # custom_settings = {
    #     'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    # }

    def start_requests(self):
        urls = [
            f"https://www.harveynorman.co.nz/whiteware/refrigeration/side-by-side/lg-655l-side-by-side-fridge-freezer-matte-black-gs-b655mbl.html",
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        p_info_json  = response.xpath("//script[contains(., 'gtin')]/text()").get()
        print(p_info_json)