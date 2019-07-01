# from json import JSONEncoder
from .items import AuthorItem

class AuthorEncoder():
    def encode(self, item: AuthorItem):
        # If there are any publications, we have to serialize them manually
        if (item.publications):
            # Save the pubs and set the Property to an empty list
            publications = item.publications
            item.publications = []
            # Iterate through all pubs and serialize them to a dict
            for pub in publications:
                # if the doc has a venueItem, serialize this too
                # Uncomment if VenueItems will be introduced
                # if (pub.venue):
                #     pub.venue = pub.venue.__dict__
                # Append the pub to the list
                item.publications.append(pub.__dict__)

        # If there are, and there will be some, citeYearValues, serialize them
        if(item.cite_year_values):
            item.cite_year_values = dict(item.cite_year_values)

        # At the end, serialize the authorItem itself and return it
        return item.__dict__