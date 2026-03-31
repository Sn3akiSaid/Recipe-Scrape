# import requests
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup

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
	data = []
	for titles in ingredients_lists:
		try:
			title_element = titles.find('h4', class_='wprm-recipe-group-name')
			data.append(title_element.text)
			ingredient_element = titles.find('ul', class_='wprm-recipe-ingredients')
			data.append(ingredient_element.text)
		except AttributeError:
			ingredient_element = titles.find('ul', class_='wprm-recipe-ingredients')
			data.append(ingredient_element.text)
			
	print(data)

soup = url_get(url_input)
parse(soup)
