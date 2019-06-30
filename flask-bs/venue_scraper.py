import urllib.request
from lxml import html, etree
from items.items import VenueItem

SEARCH_PATTERN = 'http://portal.core.edu.au/conf-ranks/?search=&by=all&source=CORE2018&sort=arank&page='
# 1 bis 33 also range(1,34)


def downloadPage(start=0):
    url = SEARCH_PATTERN+'1'
    with urllib.request.urlopen(url) as response:
        with open("asdf.html", "w+") as file:
            html = response.read().decode('utf-8')
            # file.write(html)
            return html


def generateVenueItem():
    venue_item = VenueItem()
    venue_item.id = 0
    venue_item.acronym = ""
    venue_item.rank = ""
    venue_item.venue = ""


def generateVenueList(row, odd_row, venue_list):
    while(venue_list.length() != 0):
        venue = {}
        venue['title'] = even_row.pop(0)
        venue['acronym'] = even_row.pop(0)
        even_row.pop(0)
        venue['rank'] = even_row.pop(0)
        # discard unused info
        even_row.pop(0)
        even_row.pop(0)
        even_row.pop(0)
        even_row.pop(0)
        venue_list.add(venue)
    return venue_list


if __name__ == "__main__":

    html = downloadPage()

    # print(html)

    dom = etree.HTML(html)
    title_even = dom.xpath('//tr[@class="evenrow"]/td/text()')
    title_odd = dom.xpath('//tr[@class="oddrow"]/td/text()')
    rest_even = dom.xpath(
        '//tr[@class="evenrow"]/td[@class="nowrap"]/text()')
    rest_odd = dom.xpath(
        '//tr[@class="oddrow"]/td[@class="nowrap"]/text()')

    even_row = dom.xpath('//tr[@class="evenrow"]/td/text()')
    odd_row = dom.xpath('//tr[@class="evenrow"]/td/text()')

    # test = dom.xpath(
    #     '//tr[@class="evenrow"]/td/text() | //tr[@class="evenrow"]/td[@class="nowrap"]/text()')
    # print(test)

    # remove whitespaces

    i = 0
    for element in even_row:
        even_row[i] = element.lstrip('\n ').rstrip()
        i += 1

    i = 0
    for element in odd_row:
        odd_row[i] = element.lstrip('\n ').rstrip()
        i += 1

    # i = 0
    # for element in title_even:
    #     title_even[i] = element.lstrip('\n ').rstrip()
    #     i += 1

    # i = 0
    # for element in title_odd:
    #     title_odd[i] = element.lstrip('\n ').rstrip()
    #     i += 1

    # i = 0
    # for element in rest_even:
    #     rest_even[i] = element.lstrip('\n ').rstrip()
    #     i += 1

    # print("DESCRIPTION: ", even_row)
    venue_list = []
    generateVenueList(even_row, venue_list)

    pass
