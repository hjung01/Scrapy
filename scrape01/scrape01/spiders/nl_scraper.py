from pathlib import Path

import scrapy
import json
import csv


class noelsSpider(scrapy.Spider):
    name = "noels"

    def start_requests(self):
        urls = [
            f"https://www.noelleeming.co.nz/c/appliances",
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        p_info_json  = response.xpath('//div[@class="product-tile"]/@data-gtm-product').getall()
        products = [json.loads(product) for product in p_info_json]
        filename = 'nl_prod_info.csv'

        with Path(filename).open('w', newline='', encoding='utf-8') as csvfile:
            if products:
                fieldnames = products[0].keys()
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                writer.writeheader()

                for product in products:
                    writer.writerow(product)
        
        self.log(f'Saved file {filename}')
        