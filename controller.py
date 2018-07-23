import frontend as GUI
import backend as Database
import recipe as Recipe

class Controller():
	def __init__(self,database):
		self.database = Database.Database(database)
		recipe = Recipe.Recipe("fuck", ["suck me"], ["dicks", "cocks", "cocknug"], ["1","2","3"])
		self.database.addRecipe(recipe)
		self.GUI = GUI.GUI(self)
		

	def shutdown(self):
		self.database.close()

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


if __name__ == '__main__':
	controller = Controller("database/database.db")
	controller.shutdown()
