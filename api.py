"""API to crawl a webpage data and output how many times a specific word appears on it"""

import re
import requests
from bs4 import BeautifulSoup
from flask import Flask, Blueprint
from flask_restplus import Resource, Api, reqparse, fields
from flask_caching import Cache


CACHE = Cache(config={'CACHE_TYPE': 'simple'})
APP = Flask(__name__)
CACHE.init_app(APP)
API = Api(APP, version='1.0', title='Crawler API', description='Count how many times a specific word appears in a webpage')
URLS = fields.String(description='List of urls to look')


word_and_urls = API.model(
    'data', {'word': fields.String('Word to be searched'),
    'urls': fields.List(URLS)
    })

def get_word_occurrences_by_url(url_list, result):
    """Funtion to orchestrate the API execution, as I have post and get methods doing the same thing,
        with this function we can assure that no code will be repeated"""
    for url in url_list:
            url = url_validator(url)
            # prevent api crash from wrong urls
            try:
                response = get_response_object_from_url(url)
            except requests.exceptions.ConnectionError:
                result[url] = 'Wrong url address'
                continue
            html_data = get_html_from_response(response)
            clean_html_data = remove_script_and_styles_from_html(html_data)
            text = get_text_from_html(clean_html_data)
            number_of_words = count_occurrences_of_word_in_text(text, result['word'])
            result[url] = number_of_words
    return result
        
def url_validator(url):
    if not url.startswith('http'):
        url = 'http://'+ str(url)
    return url

@CACHE.memoize(timeout=300)
def get_response_object_from_url(url):
    response_object = requests.get(url)
    return response_object

def get_html_from_response(response):
    soup = BeautifulSoup(response.content, features='html.parser')
    return soup

def remove_script_and_styles_from_html(html_data):
    for script in html_data(["script", "style"]):
        script.extract()
    return html_data

def get_text_from_html(clean_html_data):
    text = clean_html_data.body.get_text()
    return text

def count_occurrences_of_word_in_text(text, word):
    found_words_list = re.findall(word, text, re.IGNORECASE)
    return len(found_words_list)


# @API.doc(params={
#     'url': 'List of pages to search for a specif word, e.g. "https://google.com"',
#     'word': 'Word to be searched in each item of the provided list, e.g "gmail"',
#     })
@API.route('/api')
class Crawler(Resource):
    """Class to config the api access methods"""
    def get(self):
        """Count how many times a specific word appears in a webpage"""
        parser = reqparse.RequestParser()
        parser.add_argument('url', action='append', type=str, required=True)
        parser.add_argument('word', type=str, required=True)
        args = parser.parse_args()
        result = dict()
        result['word'] = args.word
        result = get_word_occurrences_by_url(args.url, result)
        return result, 200

    @API.expect(word_and_urls)
    def post(self):
        # Postman headers
        # Accept : application/json
        # Content-Type : application/json
        result = dict()
        result['word'] = API.payload['word'] 
        url_list = API.payload['urls']
        result = get_word_occurrences_by_url(url_list, result)
        return result, 200

if __name__ == '__main__':
    APP.run(debug=True)
    