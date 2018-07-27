import tkinter as tk
import os
from tkinter import messagebox
from tkinter import filedialog
from recipe import Recipe

def unitConversion(value, unit_in, unit_out):
    units = {'gal':1, 'qt':4, 'pt':8, 'cups':16, 'oz':128, 'tbsp':256, 'tsp': 768, 'mL':3800, 'L':3.8}
    return value * units[unit_out]/units[unit_in]

def bestValue(value):
    units = ["gal","L","cups","oz","tbsp","tsp","mL"]

    for unit in units:
        convert = unitConversion(value,"mL",unit)
        if unit is "cups" and convert >= 0.25:
            return (convert,unit)
        if convert > 1:
            return (convert,unit)
    return (value, "mL")

class AutoScrollbar(tk.Scrollbar):
    def __init__(self, parent, orient = "vertical", command = None):
        tk.Scrollbar.__init__(self,parent, orient = orient, command = command)
    def set(self, lo, hi):
        if float(lo) <= 0.0 and float(hi) >= 1.0:
            self.tk.call("grid", "remove", self)
        else:
            self.grid()
        tk.Scrollbar.set(self, lo, hi)

class scrollingFrame(tk.Frame):
    def __init__(self, parentObject, height, width = 100):
        tk.Frame.__init__(self, parentObject,height = height,  bg = "white")
        self.canvas = tk.Canvas(self, borderwidth=1, highlightthickness=0, relief = "sunken",height = height, width = width, bg = "white")
        self.frame = tk.Frame(self.canvas,bg = "white")

        self.vsb = AutoScrollbar(self, orient = "vertical", command = self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vsb.set)
        self.vsb.grid(row=0, column=1, sticky="NS")

        self.canvas.grid(row=0, column=0, sticky="NSEW")
        self.window = self.canvas.create_window(0,0, window=self.frame, anchor="nw", tags="self.frame")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.frame.bind("<Configure>", self.onFrameConfigure)

        self.checkbuttons = []
        self.checked = []

    def onFrameConfigure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def addCheck(self, recipe_name):
        var = tk.IntVar()
        self.checked.append(var)
        button = tk.Checkbutton(self.frame, text = recipe_name, variable = var,bg = "white")
        button.grid(sticky = "NSEW")
        self.checkbuttons.append(button)
        return

    def removeAll(self):
        self.checked.clear()
        [button.destroy() for button in self.checkbuttons]
        self.checkbuttons.clear()
        return

    def removeOption(self, index):
        recipe_name = self.checkbuttons[index].cget("text")
        del self.checked[index]
        self.checkbuttons[index].destroy()
        del self.checkbuttons[index]
        return recipe_name

class scrollingText(tk.Frame):
    def __init__(self, parentObject, height, width = 100):
        tk.Frame.__init__(self, parentObject, relief = "sunken", borderwidth = 1)
        self.text = tk.Text(self, borderwidth=0, wrap=None, state='disabled', highlightthickness=0, height = height, width = width)

        self.vsb = AutoScrollbar(self)
        self.text.configure(yscrollcommand=self.vsb.set)
        self.vsb.grid(row=0, column=1, sticky="NS")

        self.hsb = AutoScrollbar(self)
        self.text.configure(xscrollcommand=self.hsb.set)
        self.hsb.grid(row=1, column=0, sticky="EW")

        self.vsb.config(command=self.text.yview)
        self.hsb.config(command=self.text.xview)

        self.text.grid(row=0, column=0, sticky="NSEW")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

    def addText(self,string):
        self.text.config(state="normal")
        self.text.insert(tk.END,string + "\n")
        self.text.config(state="disabled")

    def addToText(self,strings):
        self.text.config(state="normal")
        self.text.insert(tk.END,self.text.index('end-1c').split('.')[0] + ". " + ", ".join(map(str,strings)) + "\n")
        self.text.config(state="disabled")

    def deleteAllText(self):
        self.text.config(state="normal")
        self.text.delete('1.0', tk.END)
        self.text.config(state="disabled")

