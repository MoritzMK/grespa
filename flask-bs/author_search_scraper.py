import urllib.request
from lxml import etree
import logging
from items.items import SearchResultItem

class AuthorSearchScraper():

    SEARCH_PATTERN = 'https://scholar.google.de/citations?hl=de&view_op=search_authors&mauthors={0}'
    SCHOLAR_BASE_PATH = 'https://scholar.google.de'
    USER_ID_LENGTH = 12

    def __init__(self):
        self.init_log()

    def DownloadSearchResults(self, search_string):
        search_string = str(search_string).strip().replace(' ', '+')
        url = AuthorSearchScraper.SEARCH_PATTERN.format(search_string)
        logging.info('Scrape url: {}'.format(url))
        with urllib.request.urlopen(url) as response:
            html = response.read()
            return html

    def parseAuthors(self, html):
        logging.debug('Parse authors.')
        dom = etree.HTML(html)

        authors = []

        # Publication items for the author
        num_authors = 0
        items = dom.xpath('//div[@class="gsc_1usr"]/div')
        logging.debug('Found {} tags with class gsc_a_tr.'.format(len(items)))
        for item in items:
            num_authors += 1

            # Create item
            result_item = SearchResultItem()
            result_item.id = str(item.xpath('.//a[@class="gs_ai_pho"]/@href')[0]).replace('/citations?hl=de&user=', '')

            # Get name from img.alt, because the real name is sometimes splitted and highlighted
            result_item.name = item.xpath('.//a[@class="gs_ai_pho"]/span/img/@alt')[0]
            result_item.image_url = AuthorSearchScraper.SCHOLAR_BASE_PATH + item.xpath('.//a[@class="gs_ai_pho"]/span/img/@src')[0]

            # Get org description
            org = item.xpath('.//div[@class="gs_ai_t"]/div[@class="gs_ai_aff"]/text()')
            result_item.organization = org[0] if len(org) > 0 else ''
            desc = item.xpath('.//div[@class="gs_ai_t"]/div[@class="gs_ai_eml"]/text()')
            result_item.description = desc[0] if len(desc) > 0 else ''

            authors.append(result_item)
        logging.info('Scraped {} authors.'.format(num_authors))

        return (num_authors, authors)

    def scrapePage(self, search_string):
        html = self.DownloadSearchResults(search_string)
        (num_authors ,authors) = self.parseAuthors(html)

        return authors

    def init_log(self):
        # Use basic logger and set logging level to debug for the assignment
        # Format logging message with timestamp
        logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s: %(message)s')