class Recipe:
	def __init__(self, name, instructions, ingredients, quantities):
		self.name = name
		self.ingredients = ingredients
		self.quantities = quantities
		self.instructions = instructions
		self.occurrences = 0

	def getJSON(self):
		return {"name": self.name, "ingredients": self.ingredients, "quantities":self.quantities,"instructions": self.instructions}

	def print(self):
		print(self.name, self.ingredients, self.quantities, self.instructions)