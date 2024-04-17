from pathlib import Path
import scrapy
from scrapy.spiders import Spider
import json
import csv
import os
import time
import logging
from scrapy.utils.log import configure_logging
from datetime import datetime
import sqlite3


class noelsSpider(scrapy.Spider):
    name = "noels" #name of spider
    start_urls = [f'https://www.noelleeming.co.nz/search?cgid=root&start=0#maincontent'] #initial url to start scraping
    filename = 'nl_prod_info.csv' #filename for csv output of data

    #logging of spider
    configure_logging(install_root_handler=False)
    logging.basicConfig(
        filename=f'D:\Py Projects\Scrapy\log_files\{name} spider.log',
        format = '%(asctime)s [%(name)s] %(levelname)s: %(message)s',
        datefmt = '%Y-%m-%d %H:%M:%S',
        level=logging.INFO
    )


    def __init__(self, *args, **kwargs):
        super(noelsSpider, self).__init__(*args, **kwargs)
        self.setup_database()


    def parse(self, response):
        p_info_json  = response.xpath('//div[@class="product-tile"]/@data-gtm-product').getall() #xpath for product info html
        products = [json.loads(product) for product in p_info_json] #parse each JSON string into python dictionary
        today = datetime.now().date()

        for product in products:
            product['date_collected'] = today
            self.cursor.execute('''
            INSERT INTO NL_product_data (
                date_collected, id, name, brand, productEAN, productBadges, productRating, category,
                primaryCategoryId, productSecondaryNavigationCategory, productCategoryLevel1, productCategoryLevel2,
                productCategoryLevel3, productCategoryLevel4, productCategoryLevel5, productCategoryLevel6,
                productCategoryLevel7, productChannelType, price, productThenPrice
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            product.get('date_collected', datetime.now().date()),
            product.get('id', ''),
            product.get('name', ''),
            product.get('brand', ''),
            product.get('productEAN', ''),
            product.get('productBadges', ''),
            product.get('productRating', 0),  # Assuming default rating is 0 if not found
            product.get('category', ''),
            product.get('primaryCategoryId', ''),
            product.get('productSecondaryNavigationCategory', ''),
            product.get('productCategoryLevel1', ''),
            product.get('productCategoryLevel2', ''),
            product.get('productCategoryLevel3', ''),
            product.get('productCategoryLevel4', ''),
            product.get('productCategoryLevel5', ''),
            product.get('productCategoryLevel6', ''),
            product.get('productCategoryLevel7', ''),
            product.get('productChannelType', ''),
            product.get('price', 0),  # Assuming default price is 0 if not found
            product.get('productThenPrice', 0)  # Assuming default then price is 0 if not found
))
        self.conn.commit()
        
        if products: #if there was any product information on the page
            current_start = int(response.url.split('start=')[-1]) #extracts current 'start' parameter from page url for pagination
            next_start = current_start + 32 #32 products on each page
            next_page_url = f"https://www.noelleeming.co.nz/search?cgid=root&start={next_start}#maincontent" #constructs new url to scrape +=32
            yield response.follow(next_page_url, self.parse) #schedules request to next page, calling parse method and looping


    def setup_database(self):
        self.conn = sqlite3.connect(f'D:\SQLite DB\scrape_data.db')  # The database file
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS NL_product_data (
                date_collected TEXT,
                id TEXT,
                name TEXT,
                brand TEXT,
                productEAN TEXT,
                productBadges TEXT,
                productRating INTEGER,
                category TEXT,
                primaryCategoryId TEXT,
                productSecondaryNavigationCategory TEXT,
                productCategoryLevel1 TEXT,
                productCategoryLevel2 TEXT,
                productCategoryLevel3 TEXT,
                productCategoryLevel4 TEXT,
                productCategoryLevel5 TEXT,
                productCategoryLevel6 TEXT,
                productCategoryLevel7 TEXT,
                productChannelType TEXT,
                price INTEGER,
                productThenPrice INTEGER
            )
        ''')
        self.conn.commit()


    def closed(self, reason):
        self.conn.close()