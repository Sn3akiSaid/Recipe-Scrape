### Recipe Scraper 

Basic recipe scraper that utilises BeautifulSoup to pull out an ingredient list out of a recipe website.\\
Utilizes schema.org standardization to extract a "recipeIngredient" list from recipe websites.

**Very early stages**

Run by
```
uv run python3 main.py
```

UPDATE:
Added early implementation of storage using SQLite3- stores recipe URLs into a database, with the ingredients list linked to each recipe.