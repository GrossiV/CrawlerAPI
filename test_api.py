import pytest
from api import url_validator, get_response_object_from_url, get_html_from_response


@pytest.mark.parametrize("test_input, expected", [
    ("https://www.google.com", "https://www.google.com"),
    ("www.google.com", "http://www.google.com"),
])
def test_url_validator(test_input, expected):
    assert url_validator(test_input) == expected 

@pytest.fixture
def mock_get_requests(scope="module"):
    import requests
    response = requests.get('https://google.com')
    return response

def test_get_response_object_from_url(mock_get_requests):
    assert get_response_object_from_url('https://google.com').status_code == mock_get_requests.status_code

@pytest.fixture
def mock_get_soup(scope="module"):
    import requests
    from bs4 import BeautifulSoup
    response = requests.get('https://google.com')
    soup = BeautifulSoup(response.content, features='html.parser')
    return soup

def test_get_html_from_response(mock_get_soup, mock_get_requests):
    assert type(get_html_from_response(mock_get_requests)) == type(mock_get_soup)
