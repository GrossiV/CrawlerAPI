"""API to crawl a webpage data and output how many times a specific word appears on it"""

import re
import requests
from bs4 import BeautifulSoup
from flask import Flask
from flask_restplus import Resource, Api, reqparse


def get_soup(url):
    """get and parse html data from provided url"""
    result = requests.get(url)
    content = result.content
    soup = BeautifulSoup(content, features='html.parser')
    return soup

def clean_text(soup):
    """Remove script, style and formate the text properly"""
    # kill all script and style elements
    for script in soup(["script", "style"]):
        script.extract()    # rip it out
    #occurrences = soup.body.find_all(text=True)
    text = soup.body.get_text()
    # break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # drop blank lines
    text = '\n'.join(chunk for chunk in chunks if chunk)
    return text

def count_occurrences(text, word):
    """count how many times the provided word appear in the page content"""
    result = re.findall(word, text, re.IGNORECASE)
    return len(result)

APP = Flask(__name__)
API = Api(APP)



class Crawler(Resource):
    """Class to config the api access methods"""
    def get(self):
        """Receives an url and word to return how many times this word appears in the url-page"""
        parser = reqparse.RequestParser()
        parser.add_argument('url', type=str, help='provide an url')
        parser.add_argument('word', type=str, help='provide a word')
        args = parser.parse_args()

        soup = get_soup(args.url)
        text = clean_text(soup)
        word_count = count_occurrences(text, args.word)

        return {"occurrences" : word_count}

API.add_resource(Crawler, '/api')

if __name__ == '__main__':
    APP.run(debug=True)
    