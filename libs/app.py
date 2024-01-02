from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import os

import tkinter as tk
from tkinter import ttk

from threading import Thread

from widgets import Categories, InfoBase, SearchBox, ComponentManager
from image_handlers import ModulesImageHandler

import numpy as np




class PouchApp(tk.Tk):


    def __init__(self):

        self.running = True

        tk.Tk.__init__(self)
        tk.Tk.wm_title(self, "Pouch")
        self.tk.call("source", "azure.tcl")
        self.tk.call("set_theme", "dark")
        self.protocol('WM_DELETE_WINDOW', self.on_destroy)
        self.resizable(tk.FALSE, tk.FALSE)

        SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
        SPREADSHIT_ID = "1yCBXd-uQdGVxtdqc1q4RfAEP3STyVT13l868Ps7s3ec"


        self.credentials = None
        self.sheets = {}

        self.auth_initialize(SCOPES)
        self.read_spreadsheets(SPREADSHIT_ID)

        self.categories = Categories(self)
        self.categories.init_entries(self.sheets)
        self.categories.grid(row=0, column=0, padx = (10,5), pady = 10, sticky = 'nw')

        self.search = SearchBox(self)
        self.search.grid(row = 1, column=0, padx = (10,5), pady = 10, sticky = 'nw', rowspan=1)

        self.info_section = None

        self.component_manager = ComponentManager(self, self.sheets)
        self.component_manager.grid(row = 2, column= 0, columnspan=2, sticky = 'nw', padx = 10, pady = (5, 10))

        



    def update_gui(self):

        if self.categories.changed:

            self.handle_selection(self.categories.selection)
            self.categories.changed = False

        if not self.info_section == None and self.info_section.entries.changed:

            self.info_section.details.update_details(self.info_section.entries.selection)
            self.info_section.entries.changed = False

        if not self.info_section == None and not self.info_section.image_handler == None and self.info_section.image_handler.loaded:

            self.info_section.image_handler.update_images()
            

        self.update_idletasks()
        self.update()


    def start(self):

        while self.running:

            self.update_gui()


    def auth_initialize(self, scopes):

        
        if os.path.exists('auth/token.json'):
            self.credentials = Credentials.from_authorized_user_file('auth/token.json', scopes)
        if not self.credentials or not self.credentials.valid:
            if self.credentials and self.credentials.expired and self.credentials.refresh_token:
                self.credentials.refresh(Request())

            else:
                flow = InstalledAppFlow.from_client_secrets_file('auth/credentials.json', scopes)
                self.credentials = flow.run_local_server(port=0)
            with open("auth/token.json", 'w') as token:
                token.write(self.credentials.to_json())


    def read_spreadsheets(self, spreadsheet_id):

        service = build("sheets", "v4", credentials=self.credentials)
        sheets = service.spreadsheets()

        spreadsheet = sheets.get(spreadsheetId=spreadsheet_id, includeGridData=True).execute()

        sheet_names = [sheet['properties']['title'] for sheet in spreadsheet['sheets']]

        for sheet_name in sheet_names:

            range_name = f"{sheet_name}!A1:J100"  # Adjust the range as needed
            result = sheets.values().get(spreadsheetId=spreadsheet_id, range=range_name).execute()
            values = result.get('values', [])

            sheet = self.parse_sheet(values, sheet_name)

            self.sheets[sheet_name] = sheet

            # break
            
        

    
    def parse_sheet(self, values, sheet_name):

        if values:
            # Find the last non-empty row
            last_row_index = max(i for i, row in enumerate(values) if any(row))

            # Find the last non-empty column
            last_col_index = max(j for row in values for j, cell_value in enumerate(row) if cell_value)

            # Extract non-empty rows and columns
            non_empty_rows = values[:last_row_index + 1]
            non_empty_columns = [row[:last_col_index + 1] for row in non_empty_rows]

            sheet = {}
            keys = None
            arrays = []

            # Print or process non-empty rows and columns            
            for col_index, cell_value in enumerate(non_empty_columns):                 

                if col_index == 0:
                    
                    keys = cell_value
                    arrays = [[] for i in range(len(keys))]

                else:

                    for index, value in enumerate(cell_value):

                        arrays[index].append(value)

            for i, key in enumerate(keys):

                
                sheet[key] = arrays[i]

            return sheet
            
            
            
            
            # sheet[keys[index]]



    


    def on_destroy(self):

        self.running = False
        self.destroy()
        self.quit()


    def handle_selection(self, selection):

        # if selection == "Resistors":

        self.create_info_section(selection, self.sheets[selection])

        if selection == "Modules":

            self.info_section.image_handler = ModulesImageHandler(self.sheets[selection], self.info_section)

        


    def create_info_section(self, label, data):

        if self.info_section == None:

            self.info_section = InfoBase(self, label, data)
            self.info_section.grid(row=0, column=1, padx=20, pady=10, sticky="nw", rowspan=2)

        else:

            self.info_section.grid_forget()
            self.info_section = InfoBase(self, label, data)
            self.info_section.grid(row=0, column=1, padx=20, pady=10, sticky="nw", rowspan=2)


        





if __name__ == '__main__':

    app = PouchApp()
    app.start()

   