from bs4 import BeautifulSoup as bs
import requests
import re

#def emblem_search(emblem):
#    for page_number in range(1, 5):
#        page = requests.get(f"https://warmind.io/analytics/item/emblems?page={page_number}")
#        soup = bs(page.content, features="lxml")
#        quotes = [re.sub(r'\n+', '\n', i.text).strip() for i in soup.find_all(class_="panel panel-filled text-center warmind-hover")]
#
#        wynik = [quotes[x] for x in range(0, len(quotes)) if emblem.upper() in quotes[x].upper()]
#        if wynik:
#            return [i for i in wynik[0].split("\n")]
#    return "Emblem not found! Check for typos"


def emblem_search(emblem):
    for page_number in range(1, 5):
        page = requests.get(f"https://warmind.io/analytics/item/emblems?page={page_number}")
        soup = bs(page.content, features="lxml")
        for x in soup.find_all(class_="panel panel-filled text-center warmind-hover"):
            EmblemName = x.h5.text.replace(x.h5.small.text.strip(), "").strip().upper()
            if emblem.upper() in EmblemName:
                list = [i for i in [re.sub(r'\n+', '\n', x.text.replace(x.h5.small.text.strip(), "")).strip()][0].split("\n")]
                return [list, x.img.get("src")]
    return "Emblem not found! Check for typos"
    
