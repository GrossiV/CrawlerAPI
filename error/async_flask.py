"""API to crawl a webpage data and output how many times a specific word appears on it"""

import re
import aiohttp
import asyncio
from bs4 import BeautifulSoup
from flask import Flask
from flask_restplus import Resource, Api, reqparse
from flask_caching import Cache


CACHE = Cache(config={'CACHE_TYPE': 'simple'})
APP = Flask(__name__)
CACHE.init_app(APP)
API = Api(APP, version='1.0', title='Crawler API', description='Count how many times a specific word appears in a webpage')


def url_validator(url):
    if not url.startswith('http'):
        url = 'http://'+ str(url)
    return url

@CACHE.memoize(timeout=300)
async def get_response_object_from_url(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response_object:
            return await response_object

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

@API.doc(params={
    'url': 'Provide a url or more to search for a specif word, e.g. "https://google.com"',
    'word': 'Just only one word to be searched in each url of the provided list, e.g "gmail"',
    })
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

        
        for url in args.url:
            url = url_validator(url)
            loop = asyncio.new_event_loop()   
            
            # prevent api crash from not founded urls
            try:
                response = loop.run_until_complete(get_response_object_from_url(url))
            except aiohttp.client_exceptions.ClientConnectorError:
                result[url] = 'Wrong url address'
                continue
            loop.close()
            
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
    