import urllib.request
import etree
import logging
from items import AuthorItem, DocItem

class BeautifulScraper():

    SCRAPED_AUTHORS_PATH = './scraped_data/authors/{}.json'
    SCRAPED_PAGES_PATH = './scraped_data/pages/{}.html'
    SEARCH_PATTERN = 'https://scholar.google.de/citations?hl=de&user={0}&cstart=0&pagesize={1}'
    PAGESIZE = 100

    def __init__(self):
        self.init_log()

    def downloadProfilePage(self, author_id, start=0):
        url = SEARCH_PATTERN.format(author_id, start)
        with urllib.request.urlopen(url) as response:
            html = response.read()
            return html

    def parseAuthorDetails(self, author_id, html):
        logging.info('Parsing main profile for author %s.' % author_id)

        dom = etree.HTML(html)

        # Create object
        author_item = AuthorItem()
        author_item.id = author_id
        author_item.image_url = dom.xpath('//img[@id="gsc_prf_pup-img"]/@src')[0]
        author_item.name = dom.xpath('//div[@id="gsc_prf_in"]/text()')[0]

        # Crawl whole description
        description = dom.xpath('//div[@class="gsc_prf_il"]/text()')[0]
        for string in dom.xpath('//div[@class="gsc_prf_il" and not(@id)]/descendant::*/text()'):
            description += " {}".format(string)
        author_item.description = description

        # Crawl cites and indexes
        tmp_table_data = dom.xpath('//table[@id="gsc_rsb_st"]/tbody/descendant::*[@class="gsc_rsb_std"]/text()')

        author_item.cited = int(tmp_table_data[0])
        author_item.cited_5y = int(tmp_table_data[1])
        author_item.h_index = int(tmp_table_data[2])
        author_item.h_index_5y = int(tmp_table_data[3])
        author_item.i10_index = int(tmp_table_data[4])
        author_item.i10_index_5y = int(tmp_table_data[5])

        # fields of study
        author_item.fields_of_study = dom.xpath('//div[@id="gsc_prf_int"]/descendant::*/text()')
        
        # crawl cites histogram
        years = dom.xpath('//div[@class="gsc_md_hist_b"]/descendant::span[@class="gsc_g_t"]/text()')
        values = dom.xpath('//div[@class="gsc_md_hist_b"]/descendant::a/span[@class="gsc_g_al"]/text()')
        author_item.cite_year_values = zip(years, values)

        return author_item

    def parsePublications(self, html):
        logging.debug('Parse publications.')
        dom = etree.HTML(html)

        publications = []

        # Publication items for the author
        num_pubs = 0
        for doc in dom.xpath('//tr[@class="gsc_a_tr"]'):
            num_pubs += 1
            doc_item = DocItem()
            doc_item.title = dom.xpath('./td[@class="gsc_a_t"]/a/text()')
            doc_item.id = dom.xpath('./td[@class="gsc_a_t"]/a/@href')
            doc_item.authors = dom.xpath('./td[@class="gsc_a_t"]/div/text()[1]')
            doc_item.venue = dom.xpath('./td[@class="gsc_a_t"]/div/text()[2]')
            doc_item.cite_count = dom.xpath('./td[@class="gsc_a_c"]/a/text()')
            doc_item.year = dom.xpath('./td[@class="gsc_a_y"]//text()')
            publications.append(doc_item)
        self.logger.info('Scraped %d documents after item %d.' % (num_pubs, old_start))

        return (num_pubs, publications)

    def scrapePage(self, author_id):
        html = self.downloadProfilePage(author_id)
        author_item = self.parseAuthorDetails(author_id, html)

        author_item.publications = {}

        (pub_count, publications) = parsePublications(html)
        author_item.publications.extend(publications)

        # TODO: Stopped here

        # if(num_pubs == self.pagesize):
        #     newStart = 'cstart={}'.format(old_start + self.pagesize)
        #     newUrl = response.url.replace('cstart={}'.format(old_start), newStart)
        #     self.logger.info('Start another request with newURL')
        #     yield Request(url=newUrl)

    def init_log(self):
        # Use basic logger and set logging level to debug for the assignment
        # Format logging message with timestamp
        logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s: %(message)s')