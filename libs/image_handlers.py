import os
from PIL import Image, ImageTk, ImageOps, ImageDraw
from threading import Thread

from io import BytesIO

import requests

import copy




class WebImageHandler():

    def __init__(self, sheets, parent):

        self.urls = (sheets["Image"], list(sheets.values())[0])
        self.image = None
        self.parent = parent
 
        self.done_task = False
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

        self.done_task = True
            


    def update_images(self):

        if not self.selection == None:

            self.download_thread.join()

            self.done_task = False
            
            if not self.selection == "Failed":

                self.handle_selection(self.selection)

            self.selection = None

            self.download_thread = None






class ResistorsImageHandler():

    def __init__(self, sheets, parent):

        self.parent = parent

        self.done_task = False

        self.coding = {1:"black", 10:"brown", 100:"red", 1000:"orange", 10000:"yellow", 100000:"green",
                        1000000:"blue", 1000000:"purple", 0.1:"gold", 0.01:"silver"}

        self.multipliers = {"M":1000000, "K":1000, "":1}

        self.digits_colors = ["black", "brown", "red", "orange", "yellow", "green",
                                "blue", "purple", "grey", "white", "gold", "silver"]
        
        self.band_sizes = [(9, 44), (9, 34), (9, 34), (9, 34), (9, 43)]
        self.band_positions = [(68, 107), (94, 112), (116,112), (137, 112), (163, 108)]

        self.base_resistor_image = Image.open('res/resistor_small.jpg')
        self.resistor_image = Image.open('res/resistor_small.jpg')

        self.tk_image = ImageTk.PhotoImage(self.base_resistor_image)      

        self.parent.image.canvas.image = self.tk_image
        self.parent.image.canvas.config(image = self.tk_image)
        
    
    def handle_selection(self, selection):

        digits = float(selection.split(' ')[0])
        multiplier = selection.split(' ')[1].strip("Ω")
        multiplier = self.multipliers[multiplier]

        value = digits * multiplier
        key = self.find_divisor(value)

        truncated_digits = str(value/key)

        colors = []

        for i, digit in enumerate(truncated_digits):

            if i < 3:

                colors.append(self.digits_colors[int(digit)])

        colors.append(self.coding[key])
        colors.append('brown')

        for i in range(5):

            self.draw_rectangle(self.resistor_image, self.band_positions[i], self.band_sizes[i], colors[i])


        self.done_task = True 

            

      


    def find_divisor(self, number):

        for key in self.coding.keys():
            result = number / key
            if result / 100 >= 1 and result / 100 <= 10:
                return key

        return None

    def update_images(self):

        self.tk_image = ImageTk.PhotoImage(self.resistor_image)      

        self.parent.image.canvas.image = self.tk_image
        self.parent.image.canvas.config(image = self.tk_image)

        self.resistor_image = copy.deepcopy(self.base_resistor_image)
        self.done_task = False




    def draw_rectangle(self, image, position, size, color):
        # Create a drawing object
        draw = ImageDraw.Draw(image)

        # Calculate the coordinates of the rectangle
        x1, y1 = position
        x2, y2 = x1 + size[0], y1 + size[1]

        # Draw the rectangle
        draw.rectangle([x1, y1, x2, y2], fill=color)

