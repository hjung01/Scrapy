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
        p_info_json  = response.xpath('//script[@type="application/javascript"]').get()
        products = [json.loads(product) for product in p_info_json]
        filename = 'hn_prod_info.csv'

        with Path(filename).open('w', newline='', encoding='utf-8') as csvfile:
            if products:
                fieldnames = products[0].keys()
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                writer.writeheader()

                for product in products:
                    writer.writerow(product)
        
        self.log(f'Saved file {filename}')