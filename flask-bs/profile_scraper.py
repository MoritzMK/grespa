import urllib.request
from lxml import etree
import logging
from items.items import AuthorItem, DocItem
from scholarmetrics import hindex, gindex, euclidean
from ranking_matcher import RankingMatcher

class ProfileScraper():

    SCRAPED_AUTHORS_PATH = './scraped_data/authors/{}.json'
    SCRAPED_PAGES_PATH = './scraped_data/pages/{}.html'
    SEARCH_PATTERN = 'https://scholar.google.de/citations?hl=de&user={0}&cstart={1}&pagesize={2}'
    SCHOLAR_BASE_PATH = 'https://scholar.google.de'
    PAGESIZE = 100

    def __init__(self):
        self.init_log()
        self.ranking_matcher = RankingMatcher()

    def downloadProfilePage(self, author_id, start=0):
        url = ProfileScraper.SEARCH_PATTERN.format(author_id, start, ProfileScraper.PAGESIZE)
        logging.info('Scrape url: {}'.format(url))
        with urllib.request.urlopen(url) as response:
            html = response.read()
            return html

    def parseAuthorDetails(self, author_id, html, year):
        logging.info('Parsing main profile for author %s.' % author_id)

        dom = etree.HTML(html)

        # Create object
        author_item = AuthorItem()
        author_item.id = author_id
        author_item.image_url = ProfileScraper.SCHOLAR_BASE_PATH + dom.xpath('//img[@id="gsc_prf_pup-img"]/@src')[0]
        author_item.name = dom.xpath('//div[@id="gsc_prf_in"]/text()')[0]

        # Crawl whole description
        description = dom.xpath('//div[@class="gsc_prf_il"]/text()')[0]
        for string in dom.xpath('//div[@class="gsc_prf_il" and not(@id)]/descendant::*/text()'):
            description += " {}".format(string)
        author_item.description = description

        # Crawl cites and indexes
        tmp_table_data = dom.xpath('//table[@id="gsc_rsb_st"]/tbody/descendant::*[@class="gsc_rsb_std"]/text()')



        # fields of study
        author_item.fields_of_study = dom.xpath('//div[@id="gsc_prf_int"]/descendant::*/text()')
        
        # crawl cites histogram
        years = dom.xpath('//div[@class="gsc_md_hist_b"]/descendant::span[@class="gsc_g_t"]/text()')
        values = dom.xpath('//div[@class="gsc_md_hist_b"]/descendant::a/span[@class="gsc_g_al"]/text()')
        tmp_cy = list(zip(years, values))
        author_item.cite_year_values = list(filter(lambda x: x[0] >= year, tmp_cy))

        #logging.debug(author_item.cite_year_values)

        # author_item.cited = int(tmp_table_data[0])
        tmp_cited = 0
        for cy in author_item.cite_year_values:
            tmp_cited += int(cy[1])
        author_item.cited = tmp_cited
        author_item.cited_5y = int(tmp_table_data[1])
        # author_item.h_index = int(tmp_table_data[2])
        author_item.h_index_5y = int(tmp_table_data[3])
        author_item.i10_index = int(tmp_table_data[4])
        author_item.i10_index_5y = int(tmp_table_data[5])


        return author_item

    def parsePublications(self, html):
        logging.debug('Parse publications.')
        dom = etree.HTML(html)

        publications = []

        # Publication items for the author
        num_pubs = 0
        docs = dom.xpath('//tr[@class="gsc_a_tr"]')
        logging.debug('Found {} tags with class gsc_a_tr.'.format(len(docs)))
        for doc in docs:
            num_pubs += 1
            doc_item = DocItem()
            doc_item.title = doc.xpath('.//td[@class="gsc_a_t"]/a/text()')[0]
            doc_item.id = doc.xpath('.//td[@class="gsc_a_t"]/a/@href')[0]
            doc_item.authors = doc.xpath('.//td[@class="gsc_a_t"]/div[1]/text()')[0]
            venue = doc.xpath('.//td[@class="gsc_a_t"]/div[2]/text()')
            doc_item.venue = venue[0] if len(venue) > 0 else ''
            cite_count = doc.xpath('.//td[@class="gsc_a_c"]/a/text()')
            doc_item.cite_count = cite_count[0] if len(cite_count) > 0 else 0
            year = doc.xpath('.//td[@class="gsc_a_y"]//text()')
            doc_item.year = year[0] if len(year) > 0 else 0
            publications.append(doc_item)
        logging.info('Scraped {} publications.'.format(num_pubs))

        return (num_pubs, publications)

    def calculateIndices(self, author_item):
        cited = list(int(pub.cite_count) for pub in author_item.publications)
        #logging.debug(cited)
        author_item.h_index = int(hindex(cited))
        author_item.g_index = int(gindex(cited))
        author_item.euclidean = round(float(euclidean(cited)), 2)

        return author_item

    def getVenueRankings(self, author_item):
        venues = list(pub.venue for pub in author_item.publications)
        logging.debug(venues)
        rankings = self.ranking_matcher.matchAllString(venues)
        author_item.venue_ranking = rankings
        logging.debug(author_item.venue_ranking)
        return author_item

    def scrapePage(self, author_id, year):
        html = self.downloadProfilePage(author_id)
        author_item = self.parseAuthorDetails(author_id, html, year)

        author_item.publications = []
        pub_count = ProfileScraper.PAGESIZE
        start = 0
        while pub_count == ProfileScraper.PAGESIZE:
            if start > 0:
                logging.debug('Start another request with newURL')
                html = self.downloadProfilePage(author_id, start)

            (pub_count, publications) = self.parsePublications(html)
            author_item.publications.extend(publications)
            start = start + ProfileScraper.PAGESIZE

        author_item = self.calculateIndices(author_item)
        author_item = self.getVenueRankings(author_item)

        return author_item

    def init_log(self):
        # Use basic logger and set logging level to debug for the assignment
        # Format logging message with timestamp
        logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s: %(message)s')