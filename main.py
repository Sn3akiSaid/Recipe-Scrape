import requests
import json

# from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import re


def url_input():

    # url_input = "https://mykoreankitchen.com/korean-beef-bone-broth/"
    # url_input = "https://mykoreankitchen.com/korean-fried-chicken/"

    user_input = input("Input your URL: ")
    if "mykoreankitchen.com" in user_input:
        return user_input
    else:
        print("This program currently only supports scraping for mykoreankitchen.com")
        return None


def url_request(url):
    response = requests.get(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        },
    )
    # webpage = urlopen(response).read()
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "lxml")
    # print(response.status_code)
    # print(response.text[:500])
    return soup


def parse_ingredient_group(data, title_element, ingredient_list, soup):
    data[title_element] = ()
    for ingredient in ingredient_list:
        label = ingredient_list.find("label", class_="wprm-checkbox-label").text
        data[title_element] = data[title_element] + (
            re.sub(label, "", ingredient.text),
        )
    return data


def parse(soup):
    ingredients_lists = soup.find_all("div", class_="wprm-recipe-ingredient-group")
    list_dict = {}

    for recipes in ingredients_lists:
        ingredients = recipes.find("ul", class_="wprm-recipe-ingredients")

        try:
            sub_recipe = recipes.find("h4", class_="wprm-recipe-group-name").text

            parse_ingredient_group(list_dict, sub_recipe, ingredients, soup)

        except AttributeError:
            parse_ingredient_group(list_dict, "Ingredients", ingredients, soup)

    return print(list_dict)


def parse2(soup):
    ingredients_lists = soup.find("script", type="application/ld+json")
    data = json.loads(ingredients_lists.string)
    with open("recipe.json", "w") as f:
        json.dump(data, f, indent=2)


def main():
    url = url_input()
    if url is None:
        return print("hm")
    soup = url_request(url)
    return parse2(soup)


if __name__ == "__main__":
    print(main())
