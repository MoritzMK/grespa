from flask import render_template, jsonify, Blueprint, current_app, make_response

from appointment_comparer.webapp.scrapy_service import ScrapyService

compareauthors = Blueprint('compareauthors', __name__, template_folder='templates')

scrapy_service = ScrapyService()

@compareauthors.route('/compareauthors', methods=['GET'])
def compare_appointment_authors():
    return render_template('pages/compare_appointment.html')

@compareauthors.route('/author/<string:author_id>', methods=['GET'])
def get_author(author_id):
    # 1. Check if crawler is running
    # If not:
    # 2. Check if data is present
    # If not:
    # 3. Start crawling

    # Check if crawler is still running
    current_app.logger.debug('Check if scraping is in progress.')
    if (scrapy_service.scrape_in_progress):
        current_app.logger.debug('Spider still running.')
        return make_response(jsonify(errors='Spider still running'), 911)

    # Check if data is present
    current_app.logger.debug('Check if data is present.')
    data = scrapy_service.get_author_data(author_id)
    current_app.logger.error('data: '.format(data))
    if data:
        current_app.logger.debug('Return data.')
        return jsonify(results=data)
        
    # Start crawler
    current_app.logger.debug('No data for author_id {} found. Crawl data.'.format(author_id))
    scrapy_service.crawl_author(author_id)
    return make_response(jsonify(errors='Spider started'), 910)
