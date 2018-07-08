import sqlite3

class Database:

	def __init__(self,database):

		self.connection = sqlite3.connect(database)

		self.c = self.connection.cursor()

		self.c.execute("""DROP TABLE IF EXISTS ingredients""")
		self.c.execute("""DROP TABLE IF EXISTS recipes""")
		self.c.execute("""DROP TABLE IF EXISTS instructions""")
		self.c.execute("""DROP TABLE IF EXISTS recipeingredients""")
		self.c.execute("""DROP TABLE IF EXISTS recipeinstructions""")

		#Create ingredients
		self.c.execute("""CREATE TABLE IF NOT EXISTS ingredients (
			ingredientID INTEGER PRIMARY KEY, 
			name TEXT,
			UNIQUE(name)
		)
		""")

		self.c.execute("""CREATE TABLE IF NOT EXISTS recipes (
			recipeID INTEGER PRIMARY KEY, 
			name TEXT,
			UNIQUE(name)
		)
		""")

		self.c.execute("""CREATE TABLE IF NOT EXISTS instructions (
			instructionID INTEGER PRIMARY KEY,
			instruction TEXT,
			num INTEGER
		)
		""")

		self.c.execute("""CREATE TABLE IF NOT EXISTS recipeingredients (
			recipeID INTEGER NOT NULL,
			ingredientID INTEGER NOT NULL,
			quantity TEXT,
			FOREIGN KEY (recipeID) REFERENCES recipes(recipeID),
			FOREIGN KEY (ingredientID) REFERENCES ingredients(ingredientID)
		)
		""")

		self.c.execute("""CREATE TABLE IF NOT EXISTS recipeinstructions (
			recipeID INTEGER NOT NULL,
			instructionID INTEGER NOT NULL,
			FOREIGN KEY (recipeID) REFERENCES recipes(recipeID),
			FOREIGN KEY (instructionID) REFERENCES instructions(instructionID)
		)
		""")
		self.test2 = "fuck"


	def addRecipe(self,recipe_name, ingredients, quantities, instructions):
		self.c.execute("INSERT OR IGNORE INTO recipes (name) VALUES (?)",(recipe_name,))
		hold = self.c.execute("SELECT recipeID FROM recipes WHERE recipes.name = ?",(recipe_name,)).fetchone()
		recipeID = hold[0]

		ingredientIDList = []
		if type(ingredients) is not str:
			for ingredient in ingredients:
				self.c.execute("INSERT OR IGNORE INTO ingredients (name) VALUES (?)",(ingredient,))
				hold2 = self.c.execute("SELECT ingredientID FROM ingredients WHERE ingredients.name = ?",(ingredient,)).fetchone()
				ingredientIDList.extend(hold2)
		else:
			self.c.execute("INSERT OR IGNORE INTO ingredients (name) VALUES (?)",(ingredients,))
			hold2 = self.c.execute("SELECT ingredientID FROM ingredients WHERE ingredients.name = ?",(ingredients,)).fetchone()
			ingredientIDList.extend(hold2)

		instructionIDList = []
		if type(instructions) is not str:
			for instruction in instructions:
				self.c.execute("INSERT OR IGNORE INTO instructions (instruction) VALUES (?)",(instruction,))
				hold3 = self.c.execute("SELECT instructionID FROM instructions WHERE instructions.instruction = ?",(instruction,)).fetchone()
				instructionIDList.extend(hold3)
		else:
			self.c.execute("INSERT OR IGNORE INTO instructions (instruction) VALUES (?)",(instructions,))
			hold2 = self.c.execute("SELECT instructionID FROM instructions WHERE instructions.instruction = ?",(instructions,)).fetchone()
			instructionIDList.extend(hold2)

		for instructionID in instructionIDList:
			self.c.execute("INSERT OR IGNORE INTO recipeinstructions (recipeID,instructionID) VALUES (?,?)",(recipeID,instructionID))

		for index, ingredientID in enumerate(ingredientIDList):
			self.c.execute("INSERT OR IGNORE INTO recipeingredients (recipeID,ingredientID,quantity) VALUES (?,?,?)",(recipeID,ingredientID,quantities[index]))

	def deleteRecipe(self,recipe_name):
		if self.c.execute("SELECT * FROM recipes WHERE recipes.name = ?",(recipe_name,)).fetchone() is None:
			print("fuck")
		self.c.execute("DELETE FROM recipes WHERE recipes.name = ?",(recipe_name,))

	def getRecipe(self,recipe_name): #return either list or single answer, if list then print options 
		recipeID = self.c.execute("SELECT recipes.recipeID FROM recipes WHERE recipes.name = ?",(recipe_name,)).fetchall()
		length = len(recipeID)
		if length == 1:
			ingredientsQuantities = self.c.execute("SELECT ingredients.name, recipeingredients.quantity FROM ingredients INNER JOIN recipeingredients ON ingredients.ingredientID = recipeingredients.ingredientID AND recipeingredients.recipeID = recipeID").fetchall()
			instructions = self.c.execute("SELECT instructions.instruction FROM instructions INNER JOIN recipeinstructions ON recipeinstructions.instructionID = instructions.instructionID AND recipeinstructions.recipeID = recipeID").fetchall()
			return [recipe_name,ingredientsQuantities,instructions]
		else: # == 0, return None
			return None

	def keyWordSearchRecipes(self):
		return

	def keyWordSearchIngredients(self):
		return

	def getRecipeList(self):
		return [name[0] for name in self.c.execute("SELECT recipes.name FROM recipes").fetchall()]

	def close(self):
		self.connection.commit()
		self.connection.close()

# c.execute("INSERT OR IGNORE INTO recipes (name) VALUES ('dicks')")
# c.execute("INSERT OR IGNORE INTO recipes (name) VALUES (2)")
# c.execute("INSERT OR IGNORE INTO recipes (name) VALUES (3)")
# c.execute("INSERT OR IGNORE INTO recipes (name) VALUES (1)")
# test = c.execute("SELECT recipeID, * FROM recipes""")

# for row in test:
# 	print(row[0])

# addRecipe("lovely dicks",["dicks","penis","cock"],["2","3","4"],["cook the cokes","eat my ass"])
# print(getRecipeList())
# print(getRecipe("lovely dicks"))
# print(getRecipe("lovely dick"))



# connection.commit()
# connection.close()