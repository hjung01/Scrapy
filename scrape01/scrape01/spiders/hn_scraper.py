from pathlib import Path

import scrapy
import json
import csv


class hnSpider(scrapy.Spider):
    name = "harveys"

    def start_requests(self):
        urls = [
            f"https://www.harveynorman.co.nz/whiteware/refrigeration/side-by-side/lg-655l-side-by-side-fridge-freezer-matte-black-gs-b655mbl.html",
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        p_info_json  = response.xpath("//script[contains(., 'gtin')]/text()").get()
        print(p_info_json)