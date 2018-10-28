import requests
from bs4 import BeautifulSoup
import re


#def count_matches(string):
## implementar match

def get_text_from_tag(tag):
    x = 0
    for tag in soup.body.find_all(tag):
        # print(tag.text)
        # count_matches(tag.text)
        print(tag.text)
        x = re.match('Astra', tag.text, re.IGNORECASE)        
    ## fazer retornar numero de matches
    return x

result = requests.get("https://www.pontotel.com.br/")
content = result.content
soup = BeautifulSoup(content, features='html.parser')

tags_to_search = ['p', 'a', 'span', 'li', 'td', 'th', 'h1', 'h2' ,'h3', 'h4', 'h5', 'h6']
matches_number = list(map(lambda tag : get_text_from_tag(tag), tags_to_search)) 
## ajustar o map para passar dois parametros
print(matches_number)