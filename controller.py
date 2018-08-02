import json

from recipe_scrapers import scrape_me
from frontend import GUI
from backend import Database
from recipe import Recipe,  Quantity, stringsToQuantities

class Controller():
    def __init__(self,database):
        self.database = Database(database)
        self.GUI = GUI(self)
        
    def writeRecipeFile(self, file):
        recipes = self.database.getAllRecipes()
        print(recipes)
        
        text = "["
        for recipe in recipes:
            text += (json.dumps(recipe.getJSON(),indent=4, sort_keys=True) + ",")

        text = text[:-1]
        text += "]"
        file.write(text)
        file.close()
        return

    def readRecipeFile(self, fileName):
        file = open(fileName, mode = "r")
        if file is None:
            return
        try:
            text = json.load(file)
            for recipe in text:
                recipe = Recipe(recipe["name"],recipe["instructions"], recipe["ingredients"], stringsToQuantities(recipe["quantities"]))
                recipe.print()
                self.database.addRecipe(recipe)
        except (ValueError) as e:
            file.close()
            return
        file.close()
        return

    def shutdown(self):
        self.database.close()

    def switchDatabase(self, fileName):
        self.database = Database(fileName)
        return

    def addRecipe(self, recipe):
        return self.database.addRecipe(recipe)

    def deleteRecipe(self, keyword):
        return self.database.deleteRecipe(keyword)

    def ingredientKeywordSearch(self, keyword):
        return self.database.keyWordSearchIngredients(keyword)

    def recipeKeywordSearch(self, keyword):
        hold = self.database.getRecipe(keyword)
        if hold is None:
            return self.database.keyWordSearchRecipes(keyword)
        else:
            return hold

    def getAllRecipeNames(self):
        return self.database.getRecipeList()

    def getRecipe(self, keyword):
        return self.database.getRecipe(keyword)


if __name__ == '__main__':
    controller = Controller("cookbooks/database.db")
    controller.shutdown()
