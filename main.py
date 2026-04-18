import requests
import json

# import pandas as pd
import sqlite3
from bs4 import BeautifulSoup
import re

conn = sqlite3.connect("recipes.db")
c = conn.cursor()
c.execute("PRAGMA foreign_keys = ON")

# c.execute("""DROP TABLE IF EXISTS ingredients""")
# c.execute("""DROP TABLE IF EXISTS recipes""")

# c.execute("""CREATE TABLE recipes(
#           recipe_id INTEGER PRIMARY KEY,
#           recipe_name TEXT NOT NULL
#           )""")

# c.execute("""CREATE TABLE ingredients(
#           ingredient_id INTEGER PRIMARY KEY,
#           ingredient_member TEXT NOT NULL,
#           recipe_id INTEGER NOT NULL,
#           FOREIGN KEY (recipe_id) REFERENCES recipes(recipe_id)
#           )""")


# ingredient = "1 tsp chipotle paste or powder"

# c.execute("""INSERT INTO ingredients VALUES(?)""", (ingredient,))
# conn.commit()
# from urllib.request import Request, urlopen


def url_input():

    # usr_inp = "https://mykoreankitchen.com/korean-beef-bone-broth/"
    # usr_inp = "https://mykoreankitchen.com/korean-fried-chicken/"
    usr_inp = "https://boldbeanco.com/blogs/beanspo-recipes/homemade-baked-beans?srsltid=AfmBOopkr11KNW1BU6rqKyp_RTdpiDcQQwREQuEX-g_a3bMmMPpiq8lB"
    return usr_inp
    # return input("Input your URL: ")
    # if "mykoreankitchen.com" in user_input:
    #     return user_input
    # else:
    #     print("This program currently only supports scraping for mykoreankitchen.com")
    #     return None


def url_request(url):

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, "lxml")

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
    ingredients_lists = soup.find("script", type="application/ld+json").text.strip()
    data = json.loads(ingredients_lists)
    return data


def finder(data, target="recipeIngredient"):
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


def data_entry(data_list, url):
    c.execute("""INSERT INTO recipes(recipe_name) VALUES(?)""", (url,))
    recipe_id = c.lastrowid
    for ingredient in data_list:
        c.execute(
            """INSERT INTO ingredients(ingredient_member, recipe_id) VALUES(?, ?)""",
            (ingredient, recipe_id),
        )
    conn.commit()
    c.execute("""SELECT * FROM recipes""")
    print(c.fetchall())
    c.execute("""SELECT * FROM ingredients""")
    print(c.fetchall())


def main():
    url = url_input()
    if url is None:
        return print("hm")
    soup = url_request(url)
    trial_db = finder(parse2(soup))

    data_entry(trial_db, url)


if __name__ == "__main__":
    main()
