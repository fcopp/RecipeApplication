import json

import frontend as GUI
import backend as Database
import recipe as Recipe

class Controller():
    def __init__(self,database):
        self.database = Database.Database(database)
        # recipe = Recipe.Recipe("fuck", ["suck me"], ["dicks", "cocks", "cocknug"], [1,2,3])
        # self.database.addRecipe(recipe)
        self.GUI = GUI.GUI(self)
        
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
                recipe = Recipe.Recipe(recipe["name"],recipe["instructions"], recipe["ingredients"], recipe["quantities"])
                recipe.print()
                self.database.addRecipe(recipe)
        except (ValueError) as e:
            return
        return

        file.close()

    def shutdown(self):
        self.database.close()

    def switchDatabase(self, fileName):
        self.database = Database.Database(fileName)
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

    def getRecipe(self, keyword):
        return self.database.getRecipe(keyword)


if __name__ == '__main__':
    controller = Controller("database/database.db")
    controller.shutdown()
