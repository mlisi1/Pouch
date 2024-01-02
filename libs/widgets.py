import tkinter as tk
from tkinter import ttk

from PIL import Image, ImageTk





class Categories(ttk.LabelFrame):

    def __init__(self, container):

        super().__init__(container, text="Categories:")

        self.scrollbar = ttk.Scrollbar(self)
        self.entry = ttk.Treeview(self, yscrollcommand=self.scrollbar.set, show="tree", height=10)        
        self.scrollbar.configure(command=self.entry.yview)

        self.scrollbar.pack(side="right", fill="y", pady=10, padx = (0, 10))
        self.entry.pack(side="left", fill="y", expand=True, padx=(10,0), pady =10)

        self.entry.bind("<<TreeviewSelect>>", self.on_select)

        self.selection = None
        self.changed = False

    def init_entries(self, sheets):

        for key in sheets.keys():

            self.entry.insert("", "end", text=key)

    def on_select(self, _):

        selected = self.entry.item(self.entry.selection()[0], 'text')


        if not self.selection == selected:

            self.selection = selected
            self.changed = True
         




class InfoBase(ttk.LabelFrame):

    def __init__(self, root, label, data):

        super().__init__(root, text=label)

        self.entries = EntriesSection(self, data)
        self.entries.grid(row=0, column=0, padx = 10, sticky='nw')

        self.hor_separator = ttk.Separator(self, orient=tk.HORIZONTAL)
        self.hor_separator.grid(row=1, column=0, columnspan=3, sticky = 'ew', pady=5, padx=10)

        self.details = DetailsSection(self, list(data.keys()), data)
        self.details.grid(row=2, column=0, sticky = 'nw', padx = 10, columnspan=3)

        self.ver_separator = ttk.Separator(self, orient=tk.VERTICAL)
        self.ver_separator.grid(row=0, column=1, padx=2, sticky='ns', pady = 10)

        self.image = ImageSection(self)
        self.image.grid(row=0, column=2, sticky = 'nw', padx = 10)

        self.entries.update_entries()

        self.image_handler = None




class EntriesSection(ttk.Frame):

    def __init__(self, root, data):

        super().__init__(root)

        self.data = data
        self.data_keys = list(data.keys())
        self.parent = root

        self.components_label = ttk.Label(self, text="Entries:")
        self.components_label.grid(row=0, column=0, sticky='w', pady=(5, 3))

        self.paned = ttk.PanedWindow(self)
        self.paned.grid(row=1, column=0)

        self.pane_1 = ttk.Frame(self.paned, padding=5)
        self.paned.add(self.pane_1, weight=1)

        self.scrollbar = ttk.Scrollbar(self.pane_1)
        self.scrollbar.pack(side="right", fill="y")

        self.entries_widget = ttk.Treeview(
            self.pane_1,
            selectmode="browse",
            yscrollcommand=self.scrollbar.set,
            columns=(0, 1),
            height=9,
            show='headings'
        )
        self.entries_widget.pack(expand=True, fill="both")
        self.scrollbar.config(command=self.entries_widget.yview)

        self.entries_widget.heading(0, text=self.data_keys[0], anchor='w')
        self.entries_widget.heading(1, text="Quantity", anchor='w')

        self.entries_widget.column(1, width=80)
        
        self.selection = None
        self.changed = False
        self.entries_widget.bind("<<TreeviewSelect>>", self.on_select)
        # self.entries_widget.column(1, anchor="w", width=60)


    def update_entries(self):

        keys = [key for key in self.data.keys()]

        for i in range(len(self.data[keys[0]])):

            entry = (str(self.data[keys[0]][i]), str(self.data["Quantity"][i]))

            self.entries_widget.insert("", 'end', values=entry)


    def on_select(self, _):

        selected = self.entries_widget.item(self.entries_widget.selection()[0], 'values')[0]

        if not self.selection == selected:

            self.selection = selected
            self.changed = True

            if not self.parent.image_handler == None:

                self.parent.image_handler.handle_selection(selected)



class DetailsSection(ttk.Frame):

    def __init__(self, root, keys, data):

        super().__init__(root)
        self.label_keys = keys
        self.data = data
        self.label = ttk.Label(self, text="Details:")
        self.label.grid(row=0, column=0, pady=5)

        self.details_label = []
        self.values_label = []

        self.vars = []

        self.init_labels()



    def init_labels(self):

        for i, key in enumerate(self.label_keys):

            if key == "Image":
                break

            self.details_label.append(ttk.Label(self, text=(key+':')))
            self.details_label[i].grid(row=1, column=i*2, padx = (10, 5), sticky = 'w', pady = (10, 20))

            self.vars.append(tk.StringVar())
            self.vars[i].set("")

            self.values_label.append(ttk.Label(self, textvariable=self.vars[i]))
            self.values_label[i].grid(row=1, column=(2*i+1), padx = (0, 10), sticky = 'w', pady = (10, 20))         




    def update_details(self, name):

        index = self.data[self.label_keys[0]].index(name)

        for i, key in enumerate(self.label_keys):

            if key == "Image":
                break

            self.vars[i].set(self.data[key][index])
     

        







