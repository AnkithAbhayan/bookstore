from tkinter import *

from time import sleep

class gui_core:
    def __init__(self,root):
        self.root = root
        """x":[
                    (16,24),(16,18),(18,16),(24,16),(50,42),
                    (76,16),(82,16),(84,18),(84,24),(58,50),

                    (84,76),(84,82),(82,84),(76,84),(50,58),

                    
                    (24,84),(18,84),(16,82),(16,76),(42,50)
                ]"""
        self.shapes = {
            "arrow": [(15,35),(55,35),(55,15),(90,50),(55,85),(55,65),(15,65)],
            "x":[
                    (16,24),(24,16),(50,42),
                    (76,16),(84,24),(58,50),

                    (84,76),(76,84),(50,58),
                    (24,84),(16,76),(42,50)
                ]
        }

    def change_focus(self,*h):
        h[0].widget.focus_set()

    def on_enter(self,*h):
        if ".!button" in str(h[0].widget):
            h[0].widget['bg'] = "#00FFFF" 
            h[0].widget['highlightbackground'] = "#00FFFF" 
           
        elif  '.!entry' in str(h[0].widget):
            h[0].widget['highlightbackground'] = "#00FFFF" 

    def on_leave(self,*h):
        if ".!button" in str(h[0].widget):
            h[0].widget['bg'] = "#FFFFFF" 
            h[0].widget['highlightbackground'] = "#FFFFFF" 
        elif  '.!entry' in str(h[0].widget):
            h[0].widget['highlightbackground'] = self.rgb_to_hex(100, 100, 100)

    def togglewindowstate(self):
        if self.root.attributes('-fullscreen'):
            self.root.attributes('-fullscreen', False)
        else:
            self.root.attributes('-fullscreen', True)

    def bgchange(self):
        r,g,b=255,255,255
        f=False
        for i in range(75): #red
            b -= 1
            g -= 1
            sleep(0.01)
            self.root["bg"] = self.rgb_to_hex(r, g, b)

        for i in range(75): #green
            g+=1
            r-=1
            sleep(0.01)
            self.root["bg"] = self.rgb_to_hex(r, g, b)

        for i in range(75): #blue
            b += 1
            g -= 1
            sleep(0.01)
            self.root["bg"] = self.rgb_to_hex(r, g, b)

        for i in range(75):
            r+=1
            g+=1
            sleep(0.01)
            self.root["bg"] = self.rgb_to_hex(r, g, b)

        self.root["bg"] = self.rgb_to_hex(255, 255, 255)

    def generate_coordinates(self,x,y,totx=100,toty=100,orient=None,shape="arrow"):
        if orient=="right":
            sft = 0
        else:
            sft = totx
        points = self.shapes[shape]
        npoints = []
        for coord in points:
            npoints.extend([round(x+abs(sft-(coord[0]/100)*totx)),round(y+(coord[1]/100)*toty)])

        return npoints


    def rgb_to_hex(self, r, g, b):
        return '#{:02x}{:02x}{:02x}'. format(r, g, b)
