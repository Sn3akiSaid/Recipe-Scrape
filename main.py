# import requests
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import re

try:
	# url_input = input("Input URLS:")
	url_input = "https://mykoreankitchen.com/korean-beef-bone-broth/"
	print(url_input)
except:
	print('Invalid!')

def url_get(url):
	
	req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
	webpage = urlopen(req).read()
	soup = BeautifulSoup(webpage, 'lxml')
	return soup

def parse(soup):

	ingredients_lists = soup.find_all('div', class_='wprm-recipe-ingredient-group')
	data1 = {}
	data2 = []
	for titles in ingredients_lists:
		try:
			title_element = titles.find(
				'h4', class_='wprm-recipe-group-name'
			).text
			ingredients = titles.find(
				'ul', class_='wprm-recipe-ingredients'
			)

			data1[title_element] = ()
			for ingredient in ingredients:
				data1[title_element] = data1[title_element] + (ingredient.text,)
			return data1
	
		except AttributeError:
			ingredients = titles.find(
				'ul', class_='wprm-recipe-ingredients'
			)
			for ingredient in ingredients:
				data2.append(ingredient.text)
			return data2

soup = url_get(url_input)
text = parse(soup)

print(text)