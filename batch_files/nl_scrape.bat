@Echo Off

CALL "D:\Py Projects\Scrapy\.venv\Scripts\activate.bat"

CD "D:\Py Projects\Scrapy\scrape01"

scrapy crawl noels

CALL "D:\Py Projects\Scrapy\.venv\Scripts\deactivate.bat"