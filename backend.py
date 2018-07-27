import sqlite3
import recipe as Recipe

class Database:

    def __init__(self,database):

        self.connection = sqlite3.connect(database)

        self.c = self.connection.cursor()

        # self.c.execute("""DROP TABLE IF EXISTS ingredients""")
        # self.c.execute("""DROP TABLE IF EXISTS recipes""")
        # self.c.execute("""DROP TABLE IF EXISTS instructions""")
        # self.c.execute("""DROP TABLE IF EXISTS recipeingredients""")
        # self.c.execute("""DROP TABLE IF EXISTS recipeinstructions""")

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

    def addRecipe(self,recipe):
        #self.c.execute("INSERT OR IGNORE INTO recipes (name) VALUES (?)",(recipe.name,))
        hold = self.c.execute("SELECT recipeID FROM recipes WHERE recipes.name = ?",(recipe.name,)).fetchone()

        if hold is  not None:
            return None

        self.c.execute("INSERT OR IGNORE INTO recipes (name) VALUES (?)",(recipe.name,))
        recipeID = hold = self.c.execute("SELECT recipeID FROM recipes WHERE recipes.name = ?",(recipe.name,)).fetchone()[0]

        ingredientIDList = []
        if type(recipe.ingredients) is not str:
            for ingredient in recipe.ingredients:
                self.c.execute("INSERT OR IGNORE INTO ingredients (name) VALUES (?)",(ingredient,))
                hold2 = self.c.execute("SELECT ingredientID FROM ingredients WHERE ingredients.name = ?",(ingredient,)).fetchone()
                ingredientIDList.extend(hold2)
        else:
            self.c.execute("INSERT OR IGNORE INTO ingredients (name) VALUES (?)",(recipe.ingredients,))
            hold2 = self.c.execute("SELECT ingredientID FROM ingredients WHERE ingredients.name = ?",(recipe.ingredients,)).fetchone()
            ingredientIDList.extend(hold2)

        instructionIDList = []
        if type(recipe.instructions) is not str:
            for index, instruction in enumerate(recipe.instructions):
                self.c.execute("INSERT OR IGNORE INTO instructions (instruction,num) VALUES (?,?)",(instruction,index+1))
                hold3 = self.c.execute("SELECT instructionID FROM instructions WHERE instructions.instruction = ?",(instruction,)).fetchone()
                instructionIDList.extend(hold3)
        else:
            self.c.execute("INSERT OR IGNORE INTO instructions (instruction,num) VALUES (?)",(recipe.instructions,1))
            hold2 = self.c.execute("SELECT instructionID FROM instructions WHERE instructions.instruction = ?",(recipe.instructions,)).fetchone()
            instructionIDList.extend(hold2)

        for instructionID in instructionIDList:
            self.c.execute("INSERT OR IGNORE INTO recipeinstructions (recipeID,instructionID) VALUES (?,?)",(recipeID,instructionID))

        for index, ingredientID in enumerate(ingredientIDList):
            self.c.execute("INSERT OR IGNORE INTO recipeingredients (recipeID,ingredientID,quantity) VALUES (?,?,?)",(recipeID,ingredientID,recipe.quantities[index]))

        return recipe

    def deleteRecipe(self,recipe_name):
        #returns None if not found
        check = self.c.execute("SELECT * FROM recipes WHERE recipes.name = ?",(recipe_name,)).fetchone()
        self.c.execute("DELETE FROM recipes WHERE recipes.name = ?",(recipe_name,))
        return check

    def getRecipe(self,recipe_name): #return either list or single answer, if list then print options 
        recipeID = self.c.execute("SELECT recipes.recipeID FROM recipes WHERE recipes.name = ?",(recipe_name,)).fetchone()
        if recipeID == None:
            return None
        elif len(recipeID) == 1:
            ingredientsQuantities = self.c.execute("SELECT ingredients.name, recipeingredients.quantity FROM ingredients INNER JOIN recipeingredients ON ingredients.ingredientID = recipeingredients.ingredientID AND recipeingredients.recipeID = ?",(recipeID[0],)).fetchall()
            instructions = self.c.execute("SELECT instructions.instruction, instructions.num FROM instructions INNER JOIN recipeinstructions ON recipeinstructions.instructionID = instructions.instructionID AND recipeinstructions.recipeID = ?",(recipeID[0],)).fetchall()
            ingredients, quantities = zip(*ingredientsQuantities)
            recipe = Recipe.Recipe(recipe_name, instructions, ingredients, quantities)
            return [recipe]
        else: # == 0, return None
            return None

    def keyWordSearchRecipes(self, keyword):
        names = [name[0] for name in self.c.execute("SELECT recipes.name FROM recipes").fetchall()]
        includes_keyword = []
        for name in names:
            if keyword in name:
                includes_keyword.append(name)
        if len(includes_keyword) == 0:
            return None    
        return includes_keyword

    def keyWordSearchIngredients(self, keyword):
        test = self.c.execute("SELECT ingredients.name FROM ingredients").fetchall()
        ingredient_names = []
        [ingredient_names.append(name[0]) for name in test if keyword in name[0] ]
        
        recipe_names = set([])
        for ingredient_name in ingredient_names:
            ingredientID = self.c.execute("SELECT ingredients.ingredientID FROM ingredients WHERE ingredients.name = ?",(ingredient_name,)).fetchone()
            recipe_name_list = self.c.execute("SELECT recipes.name FROM recipes INNER JOIN recipeingredients ON recipeingredients.ingredientID = ? AND recipes.recipeID = recipeingredients.recipeID",(ingredientID[0],)).fetchall()
            [recipe_names.add(name[0]) for name in recipe_name_list]
        return list(recipe_names)

    def getRecipeList(self):
        return [name[0] for name in self.c.execute("SELECT recipes.name FROM recipes").fetchall()]

    def getAllRecipes(self):
        return [self.getRecipe(name[0])[0] for name in self.c.execute("SELECT recipes.name FROM recipes").fetchall()]

    def close(self):
        self.connection.commit()
        self.connection.close()

# c.execute("INSERT OR IGNORE INTO recipes (name) VALUES ('dicks')")
# c.execute("INSERT OR IGNORE INTO recipes (name) VALUES (2)")
# c.execute("INSERT OR IGNORE INTO recipes (name) VALUES (3)")
# c.execute("INSERT OR IGNORE INTO recipes (name) VALUES (1)")
# test = c.execute("SELECT recipeID, * FROM recipes""")

# for row in test:
#   print(row[0])

# addRecipe("lovely dicks",["dicks","penis","cock"],["2","3","4"],["cook the cokes","eat my ass"])
# print(getRecipeList())
# print(getRecipe("lovely dicks"))
# print(getRecipe("lovely dick"))



# connection.commit()
# connection.close()