# coding: utf-8
import re
from bs4 import BeautifulSoup
import requests


def slugify(text: str) -> str:
    """Replaces whitespace and commas in SOTU titles for use as filenames."""
    return text.strip().replace(', ', '-').replace(' ', '_').lower()

def get_links() -> list:
    """Fetches all links to SOTU speeches from the essay page."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
        "Accept": "text/html",
        "Accept-Encoding": "gzip, deflate",
    }
    p = re.compile(r'\d+.html')
    base_url = 'http://stateoftheunion.onetwothree.net/texts/'
    essay_url = base_url + 'index.html'
    res = requests.get(essay_url, headers=headers)
    soup = BeautifulSoup(res.content, 'html')
    links = soup.find_all('a')
    sotu_links = {link.text: base_url + link.get('href', '') for link in links if re.match(p, link.get('href', ''))}
    return sotu_links

def clean_sotu(speech_link: str, headers: dict) -> str:
    """Fetches and cleans up the text of a SOTU from the provided website URL."""
    response = requests.get(speech_link, headers=headers)
    sotu_soup = BeautifulSoup(response.content, 'html')
    text = sotu_soup.find('div', {'id': 'text'}).text.replace('< Previous\xa0\xa0\xa0Next >', '').rstrip('^ Return to top\n').strip()
    speech = text.lstrip('State of the Union Address').strip()
    return speech

def download_speeches(sotu_links: dict):
    """Downloads all SOTU addresses as TXT files."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
        "Accept": "text/html",
        "Accept-Encoding": "gzip, deflate",
    }
    for name, link in sotu_links.items():
        with open(f'speeches/{slugify(name)}.txt', 'w') as fout:
            fout.write(clean_sotu(link, headers))


download_speeches(get_links())
