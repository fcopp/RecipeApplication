import tkinter as tk

class Q_and_A(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master, borderwidth=1, relief="sunken")
        self.label = tk.Label(self)
        self.results_txtbx = tk.Text(self, width=20, height=4, wrap="none",
                                     borderwidth=0, highlightthickness=0)
        self.results_scrbr = tk.Scrollbar(self, orient="vertical", 
                                          command=self.results_txtbx.yview)
        self.results_txtbx.configure(yscrollcommand=self.results_scrbr.set)

        self.label.grid(row=1, columnspan=2)
        self.results_scrbr.grid(row=0, column=1, sticky="ns")
        self.results_txtbx.grid(row=0, column=0, sticky="nsew")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

root = tk.Tk()
root.wm_title("Question And Answer")

app = Q_and_A(root)
app.pack(side="top", fill="both", expand=True)
root.mainloop()