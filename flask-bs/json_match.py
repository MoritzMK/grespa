import json
import re
from fuzzywuzzy import fuzz


def hasAcronym(title):
    x = re.search("\(([^)]+)\)", title)
    if x != None:
        acronym = title[int(x.span()[0])+1:int(x.span()[1])-1]
        return(acronym)
    else:
        return None


if __name__ == "__main__":
    rank_dict = {}
    with open("venues.json", "r") as venues:
        venue_list = json.load(venues)
        with open("journals.json", "r") as journals:
            journal_list = json.load(journals)
            with open("papers.json", "r") as papers:
                paper_list = json.load(papers)
                for paper in paper_list:
                    acronym = hasAcronym(paper['venue'])
                    if acronym != None:
                        # search for acronym
                        for venue in venue_list:
                            if venue['acronym'] == acronym:
                                print('acronym match')
                                if venue['rank'] in rank_dict:
                                    rank_dict[venue['rank']] += 1
                                else:
                                    rank_dict[venue['rank']] = 1
                    else:
                        # string match title
                        print(
                            "No acronym for ", paper["title"], ". Searching by given venue: ", paper['venue'])
                        match = False
                        # substring = paper['venue']
                        # substring = substring[:-1]
                        # print("Substring: ", substring)
                        for venue in venue_list:
                            if paper['venue'] == venue['title']:
                                if venue['rank'] in rank_dict:
                                    rank_dict[venue['rank']] += 1
                                    match = True
                                else:
                                    rank_dict[venue['rank']] = 1
                                    match = True
                        if match == False:
                            # search in journals
                            print(
                                "No match found for ", paper["title"], "in conferences. Searching in journals")
                            for journal in journal_list:
                                if paper['venue'] in journal['title']:
                                    if journal['rank'] in rank_dict:
                                        rank_dict[journal['rank']] += 1
                                        match = True
                                    else:
                                        rank_dict[journal['rank']] = 1
                                        match = True
                            if match == False:
                                print("No match found")

    print(rank_dict)
    pass
