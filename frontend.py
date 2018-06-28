from backend import Database
import kivy
kivy.require("1.9.1")
from kivy.app import App
from kivy.uix.label import Label



class RecipeDataBase(App):
	def build(self):
		return Label(text="Hello")

if __name__ == "__main__":
    #test1 = Database()
	#test1.addRecipe("lovely dicks",["dicks","penis","cock"],["2","3","4"],["cook the cokes","eat my ass"])
	#print(test1.getRecipeList())
    RecipeDataBase().run()
    #test1.close()