import frontend as GUI
import backend as Database

class Controller():
	def __init__(self,database):
		self.database = Database.Database(database)
		self.GUI = GUI.GUI(self)
		

	def shutdown(self):
		self.database.close()

	def addRecipe(self, recipe_name, instructions,ingredients, quantities):
		print(", ".join( repr(e) for e in (recipe_name, instructions, ingredients, quantities)))
		self.database.addRecipe(recipe_name,ingredients,quantities,instructions)
		return

if __name__ == '__main__':
	controller = Controller("database/database.db")
	controller.shutdown()
