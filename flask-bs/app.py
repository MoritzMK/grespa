from flask import Flask, render_template, jsonify, request
from items.encoder import AuthorEncoder
# from flask_bootstrap import Bootstrap

from profile_scraper import ProfileScraper
from author_search_scraper import AuthorSearchScraper


app = Flask(__name__)
# Bootstrap(app)

profileScraper = ProfileScraper()
authorSearchScraper = AuthorSearchScraper()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/author/<string:author_id>', methods=['GET'])
def get_author(author_id):
    year = request.args.get('year')
    data = profileScraper.scrapePage(author_id, year)
    return jsonify(data=AuthorEncoder().encode(data))

@app.route('/author/search/<string:search_string>', methods=['GET'])
def search_author(search_string):
    data = authorSearchScraper.scrapePage(search_string)
    data = list(item.__dict__ for item in data)
    return jsonify(data=data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)