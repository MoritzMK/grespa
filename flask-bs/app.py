from flask import Flask, render_template
# from flask_bootstrap import Bootstrap


app = Flask(__name__)
# Bootstrap(app)

@app.route('/')
def index():
    return render_template('index.html')

@compareauthors.route('/author/<string:author_id>', methods=['GET'])
def get_author(author_id):
    # 1. Check if crawler is running
    # If not:
    # 2. Check if data is present
    # If not:
    # 3. Start crawling

    # Check if crawler is still running
    app.logger.debug('Check if scraping is in progress.')
    if (scrapy_service.scrape_in_progress):
        app.logger.debug('Spider still running.')
        return make_response(jsonify(errors='Spider still running'), 911)

    # Check if data is present
    app.logger.debug('Check if data is present.')
    data = scrapy_service.get_author_data(author_id)
    app.logger.error('data: '.format(data))
    if data:
        app.logger.debug('Return data.')
        return jsonify(results=data)
        
    # Start crawler
    app.logger.debug('No data for author_id {} found. Crawl data.'.format(author_id))
    scrapy_service.crawl_author(author_id)
    return make_response(jsonify(errors='Spider started'), 910)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)