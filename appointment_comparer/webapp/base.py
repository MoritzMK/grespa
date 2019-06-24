from urllib.parse import urlparse, parse_qs
import requests


from flask import render_template, logging, jsonify, request, Response, Blueprint

base = Blueprint('base', __name__, template_folder='templates')

@base.route('/', methods=['GET'])
def index():
    return render_template('pages/index.html', errors=None,  metrics=None)

@base.route('/browse', methods=['GET'])
def browse():
    return render_template('pages/browse.html', errors=None, metrics=None)

@base.route('/top')
def top():
    errors = []
    result = []
    
    return render_template('pages/top.html',errors=errors, rankings=result)

@base.route('/getRankings/<m>', methods=['GET', 'POST'])
def getRankings(m):
    errors = []
    result = []
    
    return jsonify(results = [dict(row) for row in result], errors =errors)

@base.route('/tempDev')
def temp_home():
    return render_template('pages/temp_dev.html')

@base.route('/getTimeSeries', methods=['GET','POST'])
def getTimeSeries():
    errors = []
    results= []
    return jsonify(results = results, errors =errors)


@base.route('/search', methods=['GET', 'POST'])
def search():
    errors = []
    return render_template('pages/search/entity.html', entity_name='Researcher or Field', action='/search', errors=errors, header='Search')

@base.route('/explore', methods=['GET'])
def explore():
    return render_template('pages/explore.html')