import requests
import json
from requests.exceptions import HTTPError, Timeout, RequestException


from bs4 import BeautifulSoup
import re


# from databaser import data_entry
def url_input():
    """Soupify data"""

    # Some test URLS
    # usr_inp = "https://mykoreankitchen.com/korean-beef-bone-broth/"
    # usr_inp = "https://mykoreankitchen.com/korean-fried-chicken/"
    # usr_inp = "https://boldbeanco.com/blogs/beanspo-recipes/homemade-baked-beans?srsltid=AfmBOopkr11KNW1BU6rqKyp_RTdpiDcQQwREQuEX-g_a3bMmMPpiq8lB"

    usr_inp = input("Input your recipe URL: ").strip()

    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"
    }

    try:
        response = requests.get(usr_inp, headers=headers, timeout=5)
        response.raise_for_status()
        return response
    except HTTPError as http_err:
        print(f"HTTP ERROR: {http_err}")
    except Timeout as timeout_err:
        print(f"TIMEOUT ERROR: {timeout_err}")
    except RequestException as err:
        print(f"REQUEST ERROR: {err}")
    return None


def souper(validresponse):

    soup = BeautifulSoup(validresponse.content, "lxml")

    return soup


# Dated Parsing
def parse_ingredient_group(data, title_element, ingredient_list, soup):
    data[title_element] = ()
    for ingredient in ingredient_list:
        label = ingredient_list.find("label", class_="wprm-checkbox-label").text
        data[title_element] = data[title_element] + (
            re.sub(label, "", ingredient.text),
        )
    return data


def parse(soup):
    """Dated parser, generic HTML"""
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


# Dated Parsing


def parser(soup):
    """Updated json parser"""
    ingredients_lists = soup.find("script", type="application/ld+json").text.strip()
    data = json.loads(ingredients_lists)
    return data


def finder(data, target="recipeIngredient"):
    """Targets the specific ingredient convention of sites"""

    if isinstance(data, dict):
        if target in data:
            return data[target]
        for value in data.values():
            result = finder(value, target)
            if result is not None:
                return result

    elif isinstance(data, list):
        for item in data:
            if item.get("@type") == "Recipe":
                return item[target]


def main():
    validated_url = url_input()
    soup = souper(validated_url)
    trial_db = finder(parser(soup))
    print(trial_db)
    # data_entry(trial_db, url)


if __name__ == "__main__":
    main()
