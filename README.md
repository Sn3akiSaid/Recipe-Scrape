### Recipe Scraper 

Basic recipe scraper that utilises BeautifulSoup to pull out an ingredient list out of a recipe website.\\
The idea is to have a simple app that gets you straight to the ingredients and instruction of a recipe, saving you time by skipping ads, long article/story- style introductions, etc.

**Very early stages**

Run by
```
python3 main.py
```

UPDATE:
Support for more websites added by introducing a generalised routine.
Added early implementation of storage using SQLite3- stores recipe URLs into a database, with the ingredients list linked to each recipe.