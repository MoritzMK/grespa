import scrapy
import re


class VenueSpider(scrapy.Spider):
    """
    Spider that crawls the venues of given link
    """
    name = "venues"

    def start_requests(self):
        # urls = [
        #     'http://portal.core.edu.au/conf-ranks/?search=&by=all&source=CORE2018&sort=arank&page=1'
        # ]
        # start_url = 'http://portal.core.edu.au/conf-ranks/?search=&by=all&source=CORE2018&sort=arank&page='
        start_url = 'http://portal.core.edu.au/conf-ranks/?search=&by=all&source=all&sort=arank&page='
        for i in range(1, 44):  # prev 34
            yield scrapy.Request(url=start_url+f'{i}', callback=self.parse)

    # start_urls = [
    #     'http://portal.core.edu.au/conf-ranks/?search=&by=all&source=CORE2018&sort=arank&page=1',
    # ]

    def parse(self, response):
        for venue in response.css('tr.evenrow'):
            yield {
                'Title': venue.css('td::text')[0].get().lstrip('\n ').rstrip(),
                'Acronym': venue.css('td.nowrap::text')[0].get().lstrip('\n ').rstrip(),
                'Rank': venue.css('td.nowrap::text')[2].get().lstrip('\n ').rstrip(),
            }
        for venue in response.css('tr.oddrow'):
            yield {
                'Title': venue.css('td::text')[0].get().lstrip('\n ').rstrip(),
                'Acronym': venue.css('td.nowrap::text')[0].get().lstrip('\n ').rstrip(),
                'Rank': venue.css('td.nowrap::text')[2].get().lstrip('\n ').rstrip(),
            }

        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
