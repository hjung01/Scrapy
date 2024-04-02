from pathlib import Path

import scrapy
from scrapy.spiders import Spider
import json
import csv
import os


class noelsSpider(scrapy.Spider):
    name = "noels"
    start_urls = [f'https://www.noelleeming.co.nz/c/appliances?start=0']
    filename = 'nl_prod_info.csv'

    def __init__(self, *args, **kwargs):
        super(noelsSpider, self).__init__(*args, **kwargs)
        if Path(self.filename).exists():
            os.remove(self.filename)

    def parse(self, response):
        p_info_json  = response.xpath('//div[@class="product-tile"]/@data-gtm-product').getall()
        products = [json.loads(product) for product in p_info_json]
        filename = 'nl_prod_info.csv'

        with Path(filename).open('a', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=products[0].keys() if products else [])
            if csvfile.tell() == 0 and products:
                writer.writeheader()
            for product in products:
                writer.writerow(product)
        
        self.log(f'Appended to file {filename}')
        
        if products:
            current_start = int(response.url.split('start=')[-1])
            next_start = current_start + 32
            next_page_url = f"https://www.noelleeming.co.nz/c/appliances?start={next_start}"
            yield response.follow(next_page_url, self.parse)
