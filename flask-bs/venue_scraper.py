import urllib.request
from lxml import html, etree
from items.items import VenueItem
import json

SEARCH_PATTERN = 'http://portal.core.edu.au/conf-ranks/?search=&by=all&source=CORE2018&sort=arank&page='
# 1 bis 33 also range(1,34)


def downloadPage(number):
    url = SEARCH_PATTERN + f'{number}'
    with urllib.request.urlopen(url) as response:
        html = response.read().decode('utf-8')
        return html


def generateVenueItem():
    venue_item = VenueItem()
    venue_item.id = 0
    venue_item.acronym = ""
    venue_item.rank = ""
    venue_item.venue = ""


def generateVenueList(row, venue_list):
    while(len(row) != 0):
        venue = {}
        venue['title'] = row.pop(0)
        venue['acronym'] = row.pop(0)
        row.pop(0)
        venue['rank'] = row.pop(0)
        # discard unused info
        row.pop(0)
        row.pop(0)
        row.pop(0)
        row.pop(0)
        venue_list.append(venue)
    return venue_list


if __name__ == "__main__":
    venue_list = []
    for i in range(1, 34):
        # html runterladen
        html = downloadPage(i)

        dom = etree.HTML(html)
        even_row = dom.xpath('//tr[@class="evenrow"]/td/text()')
        odd_row = dom.xpath('//tr[@class="evenrow"]/td/text()')
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
        pass
    # liste in json umwandeln
    y = json.dumps(venue_list, indent=4)
    with open("venues.json", "w+") as file:
        file.write(y)

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

    pass
