### Recipe Scraper 

Basic recipe scraper that utilises BeautifulSoup to pull out an ingredient list out of a recipe website.\\
Utilizes schema.org standardization to extract a "recipeIngredient" list from recipe websites.\\
Rudimentary CRUD app

Roadmap: Combine script with CRUD app. Deploy on own Linux server.

**Very early stages**

Run script by
```
uv run main.py
```

Run app by
```
uv run app.py
```

UPDATE:
Added early implementation of storage using SQLite3- stores recipe URLs into a database, with the ingredients list linked to each recipe.