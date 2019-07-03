import urllib.request
from lxml import html, etree
from items.items import VenueItem
import json
from pathlib import Path


class VenueScraper():

    SEARCH_PATTERN_VENUE = 'http://portal.core.edu.au/conf-ranks/?search=&by=all&source=all&sort=atitle&page='
    # 1 bis 33 also range(1,44)
    SEARCH_PATTERN_JOURNAL = 'http://portal.core.edu.au/jnl-ranks/?search=&by=all&source=ERA2010%0D%0A&sort=atitle&page='

    def downloadPageVenue(self, number):
        url = SEARCH_PATTERN_VENUE + f'{number}'
        with urllib.request.urlopen(url) as response:
            html = response.read().decode('utf-8')
            return html

    def downloadPageJournal(self, number):
        url = SEARCH_PATTERN_JOURNAL + f'{number}'
        with urllib.request.urlopen(url) as response:
            html = response.read().decode('utf-8')
            return html

    # def generateVenueItem():
        # venue_item = VenueItem()
        # venue_item.id = 0
        # venue_item.acronym = ""
        # venue_item.rank = ""
        # venue_item.venue = ""

    def generateVenueList(self, row, venue_list):
        while(len(row) != 0):
            venue = {}
            venue['title'] = row.pop(0)
            venue['acronym'] = row.pop(0)
            venue['source'] = row.pop(0)
            venue['rank'] = row.pop(0)
            # discard unused info
            row.pop(0)
            row.pop(0)
            row.pop(0)
            row.pop(0)
            venue_list.append(venue)
        return venue_list

    def generateJournalList(self, row, journal_list):
        while(len(row) != 0):
            journal = {}
            journal['title'] = row.pop(0)
            row.pop(0)
            journal['rank'] = row.pop(0)
            # discard unused info
            row.pop(0)
            row.pop(0)
            row.pop(0)
            row.pop(0)
            journal_list.append(journal)
        return journal_list

    def fileExists(self, file):
        my_file = Path("./"+file)
        if my_file.exists():
            return True
        else:
            return False

    def writeJson(self, my_list, target):
        y = json.dumps(my_list, indent=4)
        with open(target, "w+") as file:
            file.write(y)

    def scrapeVenues(self):  # eigentlich conferences
        print("Scraping Venues")
        # nur falls file nicht vorhanden
        if self.fileExists("venues.json") == False:
            try:
                venue_list = []
                for i in range(1, 44):
                    # html runterladen
                    html = downloadPageVenue(i)

                    dom = etree.HTML(html)
                    even_row = dom.xpath('//tr[@class="evenrow"]/td/text()')
                    odd_row = dom.xpath('//tr[@class="oddrow"]/td/text()')
                    j = 0
                    for element in even_row:
                        even_row[j] = element.lstrip('\n ').rstrip()
                        j += 1

                    j = 0
                    for element in odd_row:
                        odd_row[j] = element.lstrip('\n ').rstrip()
                        j += 1

                    # liste erweitern
                    generateVenueList(even_row, venue_list)
                    generateVenueList(odd_row, venue_list)

                # liste in json umwandeln
                writeJson(venue_list, "venues.json")
            except urllib.error.HTTPError as error:
                print("Error while scraping: ", error)
        print("Done")

    def scrapeJournals(self):
        print("Scraping Journals")
        if self.fileExists("journals.json") == False:
            try:
                journal_list = []
                for i in range(1, 19):
                    # html runterladen
                    html = downloadPageJournal(i)

                    dom = etree.HTML(html)
                    even_row = dom.xpath('//tr[@class="evenrow"]/td/text()')
                    odd_row = dom.xpath('//tr[@class="oddrow"]/td/text()')
                    j = 0
                    for element in even_row:
                        even_row[j] = element.lstrip('\n ').rstrip()
                        j += 1

                    j = 0
                    for element in odd_row:
                        odd_row[j] = element.lstrip('\n ').rstrip()
                        j += 1

                    # liste erweitern
                    generateJournalList(even_row, journal_list)
                    generateJournalList(odd_row, journal_list)

                # liste in json umwandeln
                writeJson(journal_list, "journals.json")
            except urllib.error.HTTPError as error:
                print("Error while scraping: ", error)
        print("Done")

        # title_even = dom.xpath('//tr[@class="evenrow"]/td/text()')
        # title_odd = dom.xpath('//tr[@class="oddrow"]/td/text()')
        # rest_even = dom.xpath(
        #     '//tr[@class="evenrow"]/td[@class="nowrap"]/text()')
        # rest_odd = dom.xpath(
        #     '//tr[@class="oddrow"]/td[@class="nowrap"]/text()')
        # even_row = dom.xpath('//tr[@class="evenrow"]/td/text()')
        # odd_row = dom.xpath('//tr[@class="evenrow"]/td/text()')

        # j = 0
        # for element in even_row:
        #     even_row[j] = element.lstrip('\n ').rstrip()
        #     j += 1


        # j = 0
        # for element in odd_row:
        #     odd_row[j] = element.lstrip('\n ').rstrip()
        #     j += 1
if __name__ == "__main__":
    scraper = VenueScraper()
    scraper.scrapeVenues()
    scraper.scrapeJournals()
    pass
