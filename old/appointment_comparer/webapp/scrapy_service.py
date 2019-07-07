import os
import scrapy
from scrapy.crawler import CrawlerProcess, CrawlerRunner
from scrapy.utils.project import get_project_settings
from appointment_comparer.scraper.scraper.spiders.author_details import AuthorDetailsSpider
from twisted.logger import Logger
from klein import route, run

    

class MyCrawlerRunner(CrawlerRunner):
    """
    Crawler object that collects items and returns output after finishing crawl.
    """
    def crawl(self, crawler_or_spidercls, *args, **kwargs):
        # keep all items scraped
        self.items = []

        # create crawler (Same as in base CrawlerProcess)
        crawler = self.create_crawler(crawler_or_spidercls)

        # handle each item scraped
        crawler.signals.connect(self.item_scraped, signals.item_scraped)

        # create Twisted.Deferred launching crawl
        dfd = self._crawl(crawler, *args, **kwargs)

        # add callback - when crawl is done cal return_items
        dfd.addCallback(self.return_items)
        return dfd

    def item_scraped(self, item, response, spider):
        self.items.append(item)

    def return_items(self, result):
        return self.items


class ScrapyService():

    def __init__(self):
        settings_file_path = 'appointment_comparer.scraper.scraper.settings' # The path seen from root, ie. from main.py
        os.environ.setdefault('SCRAPY_SETTINGS_MODULE', settings_file_path)
        self.settings = get_project_settings()
        # self.crawler_process = CrawlerProcess(self.settings)
        self.crawler_runner = CrawlerRunner(self.settings)
        self.author_details_spider = AuthorDetailsSpider
        self.logger = Logger()
        self.scrape_in_progress = False

    def crawl_author(self, author_id):
        if not self.scrape_in_progress:
            self.logger.debug('Start crawler.')
            self.scrape_in_progress = True
            # self.crawler_process.crawl(self.author_details_spider, author_id=author_id)
            process = self.crawler_runner.crawl(self.author_details_spider, author_id=author_id)
            process.addCallback(self._crawler_finished)
            self.logger.debug('Crawler started.')

    def _crawler_finished(self):
        self.scrape_in_progress = False
        

    def get_author_data(self, author_id):
        if self.scrape_in_progress:
            return None
        
        # Get path
        path = self.settings.get("SCRAPED_AUTHORS_PATH").format(author_id)

        # Check if path exists
        if not os.path.exists(path):
            self.logger.info('Path {} for author_id {} not found.'.format(path, author_id))
            return None

        # Read file
        with open(path, 'r') as file:
            data = file.read()
            return data


