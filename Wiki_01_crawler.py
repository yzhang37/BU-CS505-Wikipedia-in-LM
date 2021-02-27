import re

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

import config

RC_FINDENTRY = re.compile(r"(?=^/wiki/)([^:#=<>]*?)")

cache_dict = set()
entry = '/wiki/Coronavirus_disease_2019'

f = open(config.PATH_ORIGINAL, 'w')


def scrape_recursive(entry, depth=1):
    if entry not in cache_dict:
        cache_dict.add(entry)
    else:
        return
    response = requests.get("https://en.wikipedia.org/" + entry, allow_redirects=False)
    soup = BeautifulSoup(response.content, 'html.parser')
    content_body = soup.find('div', {
        "id": "bodyContent"
    })
    f.write(content_body.text)
    f.flush()
    if depth <= 0:
        return
    content_lists = content_body.find_all("a", attrs={'href': RC_FINDENTRY})
    redirect_to_remove = soup.find_all('a', attrs={'class': 'mw-redirect'})
    content_lists_url = map(lambda x: x.attrs['href'], content_lists)
    redirect_to_remove_url = map(lambda x: x.attrs['href'], redirect_to_remove)
    remains = set(content_lists_url) - set(redirect_to_remove_url)
    for next_entry in tqdm(remains):
        if next_entry not in cache_dict:
            scrape_recursive(next_entry, depth - 1)


scrape_recursive(entry)
f.close()
