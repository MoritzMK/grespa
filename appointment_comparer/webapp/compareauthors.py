from flask import render_template, jsonify, Blueprint, current_app

from appointment_comparer.webapp.scrapy_launcher import ScrapyLauncher

# Instantiate scrapy launcher

compareauthors = Blueprint('compareauthors', __name__, template_folder='templates')

scrapy_launcher = ScrapyLauncher()


@compareauthors.route('/compareauthors', methods=['GET'])
def compare_appointment_authors():
    return render_template('pages/compare_appointment.html')

@compareauthors.route('/author/<string:author_id>', methods=['GET'])
def get_author(author_id):

    data = scrapy_launcher.get_author_data(author_id)
    current_app.logger.error('data: '.format(data))
    if not data:
        current_app.logger.debug('No data for author_id {} found. Crawl data.'.format(author_id))
        scrapy_launcher.crawl_author(author_id)
        data = scrapy_launcher.get_author_data(author_id)

    return jsonify(results=data)