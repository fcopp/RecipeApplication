import tkinter as tk


class scrollingFrame(tk.Frame):
    def __init__(self, parentObject, background):
        tk.Frame.__init__(self, parentObject, relief = "sunken", borderwidth = 1, background = background)
        self.canvas = tk.Canvas(self, borderwidth=0, background = background, highlightthickness=0)
        self.frame = tk.Frame(self.canvas, background = background)

        self.vsb = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview, background=background)
        self.canvas.configure(yscrollcommand=self.vsb.set)
        self.vsb.grid(row=0, column=1, sticky="NS")

        self.hsb = tk.Scrollbar(self, orient="horizontal", command=self.canvas.xview, background=background)
        self.canvas.configure(xscrollcommand=self.hsb.set)
        self.hsb.grid(row=1, column=0, sticky="EW")

        self.canvas.grid(row=0, column=0, sticky="NSEW")
        self.window = self.canvas.create_window(0,0, window=self.frame, anchor="nw", tags="self.frame")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.frame.bind("<Configure>", self.onFrameConfigure)
        self.canvas.bind("<Configure>", self.onCanvasConfigure)


    def onFrameConfigure(self, event):
        #Reset the scroll region to encompass the inner frame
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))


    def onCanvasConfigure(self, event):
        #Resize the inner frame to match the canvas
        minWidth = self.frame.winfo_reqwidth()
        minHeight = self.frame.winfo_reqheight()

        if self.winfo_width() >= minWidth:
            newWidth = self.winfo_width()
            #Hide the scrollbar when not needed
            self.hsb.grid_remove()
        else:
            newWidth = minWidth
            #Show the scrollbar when needed
            self.hsb.grid()

        if self.winfo_height() >= minHeight:
            newHeight = self.winfo_height()
            #Hide the scrollbar when not needed
            self.vsb.grid_remove()
        else:
            newHeight = minHeight
            #Show the scrollbar when needed
            self.vsb.grid()

        self.canvas.itemconfig(self.window, width=newWidth, height=newHeight)


def scroll(event):
    canvas.configure(scrollregion=canvas.bbox("all"))#,height = 225)


if __name__ == '__main__':
    root = tk.Tk()
    root.title('Add Recipe')
    root.geometry('{}x{}'.format(700,520))
    root.configure(bg = 'red')
    root.grid()

    #create the 4 row frames
    recipe_frame = tk.Frame(root,bg='cyan',height = 100,borderwidth = 5)
    instructions_frame = tk.Frame(root,bg='white',height = 200)
    ingredients_frame = tk.Frame(root,bg='green',relief="sunken",height = 200)
    add_recipe_frame = tk.Frame(root,bg='blue',height = 20)

    #first row cannot resize
    root.grid_columnconfigure(0,weight = 1) 
    root.grid_rowconfigure(0,weight = 0)
    root.grid_rowconfigure(1,weight = 1)
    root.grid_rowconfigure(2,weight = 1)
    root.grid_rowconfigure(3,weight = 0)

    #add frames to rows
    recipe_frame.grid(row = 0,column=0,sticky = "NSEW")
    instructions_frame.grid(row = 1,column=0,sticky = "NSEW")
    ingredients_frame.grid(row = 2,column=0,sticky = "NSEW")
    add_recipe_frame.grid(row = 3,column=0,sticky = "NSEW")


    #populate frames, first recipename
    recipe_name_label = tk.Label(recipe_frame, text = "Recipe Name:").pack(side = "left")
    recipe_name_entry = tk.Entry(recipe_frame).pack(side = "left")

    #next, instruction frame
    instructions_frame_left = tk.Frame(instructions_frame, bg = 'red',width = 500)#,height = 200)
    instructions_name_frame = tk.Frame(instructions_frame_left)
    instructions_name_frame.pack(side = "top",pady = 10,padx = 10,fill = "x")
    instruction_name_label = tk.Label(instructions_name_frame, text = 'Instruction:') #cannot make sizes bigger, pack overrides?
    instruction_name_label.pack(side = "left")
    instruction_name_entry = tk.Entry(instructions_name_frame)
    instruction_name_entry.pack(side = "left")
    instruction_add_button = tk.Button(instructions_frame_left, text = 'Add Instruction').pack(side = "top",pady = 10)

    #right side
    instructions_frame_right = tk.Frame(instructions_frame, bg = 'purple')
    instruction_right_label = tk.Label(instructions_frame_right,text = 'Instructions:')
    instruction_right_label.grid(row = 0, column = 0, sticky = "NSEW")

    instructions_frame_right.grid_rowconfigure(0, weight=0)
    instructions_frame_right.grid_rowconfigure(1, weight=1)
    instructions_frame_right.grid_columnconfigure(0, weight=1)

    instruction_list_outer = scrollingFrame(instructions_frame_right,background = "cyan")
    instruction_list_outer.grid(row = 1, column = 0, sticky = "NSEW")
    # instruction_list_outer = tk.Frame(instructions_frame_right, relief="sunken", borderwidth = 1)
    

    # canvas = tk.Canvas(instruction_list_outer)
    # instruction_list_inner = tk.Frame(canvas)
    # vsb = tk.Scrollbar(instruction_list_outer,orient = "vertical", command = canvas.yview)
    # canvas.configure(yscrollcommand = vsb.set)

    # vsb.pack(side="right", fill="y")
    # canvas.pack(side="left", fill="both", expand=True)
    # canvas.create_window((0,0),window=instruction_list_inner,anchor='nw')
    # instruction_list_inner.bind("<Configure>",scroll)

    for i in range(50):
        label = tk.Label(instruction_list_outer.frame,text=i).pack(side = "top")
        

    # instruction_list_outer.pack(side = "top",fill = "both")


    instructions_frame.grid_rowconfigure(0,weight = 1)
    instructions_frame.grid_columnconfigure(0, weight = 0)
    instructions_frame.grid_columnconfigure(1, weight = 1)
    instructions_frame_left.grid(row = 0, column = 0, sticky = "NSEW")
    instructions_frame_right.grid(row = 0, column = 1, sticky = "NSEW")

    #add add_recipe button to bottom frame
    add_recipe_button = tk.Button(add_recipe_frame, text = 'Add Recipe')
    add_recipe_button.pack(side = "right",padx = 50, pady = 5)
    root.mainloop()

