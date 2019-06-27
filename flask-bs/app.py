from flask import Flask, render_template, jsonify
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
    # 1. Check if crawler is running
    # If not:
    # 2. Check if data is present
    # If not:
    # 3. Start crawling

    # Check if crawler is still running
    app.logger.debug('Check if scraping is in progress.')
    data = scraper.scrapePage(author_id)
    return jsonify(data=AuthorEncoder().encode(data))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)