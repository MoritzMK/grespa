class AuthorItem():

    def __init__(self, id, fields_of_study, name, description, cited, cited_5y, h_index, h_index_5y, i10_index, i10_index_5y, cite_year_values, image_url, publications):
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
        self.cite_year_values = cite_year_values
        self.image_url = image_url
        self.publications = publications

class DocItem():

    def __init__ (self, id, title, authors, venue, year, cite_count):
        self.id = id
        self.title = title
        self.authors = authors
        self.venue = venue
        self.year = year
        self.cite_count = cite_count