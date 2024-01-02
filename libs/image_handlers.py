import os
from PIL import Image, ImageTk, ImageOps
from threading import Thread

from io import BytesIO

import requests




class ModulesImageHandler():

    def __init__(self, sheets, parent):

        self.urls = (sheets["Image"], list(sheets.values())[0])
        self.image = None
        self.parent = parent
 
        self.loaded = False
        self.download_thread = None
        self.selection = None

        os.makedirs('.cache/modules', exist_ok=True)


    def handle_selection(self, selection):

        index = None

        for i, pair in enumerate(self.urls[1]):

            if pair == selection:

                index = i

        if not index == None:

            url = self.urls[0][index]

            files = os.listdir('.cache/modules')
            
            if f'{selection}.jpg' in files:

                tk_image = ImageTk.PhotoImage(Image.open(os.path.join('.cache/modules', f'{selection}.jpg')))

                self.parent.image.canvas.image = tk_image
                self.parent.image.canvas.config(image = tk_image)

            else:

                self.parent.image.canvas.image = self.parent.image.blank
                self.parent.image.canvas.config(image = self.parent.image.blank)
                if self.download_thread == None:

                    self.download_thread = Thread(target=self.download_thread_fn, args=(url, selection, ))
                    self.download_thread.start()



        


    def download_thread_fn(self, url, name):    

        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an exception for bad responses
        except requests.exceptions.RequestException as e:
            print(f"Error downloading image: {e}")
            self.selection = "Failed"
            
        try:
            img = Image.open(BytesIO(response.content))
            
            img = ImageOps.expand(img, border=(int(max(img.size)/6), int(max(img.size)/6)), fill='white')

            img = img.resize((256, 256))

            img.save(os.path.join('.cache/modules', f'{name}.jpg'), )

            self.selection = name

        except Exception as e:
            print(f"Error opening image: {e}")
            self.selection = "Failed"

        self.loaded = True
            


    def update_images(self):

        if not self.selection == None:

            self.download_thread.join()

            self.loaded = False
            
            if not self.selection == "Failed":

                self.handle_selection(self.selection)

            self.selection = None

            self.download_thread = None