class ImageSection(ttk.Frame):

    def __init__(self, root):

        super().__init__(root)
        self.label = ttk.Label(self, text="Image:")
        self.label.grid(row=0, column=0, sticky = 'nw', pady = (5,3))

        
        


        self.blank = ImageTk.PhotoImage(Image.open(r'res/blank.jpg'))
        self.canvas = tk.Label(self, image=self.blank)

        # self.canvas.image = self.blank  
        # self.canvas.configure(image=self.blank)

        # self.container = self.canvas.create_image(0, 0, image = blank, anchor = 'w')
        # self.canvas.itemconfig(self.container, anchor='nw')
        self.canvas.grid(row=2, column=0, padx=10, pady=10)
     

        # self.canvas.bind("<Configure>", self.draw_canvas)

    def draw_canvas(self, event):
        # Update the canvas size and redraw the image when the canvas is resized
        
        self.canvas.itemconfig(self.container, anchor='nw')




class SearchBox(ttk.LabelFrame):

    def __init__(self, root):

        super().__init__(root, text="Search components:")

        self.entry = ttk.Entry(self, width=26)
        self.entry.pack(padx = 30, pady = 5)

        self.button = ttk.Button(self, text="Search")
        self.button.pack(pady = (5, 10))



class ComponentManager(ttk.LabelFrame):

    def __init__(self, root, sheet):

        super().__init__(root, text="Manage Components", height = 200)
        
        self.add_button = ttk.Button(self, text="Add Component", command=self.create_entries)
        self.add_button.grid(row=0, column=0, padx=(50, 10), pady=10)

        self.entries = ComponentEntries(self)
        self.rowconfigure(2, weight=1)
        self.entries.grid(row=2, column=0, columnspan=5, sticky = 'nw')

        spacer = tk.Canvas(self, height = 200, width = 1)
        
        spacer.grid(row=2, column=0, columnspan=5, sticky = 'w', in_=self)
      
        

    
 

        self.categories = list(sheet.keys())
        self.sheets = sheet
        self.category_var = tk.StringVar()
        self.category_var.set(self.categories[0])

        self.cat_label = ttk.Label(self, text="Choose a category:")
        self.cat_label.grid(row=0, column=1, padx=(50,5), pady = 10)
        self.category_select = ttk.OptionMenu(self, self.category_var, *self.categories, command=self.entries.remove_entries)
        self.category_select.grid(row=0, column=2, pady = 10, padx = (5, 213))
        self.category_select.config(width=20)

        sep = ttk.Separator(self)
        sep.grid(row = 0, column=3, sticky="ns", padx=5, pady = (5, 10))

        self.add_category = ttk.Button(self, text="Add category")
        self.add_category.grid(row = 0, column=4, padx = (50, 30))

        sep = ttk.Separator(self, orient=tk.HORIZONTAL)
        sep.grid(row=1, column=0, columnspan=5, sticky='ew', padx = 5, pady = 5)

        


    def create_entries(self):

        fields = self.sheets[self.category_var.get()].keys()

        self.entries.create_fields(fields)



class ComponentEntries(ttk.Frame):

    def __init__(self, root):

        super().__init__(root)
        self.labels = []
        self.entries = []
        self.add = ttk.Button(root, text="Add")


    def create_fields(self, fields):

        if len(self.entries) == 0:

            j = 0

            for i, field in enumerate(fields):

                if i>2:
                    j=1
                
                self.labels.append(ttk.Label(self, text=field))
                self.labels[i].grid(row = j, column=2*i-(2*i*j)+ (j*(2*(i-3))), padx = (20, 5), pady = 10, sticky='w')

                self.entries.append(ttk.Entry(self, width=20))
                self.entries[i].grid(row = j, column = 2*i+1-(2*i*j) + (j*(2*(i-3))), padx = (5, 20), pady = 10, sticky='w')

            self.add.grid(row=2, column=4, sticky="se", padx = 20, pady = 20)


    def remove_entries(self, _):

        if not len(self.labels) == 0:

            for label in self.labels:

                label.grid_forget()
                label.destroy()

            for entry in self.entries:

                entry.grid_forget()
                entry.destroy()

            self.labels = []
            self.entries = []
            self.add.grid_forget()






    

        




        

