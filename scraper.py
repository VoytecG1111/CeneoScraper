import requests
from bs4 import BeautifulSoup
import json
#product_code = input("Podaj kod produktu: ")

selectors = {
    "opinion_id":  [None, "data-entry-id"],
    "author":  ["span.user-post__author-name"],
    "recommendation":  ["span.user-post__author-recomendation > em"],
    "stars":  ["span.user-post__score-count"],
    "purchased":  ["div.review-pz"],
    "opinion_date":  ["span.user-post__published > time:nth-child(1)","datetime"],
    "purchase_date":  ["span.user-post__published > time:nth-child(2)","datetime"],
    "useful":  ["button.vote-yes","data-total-vote"],
    "unuseful":  ["button.vote-no","data-total-vote"],
    "content": ["div.user-post__text"],
    "cons": ["div.review-feature__title--negatives ~ div.review-feature__item", None, True],
    "pros": ["div.review-feature__title--positives ~ div.review-feature__item", None, True],

}


def get_element(ancestor, selector=None, attribute=None, return_list=False):
    try:
        if return_list:
            return [tag.text.strip() for tag in ancestor.select(selector)].copy()
        if not selector and attribute:
            return ancestor[attribute]
        if attribute:
            return ancestor.select_one(selector)[attribute].strip()
        return ancestor.select_one(selector).text.strip()
    except (AttributeError,TypeError):
        return None
    

product_code = "123849599"
url = f"https://www.ceneo.pl/{product_code}#tab=reviews"
while(url):
    print(url)
    response = requests.get(url)
    page_dom = BeautifulSoup(response.text, "html.parser")
    opinions = page_dom.select("div.js_product-review")
    all_opinions = []
    for opinion in opinions:
        single_opinion = {}
        for key, value in selectors.items():
            single_opinion[key] = get_element(opinion, *value)
        all_opinions.append(single_opinion)
    try:
        next_page = f"https://www.ceneo.pl"+get_element(page_dom,"a.pagination__next", "href")
    except TypeError:
        url = None


with open(f"./opinions/{product_code}.json", "w", encoding="UTF-8") as jf:
    json.dump(all_opinions, jf, indent=4, ensure_ascii=False)





#print(type(page_dom))
#print(type(opinions))
#print(len(opinions))
