"""API to crawl a webpage data and output how many times a specific word appears on it"""

import re
import requests
from bs4 import BeautifulSoup
from flask import Flask, Blueprint
from flask_restplus import Resource, Api, reqparse


# tornar assincrono apenas o get_response_object enquanto esperar baixar o html, o resto  nao precisa
def get_response_object(url): #unica funcao assincrona da API
    # return requests.get(url)
    response_object = requests.get(url)
    return response_object

def get_html_from_response(response):
    soup = BeautifulSoup(response.content, features='html.parser')
    return soup

def clean_text(soup):
    """Remove script and style elements"""
    for script in soup(["script", "style"]):
        script.extract() 
    text = soup.body.get_text()
    return text

def count_occurrences(text, word):
    """count how many times the provided word appear in the page content"""
    result = re.findall(word, text, re.IGNORECASE)
    return len(result)


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
        html = get_html_from_response(response)
        text = clean_text(html)
        word_count = count_occurrences(text, args.word)

        return {"occurrences" : word_count}, 200

API.add_resource(Crawler, '/api')

if __name__ == '__main__':
    APP.run(debug=True)
    