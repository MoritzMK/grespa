from flask import Flask, render_template, jsonify, request
from items.encoder import AuthorEncoder
# from flask_bootstrap import Bootstrap

from scraper import BeautifulScraper


app = Flask(__name__)
# Bootstrap(app)

scraper = BeautifulScraper()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/author/<string:author_id>', methods=['GET'])
def get_author(author_id):
    year = request.args.get('year')
    data = scraper.scrapePage(author_id, year)
    return jsonify(data=AuthorEncoder().encode(data))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)