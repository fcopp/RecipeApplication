import tkinter as tk


if __name__ == '__main__':
   root = tk.Tk()
   root.title('Add Recipe')
   root.geometry('{}x{}'.format(700,520))
   root.configure(bg = 'red')
   root.grid()

   #create the 4 row frames
   recipe_frame = tk.Frame(root,bg='cyan',height = 100,borderwidth = 5)
   instructions_frame = tk.Frame(root,bg='white',height = 200)
   ingredients_frame = tk.Frame(root,bg='green',height = 200)
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

   #next instruction frame
   instructions_frame_left = tk.Frame(instructions_frame, bg = 'red',width = 500,height = 200)
   instructions_name_frame = tk.Frame(instructions_frame_left, width = 500)
   instructions_name_frame.pack(side = "top",pady = 10)
   instruction_name_label = tk.Label(instructions_name_frame, text = 'Instruction:') #cannot make sizes bigger, pack overrides?
   instruction_name_label.pack(side = "left")
   instruction_name_entry = tk.Entry(instructions_name_frame)
   instruction_name_entry.pack(side = "left")
   instruction_add_button = tk.Button(instructions_frame_left, text = 'Add Instruction').pack(side = "top",pady = 10)

   #right side
   instructions_frame_right = tk.Frame(instructions_frame, bg = 'blue',width = 200,height = 200)
   

   instructions_frame.grid_rowconfigure(0,weight = 1)
   instructions_frame.grid_columnconfigure(0, weight = 0)
   instructions_frame.grid_columnconfigure(1, weight = 1)
   instructions_frame_left.grid(row = 0, column = 0, sticky = "NSEW")
   instructions_frame_right.grid(row = 0, column = 1, sticky = "NSEW")

   #add add_recipe button to bottom frame
   add_recipe_button = tk.Button(add_recipe_frame, text = 'Add Recipe')
   add_recipe_button.pack(side = "right",padx = 50, pady = 5)
   root.mainloop()