class updatingListFrame(tk.Frame):
    def __init__(self, parentObject, h, bg, entriesTuple, name, addFunc):
        tk.Frame.__init__(self, parentObject)
        self.frame_left = tk.Frame(self,width = 325)
        self.frame_left.pack_propagate(0)

        self.name_frames = []
        self.name_labels = []
        self.entries = []

        for i, input in enumerate(entriesTuple):

            self.name_frames.append(tk.Frame(self.frame_left))
            self.name_frames[i].pack(side = "top",pady = 10,padx = 10,fill = "x")
            self.name_labels.append(tk.Label(self.name_frames[i],text = input + ":"))
            self.name_labels[i].pack(side = "left")
            
            if input is "Quantity":
                vcmd = (self.register(self.doValidate),'%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
                self.entries.append(tk.Entry(self.name_frames[i], validate = 'key', validatecommand = vcmd))
                self.entries[i].pack(side = "left")

                units = ["tsp","tbsp","oz","cups","pt","qt","gal","mL","L"]
                self.var = tk.StringVar(self.name_frames[i])
                self.var.set(units[0])
                self.quantity_unit = tk.OptionMenu(self.name_frames[i],self.var,*units)
                self.quantity_unit.pack(side = "left")
            else:
                self.entries.append(tk.Entry(self.name_frames[i]))
                self.entries[i].pack(side = "left")

            self.entries[i].bind('<Return>',lambda event, function = addFunc: self.eventHandler(event, function))

        self.add_button = tk.Button(self.frame_left, text = "Add " +name)#, command = lambda event: self.eventHandler(event,function))
        self.add_button.pack(side = "top", pady = 10)
        self.add_button.bind('<ButtonRelease>',lambda event, function = addFunc: self.eventHandler(event, function))

        self.frame_right = tk.Frame(self,borderwidth = 10)
        self.right_label = tk.Label(self.frame_right,text = name + "s:")
        self.right_label.grid(row = 0, column = 0, sticky = "NSEW")

        self.frame_right.grid_rowconfigure(0, weight=0)
        self.frame_right.grid_rowconfigure(1, weight=1)
        self.frame_right.grid_columnconfigure(0, weight=1)

        self.list_outer = scrollingText(self.frame_right,height = 10)
        self.list_outer.grid(row = 1, column = 0, sticky = "NSEW")

        self.grid_rowconfigure(0,weight = 1)
        self.grid_columnconfigure(0, weight = 0)
        self.grid_columnconfigure(1, weight = 1)
        self.frame_left.grid(row = 0, column = 0, sticky = "NSEW")
        self.frame_right.grid(row = 0, column = 1, sticky = "NSEW")

    def doValidate(self, d, i, P, s, S, v, V, W):
        if S in '.0123456789' and s.count('.') < 1:
            return True
        elif S in '0123456789':
            return True
        elif d == "0": ###action 0 = removing char
            return True
        else:
            return False

    def clearText(self):
        self.list_outer.deleteAllText()
        for entry in self.entries:
            entry.delete("0",tk.END)
        return

    def eventHandler(self, event, function):
        entriesList = []
        for entry in self.entries:
            value = entry.get()
            entry.delete("0",tk.END)
            if value == "":
                return
            else:
                entriesList.append(value)
        #self.list_outer.addToText(entriesList)

        function(entriesList)

class recipeFrame(tk.Frame):
    def __init__(self, GUI, parent):
        tk.Frame.__init__(self, parent,borderwidth = 10)
        self.parent = parent
        self.GUI = GUI
        self.pack()
        self.recipe_frame = tk.Frame(self,height = 100)
        #instructions_frame = tk.Frame(root,bg='white')
        self.instructions_frame = updatingListFrame(self, h = 200, bg = None, entriesTuple = ("Instruction",), name = "Instruction", addFunc = self.instructionEvent)

        self.ingredients_frame = updatingListFrame(self, h = 200, bg = None, entriesTuple = ("Ingredient","Quantity"), name = "Ingredient", addFunc = self.ingredientEvent)
        #ingredients_frame = tk.Frame(root,bg='green',relief="sunken",height = 200)
        self.add_recipe_frame = tk.Frame(self,height = 20)

        #first row cannot resize
        self.grid_columnconfigure(0,weight = 1) 
        self.grid_rowconfigure(0,weight = 0)
        self.grid_rowconfigure(1,weight = 1)
        self.grid_rowconfigure(2,weight = 1)
        self.grid_rowconfigure(3,weight = 0)

        #add frames to rows
        self.recipe_frame.grid(row = 0,column=0,sticky = "NSEW")
        self.instructions_frame.grid(row = 1,column=0,sticky = "NSEW")
        self.ingredients_frame.grid(row = 2,column=0,sticky = "NSEW")
        self.add_recipe_frame.grid(row = 3,column=0,sticky = "NSEW")

        #populate frames, first recipename
        self.add_recipe_label = tk.Label(self.recipe_frame,text = "Add Recipe")
        self.add_recipe_label.pack(side= "top")
        self.recipe_name_label = tk.Label(self.recipe_frame, text = "Recipe Name:").pack(side = "left")
        self.recipe_name_entry = tk.Entry(self.recipe_frame)
        self.recipe_name_entry.pack(side = "left")
        self.recipe_name_entry.bind('<Return>',self.recipeEvent)

        #add add_recipe button to bottom frame
        self.add_recipe_button = tk.Button(self.add_recipe_frame, text = 'Add Recipe')
        self.add_recipe_button.pack(side = "right",padx = 50, pady = 5)
        self.add_recipe_button.bind('<ButtonRelease>',self.recipeEvent)

        self.instructions = []
        self.ingredients = []
        self.quantities = []

    def instructionEvent(self,instruction):
        self.instructions.append(instruction[0])
        self.instructions_frame.list_outer.addToText(instruction)
        return

    def ingredientEvent(self,ingredient_quantity):#, owner):
        self.ingredients.append(ingredient_quantity[0])
        #store in database in mL
        self.quantities.append(unitConversion(float(ingredient_quantity[1]),self.ingredients_frame.var.get(),'mL'))
        self.ingredients_frame.list_outer.addToText([self.ingredients[-1],ingredient_quantity[1]+" "+self.ingredients_frame.var.get()])
        return

    def recipeEvent(self,event):
        if len(self.instructions) == 0 or len(self.ingredients) == 0:
            return
        if self.recipe_name_entry.get() == "":
            messagebox.showerror("Error","Recipe name not entered.")
            return
        recipe = Recipe(self.recipe_name_entry.get(),self.instructions,self.ingredients,self.quantities)
        if self.GUI.parent.addRecipe(recipe) != recipe:
            messagebox.showerror("Error","Recipe name already exists.")
            return
        self.clearFrame()
        return

    def clearFrame(self):
        self.instructions_frame.clearText()
        self.ingredients_frame.clearText()
        self.recipe_name_entry.delete("0",tk.END)
        del self.instructions[:]
        del self.ingredients[:]
        del self.quantities[:]
        return

class lookupFrame(tk.Frame):
    def __init__(self, GUI, parent):
        tk.Frame.__init__(self, parent,borderwidth = 10)
        self.parent = parent
        self.GUI = GUI

        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.label = tk.Label(self, text = "Search Recipes",height = 1)
        self.label.grid(row = 0, column = 0)

        self.keyword_frame = tk.Frame(self)
        self.result_frame = tk.Frame(self)
        
        self.recipe_frame = tk.Frame(self.keyword_frame)
        self.recipe_label = tk.Label(self.recipe_frame, text = "Search Recipe Names:")
        self.recipe_entry = tk.Entry(self.recipe_frame)
        self.recipe_entry.bind('<Return>',lambda event: self.searchRecipes(event))
        self.recipe_button = tk.Button(self.recipe_frame, text = "Search Names")
        self.recipe_button.bind('<ButtonRelease>',lambda event: self.searchRecipes(event))

        self.recipe_label.pack(side = "left")
        self.recipe_entry.pack(side = "left")
        self.recipe_button.pack(side = "left")
        self.recipe_frame.pack(side = "top")

        self.ingredient_frame = tk.Frame(self.keyword_frame)
        self.ingredient_label = tk.Label(self.ingredient_frame, text = "Search Ingredients:")
        self.ingredient_entry = tk.Entry(self.ingredient_frame)
        self.ingredient_entry.bind('<Return>',lambda event: self.searchIngredients(event))
        self.ingredient_button = tk.Button(self.ingredient_frame, text = "Search Ingredients")
        self.ingredient_button.bind('<ButtonRelease>',lambda event: self.searchIngredients(event))

        self.ingredient_label.pack(side = "left")
        self.ingredient_entry.pack(side = "left")
        self.ingredient_button.pack(side = "left")
        self.ingredient_frame.pack(side = "top")

        self.result_label = tk.Label(self.result_frame, text = "Results:")
        self.result_label.pack(side = "top")

        self.scroll_frame = scrollingText(self.result_frame, height = 20)
        #self.scroll_frame.addText("Recipe Results:")
        self.scroll_frame.pack(side = "top")

        self.keyword_frame.grid(row = 1, column = 0,sticky = "NSEW")
        self.result_frame.grid(row = 2, column = 0,sticky = "NSEW")

    def searchIngredients(self, event):
        self.scroll_frame.deleteAllText()
        ingredient_keyword = self.ingredient_entry.get()
        self.ingredient_entry.delete("0",tk.END)
        self.recipe_entry.delete("0",tk.END)
        if ingredient_keyword == "":
            return
        self.printResults(self.GUI.parent.ingredientKeywordSearch(ingredient_keyword))
        return

    def searchRecipes(self, event):
        self.scroll_frame.deleteAllText()
        recipe_keyword = self.recipe_entry.get()
        self.recipe_entry.delete("0",tk.END)
        self.ingredient_entry.delete("0",tk.END)
        if recipe_keyword == "":
            return
        self.printResults(self.GUI.parent.recipeKeywordSearch(recipe_keyword))
        return

    def printResults(self, results):
        #either list or single recipe or none
        print(results)
        if results is None or len(results) == 0:
            messagebox.showerror("Error","No results found.")
        else:
            if isinstance(results[0],Recipe) and len(results) == 1:
                #print onto text recipe
                self.scroll_frame.addText("{:<15}".format("Recipe Name:"))
                self.scroll_frame.addText("{:<50}".format(results[0].name))
                
                self.scroll_frame.addText("{:<15}".format("\nRequired Ingredients:"))
                for index, ingredient in enumerate(results[0].ingredients):
                    value, unit = bestValue(float(results[0].quantities[index]))
                    self.scroll_frame.addText("{:<25}{:<10.2f}{}".format(ingredient,value,unit))

                self.scroll_frame.addText("{:<15}".format("\nInstructions:"))
                for index, instruction in enumerate(results[0].instructions):
                    self.scroll_frame.addText("{}. {}".format(index+1,instruction[0]))

            else:
                #print only names of recipes
                self.scroll_frame.addText("{:<15}".format("Names of possible recipes:"))
                for result in results:
                    self.scroll_frame.addText("{}".format(result))
        return

    def clearFrame(self):
        self.recipe_entry.delete("0",tk.END)
        self.ingredient_entry.delete("0",tk.END)
        self.scroll_frame.deleteAllText()

class deleteFrame(tk.Frame):
    def __init__(self, GUI, parent):
        tk.Frame.__init__(self, parent,borderwidth = 10)
        self.parent = parent
        self.GUI = GUI
        
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.label = tk.Label(self, text = "Delete Recipes",height = 1)
        self.label.grid(row = 0, column = 0)

        self.keyword_frame = tk.Frame(self)
        
        self.recipe_name_frame = tk.Frame(self.keyword_frame)
        self.recipe_name_label = tk.Label(self.recipe_name_frame, text = "Search Recipe Names:")
        self.recipe_name_entry = tk.Entry(self.recipe_name_frame)
        self.recipe_name_entry.bind('<Return>',lambda event: self.deleteRecipe(event))
        self.recipe_name_button = tk.Button(self.recipe_name_frame, text = "Search Names")
        self.recipe_name_button.bind('<ButtonRelease>',lambda event: self.deleteRecipe(event))

        self.recipe_name_label.pack(side = "left")
        self.recipe_name_entry.pack(side = "left")
        self.recipe_name_button.pack(side = "left")
        self.recipe_name_frame.pack(side = "top")

        self.keyword_frame.grid(row = 1, column = 0,sticky = "NSEW")


    def deleteRecipe(self, event):
        recipe_keyword = self.recipe_name_entry.get()
        self.recipe_name_entry.delete("0",tk.END)
        result = self.GUI.parent.deleteRecipe(recipe_keyword)

        message = ""
        if result is None:
            message = "Recipe not found."
        else:
            message = "Recipe deleted."
        
        messagebox.showinfo("Result", message)
        return

    def clearFrame(self):
        self.recipe_name_entry.delete("0",tk.END)
        return

class groceriesFrame(tk.Frame):
    def __init__(self, GUI, parent):
        tk.Frame.__init__(self, parent,borderwidth = 10)
        self.parent = parent
        self.GUI = GUI
        self.label = tk.Label(self, text = "Grocery List", height = 1)
        self.label.grid(row = 0, column = 0)

        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=0)
        self.grid_columnconfigure(0, weight=1)

        self.keyword_frame = tk.Frame(self)

        self.recipe_name_frame = tk.Frame(self.keyword_frame)
        self.recipe_name_label = tk.Label(self.recipe_name_frame, text = "Add Recipe:")
        self.recipe_name_entry = tk.Entry(self.recipe_name_frame)
        self.recipe_name_entry.bind('<Return>',lambda event: self.addRecipes(event))
        self.recipe_name_button = tk.Button(self.recipe_name_frame, text = "Add")
        self.recipe_name_button.bind('<ButtonRelease>',lambda event: self.addRecipes(event))

        self.recipe_name_label.pack(side = "left")
        self.recipe_name_entry.pack(side = "left")
        self.recipe_name_button.pack(side = "left")
        self.recipe_name_frame.pack(side = "top")

        self.keyword_frame.grid(row = 1, column = 0,sticky = "NSEW")

        self.middle_frame = tk.Frame(self)
        self.middle_frame.grid_rowconfigure(0,weight = 1)
        self.middle_frame.grid_columnconfigure(0,weight = 1)
        self.middle_frame.grid_columnconfigure(1,weight = 0)
        self.middle_frame.grid(row = 2, column = 0, sticky = "NSEW")

        self.textbox_frame = tk.Frame(self.middle_frame,pady = 10)
        #self.textbox_frame.pack_propagate(0)
        self.textbox_frame.grid(row = 0, column = 0, sticky = "NSEW")

        self.textbox_label = tk.Label(self.textbox_frame,text = "Added:")
        self.textbox_label.pack(side = "top")
        self.scroll_frame = scrollingFrame(self.textbox_frame, height = 500, width = 500)
        self.scroll_frame.pack(side = "top")

        self.delete_frame = tk.Frame(self.middle_frame, pady = 10)
        self.delete_frame.grid(row = 0, column = 1, sticky = "NSEW")

        self.delete_button = tk.Button(self.delete_frame, text = "Remove Selected")
        self.delete_button.bind('<ButtonRelease>', self.removeSeleted)
        self.delete_button.pack(side = "top")

        self.clear_button = tk.Button(self.delete_frame, text = "Clear All")
        self.clear_button.bind('<ButtonRelease>', self.clearAll)
        self.clear_button.pack(side = "top")

        self.save_frame = tk.Frame(self)
        self.save_frame.grid(row = 3, column = 0, sticky = "NSEW")
        self.save_button = tk.Button(self.save_frame, text = "Save Grocery List")
        self.save_button.pack(side = "right",padx = 5, pady = 5)
        self.save_button.bind('<ButtonRelease>',self.saveGroceryList)

        self.recipes = {}

    def addRecipes(self, event):
        result = self.GUI.parent.getRecipe(self.recipe_name_entry.get())
        if result is None:
            messagebox.showerror("Error", "Recipe not found.")
            return
        recipe = result[0]

        if recipe.name not in self.recipes:
            self.recipes[recipe.name] = recipe

        self.recipes[recipe.name].occurrences += 1
        self.scroll_frame.addCheck(recipe.name)
        
        return

    def removeSeleted(self, event):
        length = len(self.scroll_frame.checked)
        index = 0
        while (index < len(self.scroll_frame.checked)):
            if self.scroll_frame.checked[index].get() == 1:
                recipe_name = self.scroll_frame.removeOption(index)
                if self.recipes[recipe_name].occurrences <= 1:
                    del self.recipes[recipe_name]
                else:
                    self.recipes[recipe_name].occurrences -= 1
                index -= 1
            index += 1
        return

    def clearAll(self, event):
        self.scroll_frame.removeAll()
        self.recipes.clear()
        return

    def saveGroceryList(self, event):
        file = filedialog.asksaveasfile(mode='w', defaultextension=".txt")
        if file is None:
            return

        grocery_list = str()
        g_list = dict()

        for recipe_name in self.recipes.keys():
            recipe = self.recipes[recipe_name]

            for index, ingredient in enumerate(recipe.ingredients):
                if ingredient in g_list:
                    g_list[ingredient] += (float(recipe.quantities[index]) * recipe.occurrences)
                else:
                    g_list[ingredient] = (float(recipe.quantities[index]) * recipe.occurrences)

        for pair in g_list.items():
            value = bestValue(pair[1])
            grocery_list += (str(pair[0]) + ", " + '{:.2f}'.format(value[0]) + " " + str(value[1]) + "\n")


        file.write(grocery_list)
        file.close()
        self.scroll_frame.removeAll()
        self.recipes.clear()
        self.recipe_name_entry.delete("0",tk.END)
        return

    def clearFrame(self):
        return

