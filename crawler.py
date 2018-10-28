import requests
from bs4 import BeautifulSoup
import re


#def count_matches(string):
## implementar match

#def get_text_from_tag(tag):
    # x = 0
    # for tag in soup.body.find_all(tag, text=True):
    #     # print(tag.text)
    #     # count_matches(tag.text)
    #     print(tag.text)
    #     x = re.match('Astra', tag.text, re.IGNORECASE)        
    # ## fazer retornar numero de matches
    # return x


result = requests.get("https://www.pontotel.com.br/")
content = result.content
soup = BeautifulSoup(content, features='html.parser')


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

#print(text)

result =  re.findall('Astra', text, re.IGNORECASE)
print(result)
print(len(result))

#tags_to_search = ['p', 'a', 'span', 'li', 'td', 'th', 'h1', 'h2' ,'h3', 'h4', 'h5', 'h6']
#tags_to_search = ['div']
#matches_number = list(map(lambda tag : get_text_from_tag(tag), tags_to_search)) 
## ajustar o map para passar dois parametros
#print(matches_number)
