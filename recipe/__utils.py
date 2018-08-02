from recipe_scrapers import scrape_me
from .recipe import Recipe
import re
import inflect

p = inflect.engine()


weights = {'kg': 1, 'g': 1000, 'mg': 1000000, 'lbs': 2.2}
volumes = {'gal':1, 'qt':4, 'pt':8, 'cups':16, 'oz':128, 'tbsp':256,'tablespoon':256, 'tsp': 768, 'teaspoon': 768,'mL':3800, 'L':3.8}
amounts = {"x": "x", "slice": "slice"}

unit_dict_list = [weights, volumes, amounts]

smallestUnit = {"volumes": "mL", "weights": "mg", **amounts}

def scrapeRecipe(scrape):
    recipe_name = scrape.title()

    scraped_instructions = scrape.instructions()

    recipe_instructions = scraped_instructions.split("\n")
    del recipe_instructions[-1]

    scraped_ingredients = scrape.ingredients()

    recipe_ingredients = []
    recipe_quantities = []

    for scraped_ingredient in scraped_ingredients:

        if "-" in scraped_ingredient:
            ingredient = scraped_ingredient.split("-")[0]
        else:
            ingredient = scraped_ingredient

        words = re.findall(r"[\w']+", scraped_ingredient)
        #print(words)

        if is_number(words[0]):
            ingredient = ingredient.replace(words[0],"")
            units = []

            for word in words:
                for unit_dict in unit_dict_list:
                    for key in unit_dict:
                        word2 = getSingular(word).lower()
                        key2 = getSingular(key).lower()

                        if key2 == "slouse": key2 = "slice"
                        print(word2,key2)
                        if str(word2) == str(key2):
                            ingredient = ingredient.replace(word,"")
                            units.append(word2)
            
            if len(units) == 1:
                quantity = Quantity(words[0], units[0])
                print("1")
                quantity.print()
            elif len(units) == 0:
                quantity = Quantity(words[0], "x")
                print("2")
                quantity.print()
            else:
                quantity = Quantity(words[0], units[0])
                print("3")
                quantity.print()

            ingredient = ingredient.replace("  "," ")
            ingredient = ingredient.strip()

            if ingredient.strip() == "" or quantity == None:
                continue

            recipe_ingredients.append(ingredient)
            recipe_quantities.append(quantity)

        else:
            continue
    
    return Recipe(recipe_name, recipe_instructions, recipe_ingredients, recipe_quantities)


def getSingular(string):
    if p.singular_noun(string) is False:
        return string
    else:
        return p.singular_noun(string)

def is_number(string):
    try:
        float(string)
        return True
    except:
        return False

def unitConversion(quantity, unit_out):
    print(unit_out)
    for unit_dict in unit_dict_list:
        if unit_dict is amounts:
            return quantity
        elif unit_out in unit_dict:
            #volumes = {'gal':1, 'qt':4, 'pt':8, 'cups':16, 'oz':128, 'tbsp':256, 'tsp': 768, 'mL':3800, 'L':3.8}
            print(type(quantity.value),type(unit_dict[unit_out]),type(unit_dict[quantity.unit]))
            return Quantity(quantity.value * unit_dict[unit_out]/unit_dict[quantity.unit], unit_out)
    return None


def sumAndBestValue(quantities_list):

    unit_types_used = {} 

    for quantity in quantities_list:
        quantity.print()

        print(smallestUnit)
        print(quantity.unit_type)
        base_unit = smallestUnit[quantity.unit_type]

        print(quantity.unit_type)
        if quantity.unit_type in unit_types_used.keys():
            unit_types_used[quantity.unit_type].value += unitConversion(quantity, base_unit).value
        else:
            unit_types_used[quantity.unit_type] = unitConversion(quantity, base_unit)

    print(unit_types_used)
    return_list = [bestValue(unit_types_used[key]) for key in unit_types_used.keys()]
    print(return_list)
    return return_list


def bestValue(quantity):
    for unit_dict in unit_dict_list:
        print(quantity.unit_type, unit_dict)
        if quantity.unit in unit_dict:
            print("got here")
            for unit in [key for key in sorted(unit_dict, key = unit_dict.get)]:
                convert = unitConversion(quantity, unit)
                if convert.value > 1:
                    return convert
            return unitConversion(quantity, smallestUnit[unit_type])

def getUnitType(unit):
    if unit in volumes.keys():
        return "volumes"
    elif unit in weights.keys():
        return "weights"
    elif unit in amounts.keys():
        return unit

def stringsToQuantities(str_quantities):
    quantities = []
    for str_quantity in str_quantities:
        hold = str_quantity.split("|")
        quantities.append(Quantity(hold[0],hold[1]))
    return quantities


class Quantity:
    def __init__(self, value, unit):
        self.value = float(value)
        self.unit = unit
        self.unit_type = getUnitType(self.unit)

    def getStorageString(self):
        return str(str(self.value) + "|" + self.unit)

    def print(self):
        print(self.getStorageString())