class GUI(tk.Tk):
    def __init__(self,parent):
        tk.Tk.__init__(self)
        self.parent = parent
        self.title('Cookbook')
        self.geometry('{}x{}'.format(700,520))
        self.grid()

        self.main_frame = tk.Frame(self)
        self.main_frame.pack()
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)

        self.menu = tk.Menu(self)
        self.config(menu = self.menu)

        self.cookbook_menu = tk.Menu(self.menu,tearoff=0)
        self.cookbook_menu.add_command(label = "Open Cookbook", command = lambda: self.openRecipeFile())
        self.cookbook_menu.add_command(label = "Export JSON recipes", command = lambda: self.saveRecipes())
        self.cookbook_menu.add_command(label = "Import JSON recipes", command = lambda: self.openJSONRecipes())
        
        self.menu.add_cascade(label = "File", menu = self.cookbook_menu)
        self.menu.add_command(label = "Add Recipe", command = lambda: self.show_frame("recipeFrame"))
        self.menu.add_command(label = "Search Recipes",command = lambda: self.show_frame("lookupFrame"))
        self.menu.add_command(label = "Delete Recipe",command = lambda: self.show_frame("deleteFrame"))
        self.menu.add_command(label = "Create Grocery List",command = lambda: self.show_frame("groceriesFrame"))

        self.frames = {}

        for fra in (recipeFrame, lookupFrame, deleteFrame, groceriesFrame):
            frame_name = fra.__name__
            frame = fra(self,self.main_frame)
            self.frames[frame_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        
        self.show_frame("recipeFrame")

        # self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.mainloop()

    def clear_frames(self):
        for key in self.frames:
            self.frames[key].clearFrame()
        return

    def show_frame(self, frame_name):
        frame = self.frames[frame_name]
        frame.tkraise()

        self.frames[frame_name].clearFrame()

    def saveRecipes(self):
        self.clear_frames()

        fileName = filedialog.asksaveasfile(mode='w', defaultextension=".JSON")

        if not fileName:
            return
        else:
            self.parent.writeRecipeFile(fileName)
        return

    def openRecipeFile(self):
        self.clear_frames()

        ftypes = [('Database files','*.db')]
        fileName = filedialog.askopenfilename(filetypes = ftypes)


        if fileName is None or type(fileName) is not str:
            return
        elif os.path.splitext(fileName)[1] == '.db':
            self.parent.switchDatabase(fileName)

        return

    def openJSONRecipes(self):
        ftypes = [('JSON files', '*.JSON')]
        fileName = filedialog.askopenfilename(filetypes = ftypes)

        if fileName is None or fileName == ():
            return
        elif os.path.splitext(fileName)[1] == '.JSON':
            self.parent.readRecipeFile(fileName)

        return

    # def on_closing(self):
    #     if messagebox.askokcancel("Quit", "Do you want to quit?"):
            
    #         self.destroy()
