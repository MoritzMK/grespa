from urllib.parse import urlparse, parse_qs

from scrapy import Spider
from scrapy.exceptions import NotSupported
from scrapy.http import Request
from scrapy.loader import ItemLoader

from ..items import AuthorItem, DocItem


class AuthorDetails(Spider):
    """ Spider that crawls the profile page of a single author for all details.
        Pass the author's id with the parameter author_id.
    """

    name = "author_details"
    pagesize = 100
    search_pattern = 'https://scholar.google.de/citations?hl=de&user={0}&cstart=0&pagesize={1}'

    def __init__(self, author_id=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.author_id = author_id
        self.start_urls = [self.search_pattern.format(self.author_id, self.pagesize)]

    def parse_profile(self, response, author_id):
        self.logger.info('Parsing main profile for author %s.' % author_id)

        # create item
        authorItem = AuthorItem()
        authorItem['id'] = author_id

        # build detailed author item
        item = ItemLoader(item=authorItem, response=response)
        
        # Save image path
        item.add_xpath('image_url', '//img[@id="gsc_prf_pup-img"]/@src')
        
        # Crawl name
        item.add_xpath('name', '//div[@id="gsc_prf_in"]/text()')

        # Crawl whole description
        description = response.xpath('//div[@class="gsc_prf_il"]/text()').extract_first()
        for string in response.xpath('//div[@class="gsc_prf_il" and not(@id)]/descendant::*/text()').extract():
            description += " {}".format(string)
        item.add_value('description', description)

        # Crawl cites and indexes
        tmp_table_data = response.xpath('//table[@id="gsc_rsb_st"]/tbody/descendant::*[@class="gsc_rsb_std"]/text()').extract()

        item.add_value('cited', int(tmp_table_data[0]))
        item.add_value('cited_5y', int(tmp_table_data[1]))
        item.add_value('h_index', int(tmp_table_data[2]))
        item.add_value('h_index_5y', int(tmp_table_data[3]))
        item.add_value('i10_index', int(tmp_table_data[4]))
        item.add_value('i10_index_5y', int(tmp_table_data[5]))

        # fields of study
        item.add_xpath('fields_of_study', '//div[@id="gsc_prf_int"]/descendant::*/text()')
        
        # crawl cites histogram
        years = response.xpath('//div[@class="gsc_md_hist_b"]/descendant::span[@class="gsc_g_t"]/text()').extract()
        values = response.xpath('//div[@class="gsc_md_hist_b"]/descendant::a/span[@class="gsc_g_al"]/text()').extract()
        item.add_value('cite_year_values', zip(years, values))

        return item.load_item()

    def parse_docs(self, response, old_start):
        # crawl the author's documents
        doc_item = DocItem()

        # Publication items for the author
        num_pubs = 0
        for doc in response.xpath('//tr[@class="gsc_a_tr"]'):
            num_pubs += 1
            il = ItemLoader(item=doc_item, selector=doc, response=response)
            il.add_xpath('title', './td[@class="gsc_a_t"]/a/text()')
            il.add_xpath('id', './td[@class="gsc_a_t"]/a/@href')
            il.add_xpath('authors', './td[@class="gsc_a_t"]/div/text()[1]')
            il.add_xpath('published_in', './td[@class="gsc_a_t"]/div/text()[2]')
            il.add_xpath('cite_count', './td[@class="gsc_a_c"]/a/text()')
            il.add_xpath('year', './td[@class="gsc_a_y"]//text()')
            yield il.load_item()
        self.logger.info('Scraped %d documents after item %d.' % (num_pubs, old_start))

        if(num_pubs == self.pagesize):
            newStart = 'cstart={}'.format(old_start + self.pagesize)
            newUrl = response.url.replace('cstart={}'.format(old_start), newStart)
            self.logger.info('Start another request with newURL')
            yield Request(url=newUrl)

    def url_params(self, url):
        return

    def parse(self, response):

        # Check if we are on the right page
        parse_res = urlparse(response.url)
        if parse_res.path != '/citations':
            # we only want author details, so the path has to be right
            raise NotSupported

        # Get all parameter from the url
        params = parse_qs(parse_res.query)
        author_id = params['user'][0]
        c_start = params.get('cstart', [None])[0]
        old_start = int(c_start) if c_start else None

        # If old_start is 0, this is the first visit, so scrap the details
        if(old_start == 0):
            yield self.parse_profile(response, author_id)
        
        for doc in self.parse_docs(response, old_start):
           yield doc

    