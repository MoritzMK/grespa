import os
import scrapy
import logging
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from appointment_comparer.scraper.scraper.spiders.author_details import AuthorDetailsSpider
    
class ScrapyLauncher():

    def __init__(self):
        settings_file_path = 'appointment_comparer.scraper.scraper.settings' # The path seen from root, ie. from main.py
        os.environ.setdefault('SCRAPY_SETTINGS_MODULE', settings_file_path)
        self.settings = get_project_settings()
        self.crawler_process = CrawlerProcess(self.settings)
        self.author_details_spider = AuthorDetailsSpider
        self.logger = logging.getLogger('scrapyLauncher')

    def crawl_author(self, author_id):
        self.crawler_process.crawl(self.author_details_spider, author_id=author_id)
        self.logger.debug('Start crawler.')
        self.crawler_process.start()
        self.crawler_process.join()
        self.logger.debug('Crawler joined.')

    def get_author_data(self, author_id):
        path = self.settings.get("SCRAPED_AUTHORS_PATH").format(author_id)
        if not os.path.exists(path):
            self.logger.info('Path {} for author_id {} not found.'.format(path, author_id))
            return None
        with open(path, 'r') as file:
            data = file.read()

            return data


