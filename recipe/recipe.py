

class Recipe:
	def __init__(self, name, instructions, ingredients, quantities):
		self.name = name.lower()
		self.ingredients = [ingredient.lower() for ingredient in ingredients]
		
		self.quantities = quantities

		self.instructions = instructions
		self.occurrences = 0

	def getJSON(self):
		return {"name": self.name, "ingredients": self.ingredients, "quantities":[quantity.getStorageString() for quantity in self.quantities],"instructions": self.instructions}

	def print(self):
		print(self.name, self.ingredients, self.quantities, self.instructions)

