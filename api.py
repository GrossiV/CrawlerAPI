"""API to crawl a webpage data and output how many times a specific word appears on it"""

import re
import requests
from bs4 import BeautifulSoup
from flask import Flask, Blueprint
from flask_restplus import Resource, Api, reqparse


def get_response_object(url): #unica funcao assincrona da API
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
        parser.add_argument('url', type=str, required=True)
        parser.add_argument('word', type=str, required=True)
        args = parser.parse_args()

        response = get_response_object(args.url)
        html_data = get_html_from_response(response)
        clean_html_data = remove_script_and_styles_from_html(html_data)
        text = get_text_from_html(clean_html_data)
        number_of_words = count_occurrences_of_word_in_text(text, args.word)

        return {"occurrences" : number_of_words}, 200

API.add_resource(Crawler, '/api')

if __name__ == '__main__':
    APP.run(debug=True)
    