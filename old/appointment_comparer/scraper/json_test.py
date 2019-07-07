import json
import re


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
        with open("papers.json", "r") as papers:
            paper_list = json.load(papers)

            # for key in first_venue:
            #     print(key)
            # for val in first_venue:
            #     print(first_venue[val])

            for paper in paper_list:
                acronym = hasAcronym(paper['Venue'])
                if acronym != None:
                    # search for acronym
                    for venue in venue_list:
                        if venue['Acronym'] == acronym:
                            if venue['Rank'] in rank_dict:
                                rank_dict[venue['Rank']] += 1
                            else:
                                rank_dict[venue['Rank']] = 1
                else:
                    # string match title and pray
                    print("No acronym for ", paper["Title"], ". Searching by given venue: ", paper['Venue'])
                    match = False
                    for venue in venue_list:
                        if venue['Title'] == paper['Venue']:
                            if venue['Rank'] in rank_dict:
                                rank_dict[venue['Rank']] += 1
                                match = True
                            else:
                                rank_dict[venue['Rank']] = 1
                                match = True
                    if match==False:
                        print("No match found for ", paper["Title"],".")
    print(rank_dict)
    pass
