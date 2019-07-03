import json
import re
from fuzzywuzzy import fuzz


class RankingMatcher():

    def hasAcronym(self, title):
        x = re.search("\(([^)]+)\)", title)
        if x != None:
            acronym = title[int(x.span()[0])+1:int(x.span()[1])-1]
            return(acronym)
        else:
            return None

    def fuzzymatch(self, a, b):
        print(fuzz.ratio(a, b))

    def searchVenues(self,):
        with open("venues.json", "r") as venues:
            venue_list = json.load(venues)
            for venue in venue_list:
                if title == venue['title']:
                    if venue['rank'] in rank_dict:
                        rank_dict[venue['rank']] += 1
                        match = True
                    else:
                        rank_dict["other"] += 1
        pass

    def searchJournals(self,):
        with open("journals.json", "r") as journals:
            journal_list = json.load(journals)
            for journal in journal_list:
                if title == journal['title']:
                    if journal['rank'] in rank_dict:
                        rank_dict[journal['rank']] += 1
                        match = True
                    else:
                        rank_dict["other"] += 1
        pass

    def matchOne(self, title):
        rank_dict = {"A*": 0, "A": 0, "B": 0, "C": 0, "other": 0}

        match = False
        if "journal" in title:
            searchJournals()
        else:

        print(rank_dict)
        return rank_dict

    def matchAll(self, ):
        rank_dict = {"A*": 0, "A": 0, "B": 0, "C": 0, "other": 0}
        with open("venues.json", "r") as venues:
            venue_list = json.load(venues)
            with open("journals.json", "r") as journals:
                journal_list = json.load(journals)
                with open("papers.json", "r") as papers:
                    paper_list = json.load(papers)
                    for paper in paper_list:
                        acronym = self.hasAcronym(paper['venue'])
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


if __name__ == "__main__":
    matcher = RankingMatcher()
    matcher.matchAll()
    # matcher.fuzzymatch(
    #     "Proc. Int. ACM SIGIR Conference on Research and Development in Information",
    #     "ACM International Conference on Research and Development in Information Retrieval")
    pass
