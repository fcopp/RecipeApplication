import tkinter

# function that is called when you select a certain radio button
def selected():
    print(var.get())


root = tkinter.Tk()

var = tkinter.StringVar() #used to get the 'value' property of a tkinter.Radiobutton

# Note that I added a command to each radio button and a different 'value'
# When you press a radio button, its corresponding 'command' is called.
# In this case, I am linking both radio buttons to the same command: 'selected'

rb1 = tkinter.Radiobutton(text='Radio Button 1', variable=var, 
                          value=1, command=selected)
rb1.pack()
rb2 = tkinter.Radiobutton(text='Radio Button 2', variable=var, 
                          value=2, command=selected)
rb2.pack()

root.mainloop()