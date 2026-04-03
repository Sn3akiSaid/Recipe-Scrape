### Recipe Scraper 

Basic recipe scraper that utilises BeautifulSoup to pull out an ingredient list out of a recipe website. The idea is to have a simple app that pulls gets you straight to the ingredients and recipe, saving you time by skipping ads, long article/story style introductions, etc.

**Very early stages** - currently supports only mykoreankitchen.com.

Run by
```
python3 main.py
```

Planning to add:
Support for more websites- ideally through a more generalised routine, rather than website specific HTML parsing.
Option to store looked up recipe into a folder, with recipe title and url for easy later lookup.
Scrape instructions too.