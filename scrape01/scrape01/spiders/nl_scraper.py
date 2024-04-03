from pathlib import Path

import scrapy
from scrapy.spiders import Spider
import json
import csv
import os
import time


class noelsSpider(scrapy.Spider):
    name = "noels" #name of spider
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    } # custom user agent
    start_urls = [f'https://www.noelleeming.co.nz/search?q=&start=0'] #initial url to start scraping
    filename = 'nl_prod_info.csv' #filename for csv output of data

    def __init__(self, *args, **kwargs):
        super(noelsSpider, self).__init__(*args, **kwargs)
        if Path(self.filename).exists(): #checks if csv file already exists
            os.remove(self.filename) # if file exists, delete the file
        time.sleep(15)

    def parse(self, response):
        p_info_json  = response.xpath('//div[@class="product-tile"]/@data-gtm-product').getall() #xpath for product info html
        products = [json.loads(product) for product in p_info_json] #parse each JSON string into python dictionary
        filename = 'nl_prod_info.csv' #file to write data to

        with Path(filename).open('a', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=products[0].keys() if products else [])
            if csvfile.tell() == 0 and products: #if file is empty and there is product data
                writer.writeheader() #write header row for csv
            for product in products: #for each product in the dictionary
                writer.writerow(product) #write product data in the row
        
        self.log(f'Appended to file {filename}') #logs message that data was successfully appended
        
        if products: #if there was any product information on the page
            current_start = int(response.url.split('start=')[-1]) #extracts current 'start' parameter from page url for pagination
            next_start = current_start + 32 #32 products on each page
            next_page_url = f"https://www.noelleeming.co.nz/search?q=&start={next_start}" #constructs new url to scrape +=32
            yield response.follow(next_page_url, self.parse) #schedules request to next page, calling parse method and looping
