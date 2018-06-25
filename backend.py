import sqlite3

connection = sqlite3.connect("database/database.db")

c = connection.cursor()

#Create ingredients
c.execute("""CREATE TABLE IF NOT EXISTS ingredients (ingredientID INTEGER PRIMARY KEY, name TEXT)""")
c.execute("""CREATE TABLE IF NOT EXISTS recipes (recipeID INTEGER PRIMARY KEY, name TEXT, instructions TEXT)""")
c.execute("""CREATE TABLE IF NOT EXISTS recipeingredients (recipeID INT FOREIGN KEY references recipes.recipeID, ingredientID INT FOREIGN KEY references ingredients.ingredientID, quantity TEXT)""")

