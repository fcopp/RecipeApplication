import tkinter as tk
from tkinter import messagebox
import recipe as Recipe

class AutoScrollbar(tk.Scrollbar):
    def set(self, lo, hi):
        if float(lo) <= 0.0 and float(hi) >= 1.0:
            self.tk.call("grid", "remove", self)
        else:
            self.grid()
        tk.Scrollbar.set(self, lo, hi)

class scrollingFrame(tk.Frame):
    def __init__(self, parentObject, height):
        tk.Frame.__init__(self, parentObject, relief = "sunken", borderwidth = 1)
        self.text = tk.Text(self, borderwidth=0, wrap=None, state='disabled', highlightthickness=0, height = height, width = 100)

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
        self.frame_left = tk.Frame(self,width = 250)
        self.frame_left.pack_propagate(0)

        self.name_frames = []
        self.name_labels = []
        self.entries = []

        for i, input in enumerate(entriesTuple):

            self.name_frames.append(tk.Frame(self.frame_left))
            self.name_frames[i].pack(side = "top",pady = 10,padx = 10,fill = "x")
            self.name_labels.append(tk.Label(self.name_frames[i],text = input + ":"))
            self.name_labels[i].pack(side = "left")
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

        self.list_outer = scrollingFrame(self.frame_right,height = 10)
        self.list_outer.grid(row = 1, column = 0, sticky = "NSEW")

        self.grid_rowconfigure(0,weight = 1)
        self.grid_columnconfigure(0, weight = 0)
        self.grid_columnconfigure(1, weight = 1)
        self.frame_left.grid(row = 0, column = 0, sticky = "NSEW")
        self.frame_right.grid(row = 0, column = 1, sticky = "NSEW")

    def clearText(self):
        self.list_outer.deleteAllText()
        for entry in self.entries:
            entry.delete("0",tk.END)
        return

    def eventHandler(self, event, function):
        entriesList = [entry.get() for entry in self.entries]
        self.list_outer.addToText(entriesList)
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
        return

    def ingredientEvent(self,ingredient_quantity):#, owner):
        self.ingredients.append(ingredient_quantity[0])
        self.quantities.append(ingredient_quantity[1])
        return

    def recipeEvent(self,event):
        recipe = Recipe.Recipe(self.recipe_name_entry.get(),self.instructions,self.ingredients,self.quantities)
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

        self.scroll_frame = scrollingFrame(self.result_frame, height = 20)
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
            if isinstance(results[0],Recipe.Recipe) and len(results) == 1:
                #print onto text recipe
                self.scroll_frame.addText("{:<15}".format("Recipe Name:"))
                self.scroll_frame.addText("{:<50}".format(results[0].name))
                
                self.scroll_frame.addText("{:<15}".format("\nRequired Ingredients:"))
                for index, ingredient in enumerate(results[0].ingredients):
                    self.scroll_frame.addText("{:<25}{:<10}".format(ingredient,str(results[0].quantities[index])))

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
        self.label = tk.Label(self, text = "groceriesFrame")
        self.label.pack()
    
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

    def show_frame(self, frame_name):
        frame = self.frames[frame_name]
        frame.tkraise()

        self.frames[frame_name].clearFrame()


    # def on_closing(self):
    #     if messagebox.askokcancel("Quit", "Do you want to quit?"):
            
    #         self.destroy()
