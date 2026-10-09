import requests
import time
import random
import json
from requests.exceptions import HTTPError, Timeout, RequestException
from bs4 import BeautifulSoup
import re

USER_AGENT = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5)"
    "AppleWebKit/537.36 (KHTML, like Gecko)"
    "Chrome/50.0.2661.102 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate",
    "Connection": "keep-alive",
}


# from databaser import data_entry
def url_input(url: str, max_retries: int = 5) -> requests.Response:
    """Soupify data"""

    # Some test URLS
    # usr_inp = "https://mykoreankitchen.com/korean-beef-bone-broth/"
    # usr_inp = "https://mykoreankitchen.com/korean-fried-chicken/"
    # https://boldbeanco.com/blogs/beanspo-recipes/homemade-baked-beans?srsltid=AfmBOopkr11KNW1BU6rqKyp_RTdpiDcQQwREQuEX-g_a3bMmMPpiq8lB
    response = requests.get(url, headers=USER_AGENT, timeout=5)
    # response.raise_for_status()
    # return response
    while True:
        try:
            response.raise_for_status()
            return response
            # for attempt in range(max_retries):
            #     response = requests.get(url, headers=USER_AGENT, timeout=(5, 30))
            #     response.raise_for_status()
            #     if response.status_code != 429:
            #         return response

            #     retry_after = response.headers.get("Retry-After")
            #     delay = float(retry_after) if retry_after else min(2**attempt, 60)
            #     time.sleep(delay + random.uniform(0, 1))
            #     print(retry_after)
            # raise RuntimeError(f"Still rate limited after {max_retries} retries")
        # except Exception as exc:
        #     print(f"There was a problem: {exc}")
        except HTTPError as http_err:
            print(f"HTTP Error occured: {http_err}")
            continue
        except Timeout as timeout_err:
            print(f"TIMEOUT Error occured: {timeout_err}")
            continue
        except RequestException as err:
            print(f"REQUEST Error occured: {err}")
            continue


# def souper(validresponse):

#     soup = BeautifulSoup(validresponse.content, "lxml")

#     return soup


# Dated Parsing
# def parse_ingredient_group(data, title_element, ingredient_list, soup):
#     data[title_element] = ()
#     for ingredient in ingredient_list:
#         label = ingredient_list.find("label", class_="wprm-checkbox-label").text
#         data[title_element] = data[title_element] + (
#             re.sub(label, "", ingredient.text),
#         )
#     return data
# def parse(soup):
#     """Dated parser, generic HTML"""
#     ingredients_lists = soup.find_all("div", class_="wprm-recipe-ingredient-group")
#     list_dict = {}

#     for recipes in ingredients_lists:
#         ingredients = recipes.find("ul", class_="wprm-recipe-ingredients")

#         try:
#             sub_recipe = recipes.find("h4", class_="wprm-recipe-group-name").text

#             parse_ingredient_group(list_dict, sub_recipe, ingredients, soup)

#         except AttributeError:
#             parse_ingredient_group(list_dict, "Ingredients", ingredients, soup)

#     return print(list_dict)
# Dated Parsing


def parser(validresponse: requests.Response) -> dict | list:
    """Updated json parser"""
    soup = BeautifulSoup(validresponse.content, "lxml")
    try:
        script = soup.find("script", type="application/ld+json")
        if script is None:
            raise ValueError("No JSON-LD found.")
        script_text = script.string
        if script_text is None:
            raise ValueError("No text content in JSON-LD")
        data = json.loads(script_text)
    except ValueError:
        print("No valid json")

    return data


def finder(data: dict | list, target: str = "recipeIngredient") -> list | None:
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
    URL = input("Input your recipe URL: ")
    # url_input(URL)
    # soup = souper(url)

    trial_db = finder(parser(url_input(URL)))
    print(trial_db)
    # data_entry(trial_db, url)


if __name__ == "__main__":
    main()
