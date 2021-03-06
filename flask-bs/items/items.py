class AuthorItem():

    def __init__(self, id=None, fields_of_study=None, name=None, description=None, cited=None, cited_5y=None, h_index=None, h_index_5y=None, i10_index=None, i10_index_5y=None, g_index=None, euclidean=None, cite_year_values=None, image_url=None, publications=None, venue_ranking=None):
        self.id = id
        self.fields_of_study = fields_of_study
        self.name = name
        self.description = description
        self.cited = cited
        self.cited_5y = cited_5y
        self.h_index = h_index
        self.h_index_5y = h_index_5y
        self.i10_index = i10_index
        self.i10_index_5y = i10_index_5y
        self.g_index = g_index
        self.euclidean = euclidean
        self.cite_year_values = cite_year_values
        self.image_url = image_url
        self.publications = publications
        self.venue_ranking = venue_ranking


class DocItem():

    def __init__(self, id=None, title=None, authors=None, venue=None, year=None, cite_count=None):
        self.id = id
        self.title = title
        self.authors = authors
        self.venue = venue
        self.year = year
        self.cite_count = cite_count


class VenueItem():

    def __init__(self, id=None, venue=None, acronym=None, rank=None):
        self.id = None
        self.venue = None
        self.acronym = None
        self.rank = None

class SearchResultItem():
    def __init__(self, id=None, name=None, organization=None, description=None, image_url=None, cited=None):
        self.id = id
        self.name = name
        self.organization = organization
        self.description = description
        self.image_url = image_url
        self.cited = cited
