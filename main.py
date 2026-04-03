# import requests
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import re

def url_input():
	
	# url_input = "https://mykoreankitchen.com/korean-beef-bone-broth/"
	url_input = "https://mykoreankitchen.com/korean-fried-chicken/"

	url_input = "Input your URL:"
	if "mykoreankitchen.com" in url_input:
		return url_input
	else:
		return print("This program currently only supports scraping for mykoreankitchen.com")

def url_request(url):
	req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
	webpage = urlopen(req).read()
	soup = BeautifulSoup(webpage, 'lxml')
	return soup

def helpah(data, title_element, ingredient_list, soup):
	data[title_element] = ()
	for ingredient in ingredient_list:
		label = soup.find('label',class_='wprm-checkbox-label').text
		data[title_element] = data[title_element] + (re.sub(label, '',ingredient.text),)
	return data

def parse(soup):
	ingredients_lists = soup.find_all('div', class_='wprm-recipe-ingredient-group')
	list_dict = {}

	for recipes in ingredients_lists:
		ingredients = recipes.find(
			'ul', class_='wprm-recipe-ingredients'
		)
		
		try:
			sub_recipe = recipes.find(
				'h4', class_='wprm-recipe-group-name'
			).text

			helpah(list_dict, sub_recipe, ingredients, soup)
	
		except AttributeError:
			helpah(list_dict, 'Ingredients', ingredients, soup)
				
	return list_dict

def main():
	soup = url_request(url_input())
	text = parse(soup)
	return text

if __name__ == '__main__':
	print(main())