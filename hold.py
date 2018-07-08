import tkinter as tk

class AutoScrollbar(tk.Scrollbar):
    def set(self, lo, hi):
        if float(lo) <= 0.0 and float(hi) >= 1.0:
            self.tk.call("grid", "remove", self)
        else:
            self.grid()
        tk.Scrollbar.set(self, lo, hi)

class scrollingFrame(tk.Frame):
    def __init__(self, parentObject, background):
        tk.Frame.__init__(self, parentObject, relief = "sunken", borderwidth = 1, background = background)
        self.text = tk.Text(self, borderwidth=0, wrap=None,background = background, highlightthickness=0,height = 1000)
        # self.frame = tk.Frame(self.canvas, background = background)

        self.vsb = AutoScrollbar(self)#tk.Scrollbar(self, orient="vertical", command=self.text.yview, background=background)
        self.text.configure(yscrollcommand=self.vsb.set)
        self.vsb.grid(row=0, column=1, sticky="NS")

        self.hsb = AutoScrollbar(self)#tk.Scrollbar(self, orient="horizontal", command=self.text.xview, background=background)
        self.text.configure(xscrollcommand=self.hsb.set)
        self.hsb.grid(row=1, column=0, sticky="EW")

        self.vsb.config(command=self.text.yview)
        self.hsb.config(command=self.text.xview)

        self.text.grid(row=0, column=0, sticky="NSEW")
        # self.window = self.canvas.create_window(0,0, window=self.frame, anchor="nw", tags="self.frame")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

    def addToText(self,strings):
        self.text.insert(tk.END,", ".join(map(str,strings)) + "\n")

    def deleteAllText(self):
        self.text.delete('1.0', END)

class updatingListFrame(tk.Frame):
    def __init__(self, parentObject, h, bg, entriesTuple, name, addFunc):
        tk.Frame.__init__(self, parentObject,bg=bg)
        self.frame_left = tk.Frame(self, bg = 'red',width = 250)
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
            # self.entries[i].bind('<Return>', lambda text = [entry.get() for entry in self.entries], owner = self: addFunc)
            self.entries[i].bind('<KeyRelease-Return>',lambda event, function = addFunc: self.eventHandler(event, function))

        self.add_button = tk.Button(self.frame_left, text = "Add " +name)#, command = lambda event: self.eventHandler(event,function))
        self.add_button.pack(side = "top", pady = 10)
        self.add_button.bind('<ButtonRelease>',lambda event, function = addFunc: self.eventHandler(event, function))

        self.frame_right = tk.Frame(self, bg = 'purple')
        self.right_label = tk.Label(self.frame_right,text = name + "s:")
        self.right_label.grid(row = 0, column = 0, sticky = "NSEW")

        self.frame_right.grid_rowconfigure(0, weight=0)
        self.frame_right.grid_rowconfigure(1, weight=1)
        self.frame_right.grid_columnconfigure(0, weight=1)

        self.list_outer = scrollingFrame(self.frame_right,background = "cyan")
        self.list_outer.grid(row = 1, column = 0, sticky = "NSEW")

        self.grid_rowconfigure(0,weight = 1)
        self.grid_columnconfigure(0, weight = 0)
        self.grid_columnconfigure(1, weight = 1)
        self.frame_left.grid(row = 0, column = 0, sticky = "NSEW")
        self.frame_right.grid(row = 0, column = 1, sticky = "NSEW")

    def eventHandler(self, event, function):
        entriesList = [entry.get() for entry in self.entries]
        self.list_outer.addToText(entriesList)
        function(entriesList)


def instructionEvent(instruction):
    print("instruction: ")
    print(instruction)
    return

def ingredientEvent(ingredient_quantity):#, owner):
    print("ingredient: ")
    print(ingredient_quantity)
    return

def recipeEvent(event):
    print("recipe")
    return




if __name__ == '__main__':
    root = tk.Tk()
    root.title('Add Recipe')
    root.geometry('{}x{}'.format(700,520))
    root.configure(bg = 'red')
    root.grid()

    frame = tk.Frame(root)
    frame.pack()

    #create the 4 row frames
    recipe_frame = tk.Frame(frame,bg='cyan',height = 100,borderwidth = 5)
    #instructions_frame = tk.Frame(root,bg='white')
    instructions_frame = updatingListFrame(frame, h = 200, bg = 'white', entriesTuple = ("Instruction",), name = "Instruction", addFunc = instructionEvent)

    ingredients_frame = updatingListFrame(frame, h = 200, bg = 'white', entriesTuple = ("Ingredient","Quantity"), name = "Ingredient", addFunc = ingredientEvent)
    #ingredients_frame = tk.Frame(root,bg='green',relief="sunken",height = 200)
    add_recipe_frame = tk.Frame(frame,bg='blue',height = 20)

    #first row cannot resize
    frame.grid_columnconfigure(0,weight = 1) 
    frame.grid_rowconfigure(0,weight = 0)
    frame.grid_rowconfigure(1,weight = 1)
    frame.grid_rowconfigure(2,weight = 1)
    frame.grid_rowconfigure(3,weight = 0)

    #add frames to rows
    recipe_frame.grid(row = 0,column=0,sticky = "NSEW")
    instructions_frame.grid(row = 1,column=0,sticky = "NSEW")
    ingredients_frame.grid(row = 2,column=0,sticky = "NSEW")
    add_recipe_frame.grid(row = 3,column=0,sticky = "NSEW")


    #populate frames, first recipename
    recipe_name_label = tk.Label(recipe_frame, text = "Recipe Name:").pack(side = "left")
    recipe_name_entry = tk.Entry(recipe_frame)
    recipe_name_entry.pack(side = "left")
    recipe_name_entry.bind('<Return>',recipeEvent)

    #add add_recipe button to bottom frame
    add_recipe_button = tk.Button(add_recipe_frame, text = 'Add Recipe')
    add_recipe_button.pack(side = "right",padx = 50, pady = 5)
    add_recipe_button.bind('<Button-1>',recipeEvent)
    root.mainloop()