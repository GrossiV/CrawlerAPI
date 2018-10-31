"""API to crawl a webpage data and output how many times a specific word appears on it"""

import re
import requests
from bs4 import BeautifulSoup
from flask import Flask, Blueprint
from flask_restplus import Resource, Api, reqparse


def url_validator(url):
    if not url.startswith('http'):
        url = 'http://'+ str(url)
    return url

def get_response_object_from_url(url): #unica funcao assincrona da API
    response_object = requests.get(url)
    return response_object

def get_html_from_response(response):
    soup = BeautifulSoup(response.content, features='html.parser')
    return soup

def remove_script_and_styles_from_html(html_data):
    """Remove script and style elements"""
    for script in html_data(["script", "style"]):
        script.extract()
    return html_data

def get_text_from_html(clean_html_data):
    text = clean_html_data.body.get_text()
    return text

def count_occurrences_of_word_in_text(text, word):
    found_words_list = re.findall(word, text, re.IGNORECASE)
    return len(found_words_list)


APP = Flask(__name__)
API = Api(APP, version='1.0', title='Crawler API', description='Count how many times a specific word appears in a webpage')

@API.doc(params={
    'url': 'List of pages to search for a specif word, e.g. "https://google.com"',
    'word': 'Word to be searched in each item of the provided list, e.g "gmail"',
    })

class Crawler(Resource):
    """Class to config the api access methods"""
    def get(self):
        """Get how many times a provided word appears in the page"""
        parser = reqparse.RequestParser()
        parser.add_argument('url', action='append', type=str, required=True)
        parser.add_argument('word', type=str, required=True)
        args = parser.parse_args()
        
        result = dict()
        result['word'] = args.word

        for url in args.url:
            url = url_validator(url)
            
            # prevent crash from wrong urls
            try:
                response = get_response_object_from_url(url)
            except requests.exceptions.ConnectionError:
                result[url] = 'Connection error, check your url and try again'
                continue

            html_data = get_html_from_response(response)
            clean_html_data = remove_script_and_styles_from_html(html_data)
            text = get_text_from_html(clean_html_data)
            number_of_words = count_occurrences_of_word_in_text(text, args.word)
            result[url] = number_of_words
            print(number_of_words)

        return result, 200

    # def post(self, url_list, word):
    #     return {
    #         'url_list': url_list,
    #         'word': word
    #     }

API.add_resource(Crawler, '/api')

#Criar uma classe results_in_cache(Resource): para consultar o cache com um get

if __name__ == '__main__':
    APP.run(debug=True)
    