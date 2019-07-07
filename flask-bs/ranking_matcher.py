import json
import re
from fuzzywuzzy import fuzz


class RankingMatcher():

    def __init__(self, *args, **kwargs):
        self.rank_dict = {"A*": 0, "A": 0, "B": 0, "C": 0, "other": 0}
        self.fuzzy = 0

    def clearDict(self):
        self.rank_dict = {"A*": 0, "A": 0, "B": 0, "C": 0, "other": 0}

    def addRank(self, rank):
        if rank in self.rank_dict:
            self.rank_dict[rank] += 1
        else:
            self.rank_dict['other'] = 1

    def hasAcronym(self, title):
        x = re.search("\(([^)]+)\)", title)
        if x != None:
            acronym = title[int(x.span()[0])+1:int(x.span()[1])-1]
            print("acronym:", acronym)
            return(acronym)
        else:
            return None

    def searchAcronym(self, acronym):
        with open("venues.json", "r") as venues:
            venue_list = json.load(venues)
            for venue in venue_list:
                if venue['acronym'] == acronym:
                    self.addRank(venue['rank'])
                    return venue['rank']

    def searchVenuesFuzzy(self, title):
        with open("venues.json", "r") as venues:
            venue_list = json.load(venues)
            highest_match = None
            for venue in venue_list:
                if fuzz.ratio(venue['title'], title) > 65:
                    highest_match = venue
                if not highest_match == None:
                    print(highest_match)
                    self.addRank(highest_match['rank'])
                    return highest_match['rank']

    def searchJournalsFuzzy(self, title):
        with open("journals.json", "r") as journals:
            journal_list = json.load(journals)
            highest_match = None
            for journal in journal_list:
                if fuzz.ratio(journal['title'], title) > 65:
                    highest_match = journal
                if not highest_match == None:
                    print(highest_match)
                    self.addRank(highest_match['rank'])
                    return highest_match['rank']

    def searchVenues(self, title):
        with open("venues.json", "r") as venues:
            venue_list = json.load(venues)
            for venue in venue_list:
                if title == venue['title']:
                    self.addRank(venue['rank'])
                    return venue['rank']

    def searchJournals(self, title):
        with open("journals.json", "r") as journals:
            journal_list = json.load(journals)
            for journal in journal_list:
                if title == journal['title']:
                    self.addRank(journal['rank'])
                    return journal['rank']

# returns rank dict given title of venue
    def matchOne(self, title):
        match = None
        acronym = self.hasAcronym(title)
        if acronym != None:
            match = self.searchAcronym(acronym)
            if not match == None:
                print("match acro")
        else:
            if "journal" in title:
                match = self.searchJournals(title)
                if not match == None:
                    print("match journal")
            else:
                match = self.searchVenues(title)
                if not match == None:
                    print("match venue")
        # if no match => fuzzy match
        if match == None:
            print("no match => fuzzy")
            match = self.searchVenuesFuzzy(title)
            if not match == None:
                print("match fuzzy venue")
            else:
                # match journal fuzzy vllt
                match = self.searchJournalsFuzzy(title)
                if not match == None:
                    print("match fuzzy journal")
                else:
                    print("no match for real")

        if not match == None:
            return match

# loads titles via json
    def matchAllJson(self):
        with open("papers.json", "r") as papers:
            paper_list = json.load(papers)
            i = 1
            for paper in paper_list:
                print(i, paper["title"])
                self.matchOne(paper["venue"])
                i += 1
        print(self.rank_dict)

# loads titles via string array
    def matchAllString(self, title_list):
        i = 1
        for paper in title_list:
            print(i, paper)
            self.matchOne(paper)
            i += 1
        print(self.rank_dict)
        rank_dict = self.rank_dict
        self.clearDict()
        return rank_dict


if __name__ == "__main__":
    matcher = RankingMatcher()
    # print(matcher.matchOne("Proc. ACM Symposium on Document Engineering(DocEng)"))
    matcher.matchAllJson()
    pass
