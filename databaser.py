import sqlite3


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


# conn object stored in variable, connects to one SQLite db file
conn = sqlite3.connect("recipes.db", isolation_level=None)
c = conn.cursor()
# c.execute("PRAGMA foreign_keys = ON")


def data_entry0(data_list, url):
    c.execute(
        "CREATE TABLE IF NOT EXISTS recipes(recipe_name TEXT NOT NULL) VALUES(?)",
        (url,),
    )
    recipe_id = c.lastrowid
    for ingredient in data_list:
        c.execute(
            "INSERT INTO ingredients(ingredient_member, recipe_id) VALUES(?, ?)",
            (ingredient, recipe_id),
        )
    conn.commit()
    c.execute("SELECT * FROM recipes")
    print(c.fetchall())
    c.execute("SELECT * FROM ingredients")
    print(c.fetchall())


def data_entry(data_list, url):
    """Rewrite"""

    c.execute("CREATE TABLE IF NOT EXISTS Recipes (recipe_name TEXT NOT NULL) STRICT")
    c.execute(
        "CREATE TABLE IF NOT EXISTS Ingredients_and_Steps (ingredient_id INT, ingerdient TEXT NOT NULL, step_number INT, step TEXT NOT NULL) STRICT"
    )
    c.execute(
        "INSERT INTO Recipes VALUES (?)",
        [
            url,
        ],
    )

    for ingredient in enumerate(data_list):
        c.execute("INSERT INTO Ingredients_and_Steps VALUES (?, ?)", ingredient)
