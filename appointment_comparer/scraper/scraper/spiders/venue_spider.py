import scrapy
import re


class VenueSpider(scrapy.Spider):
    name = "venues"

    def start_requests(self):
        # urls = [
        #     'http://portal.core.edu.au/conf-ranks/?search=&by=all&source=CORE2018&sort=arank&page=1'
        # ]
        start_url = 'http://portal.core.edu.au/conf-ranks/?search=&by=all&source=CORE2018&sort=arank&page='
        for i in range(1, 34):
            yield scrapy.Request(url=start_url+f'{i}', callback=self.parse)

    # start_urls = [
    #     'http://portal.core.edu.au/conf-ranks/?search=&by=all&source=CORE2018&sort=arank&page=1',
    # ]

    def parse(self, response):
        for venue in response.css('tr.evenrow'):
            yield {
                'Title': venue.css('td::text')[0].get().lstrip('\n ').rstrip(),
                'Acronym': venue.css('td.nowrap::text')[0].get().lstrip('\n ').rstrip(),
                # 'Source': venue.css('td.nowrap::text')[1].get().lstrip('\n ').rstrip(),
                'Rank': venue.css('td.nowrap::text')[2].get().lstrip('\n ').rstrip(),
                # 'HasData': venue.css('td.nowrap::text')[3].get().lstrip('\n ').rstrip(),
                # 'Comments': venue.css('td.nowrap::text')[4].get().lstrip('\n ').rstrip(),
                # 'AvgRating': venue.css('td.nowrap::text')[5].get().lstrip('\n ').rstrip(),
            }
        for venue in response.css('tr.oddrow'):
            yield {
                'Title': venue.css('td::text')[0].get().lstrip('\n ').rstrip(),
                'Acronym': venue.css('td.nowrap::text')[0].get().lstrip('\n ').rstrip(),
                # 'Source': venue.css('td.nowrap::text')[1].get().lstrip('\n ').rstrip(),
                'Rank': venue.css('td.nowrap::text')[2].get().lstrip('\n ').rstrip(),
                # 'HasData': venue.css('td.nowrap::text')[3].get().lstrip('\n ').rstrip(),
                # 'Comments': venue.css('td.nowrap::text')[4].get().lstrip('\n ').rstrip(),
                # 'AvgRating': venue.css('td.nowrap::text')[5].get().lstrip('\n ').rstrip(),
            }

        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
