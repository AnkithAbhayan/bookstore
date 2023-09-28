from tkinter import *
from PIL import ImageTk, Image
from difflib import SequenceMatcher

from core import data
import threading
import time

stop_thread = False

class Gui:
    def __init__(self,mydata):
        self.root = Tk()
        self.root.title("Bookshop")
        self.root.attributes('-fullscreen', True)
        self.root.bind("<F11>", lambda event: self.togglewindowstate())
        self.root.bind('<Return>', self.search)
        self.root.bind_all('<Button>',self.change_focus)
        self.root.bind_all('<Enter>',self.on_enter)
        self.root.bind_all('<Leave>',self.on_leave)
        self.root.wm_attributes('-transparentcolor','grey')

        self.pixel = PhotoImage(width=1, height=1)
        self.resultstext = ""
        self.mydata = mydata
        pass

    def change_focus(self,*h):
        h[0].widget.focus_set()

    def on_enter(self,*h):
        if ".!button" in str(h[0].widget):
            h[0].widget['bg'] = "#00FFFF" 
        elif  '.!entry' in str(h[0].widget):
            h[0].widget['highlightbackground'] = "#00FFFF" 

    def on_leave(self,*h):
        if ".!button" in str(h[0].widget):
            h[0].widget['bg'] = "#FFFFFF" 
        elif  '.!entry' in str(h[0].widget):
            h[0].widget['highlightbackground'] = rgb_to_hex(100, 100, 100)


    def load_images(self):
        self.mainlogo=ImageTk.PhotoImage(Image.open('images/icons/book 2.jpg').resize((200, 200)))
        self.search_logo = ImageTk.PhotoImage(Image.open('images/icons/mag.jpg').resize((30,30)))
        self.cart_logo = ImageTk.PhotoImage(Image.open('images/icons/cart.jpg').resize((30, 30)))
        self.bg_image=ImageTk.PhotoImage(Image.open('images/icons/background 3.jpg').resize((1366, 708)))


    def bgchange(self):
        r,g,b=255,255,255
        f=False
        for i in range(75): #red
            b -= 1
            g -= 1
            time.sleep(0.01)
            self.root["bg"] = rgb_to_hex(r, g, b)

        for i in range(75): #green
            g+=1
            r-=1
            time.sleep(0.01)
            self.root["bg"] = rgb_to_hex(r, g, b)

        for i in range(75): #blue
            b += 1
            g -= 1
            time.sleep(0.01)
            self.root["bg"] = rgb_to_hex(r, g, b)

        for i in range(75):
            r+=1
            g+=1
            time.sleep(0.01)
            self.root["bg"] = rgb_to_hex(r, g, b)

        self.root["bg"] = rgb_to_hex(255, 255, 255)

    def start(self):
        self.mainlogopic = Label(self.root,image=self.mainlogo,bg="#f5f5dc")
        self.mainlogopic.image = self.mainlogo
        self.mainlogopic.place(relx=.5, rely=.5,anchor= CENTER)
        t = threading.Thread(target=self.bgchange, daemon=True)
        t.start()
        self.mainlogopic.after(1000, self.load_screen)

    def togglewindowstate(self):
        if self.root.attributes('-fullscreen'):
            self.root.attributes('-fullscreen', False)
        else:
            self.root.attributes('-fullscreen', True)
     
    def load_screen(self):
        global stop_thread
        stop_thread = True
        self.mainlogopic.destroy()
        self.menubar = Frame(self.root,height=60,width=1366,bg="#0F1111",relief='flat')
        self.menubar["highlightthickness"]=0
        self.menubar["borderwidth"]=0
        self.menubar.grid(row=0,column=0,sticky="WE")
        self.menubar.grid_propagate(0)

        self.title = Label(
            self.menubar,
            text="BOOKSHOP",
            font=("Arial Bold Italic",20),
            fg=rgb_to_hex(255,255,255),
            bg="#0F1111",
        )

        self.searchbox = Entry(
            self.menubar,
            width=55,
            font=("Consolas",16),
            highlightthickness=2,
            highlightcolor=rgb_to_hex(0, 0, 255),
            highlightbackground=rgb_to_hex(100, 100, 100)
        )

        self.search_icon = Button(self.menubar, image=self.search_logo, highlightthickness=0,command = self.search)
        self.search_icon.image = self.search_logo

        self.cart_icon = Button(self.menubar, image=self.cart_logo,highlightthickness=0)
        self.cart_icon.image = self.cart_logo

        self.title.place(relx=0.07,rely=0.5,anchor=CENTER)
        self.searchbox.place(relx=0.40,rely=0.5,anchor=CENTER)
        self.search_icon.place(relx=0.668,rely=0.5,anchor=CENTER)
        self.cart_icon.place(relx=0.78,rely=0.5,anchor=CENTER)

        # Create Canvas
        self.canvas1 = Canvas(self.root, width = 1366,height = 708,relief='flat',highlightthickness=0)
 
        self.canvas1.grid(row=1,column=0,sticky="WE")
        # Display image
        self.canvas1.create_image( 0, 0, image = self.bg_image,anchor = "nw")
        mygui.display_books()
        
    
    def display_books(self):
        self.booklogos = []
        self.bookbuttons = []
        self.buttoncanvasses = []
        
        self.booklabels = []
        self.booklabelcanvasses = []

        num = 100
        titles = mydata.fetch_titles()
        for i in range(4):
            self.booklogos.append(ImageTk.PhotoImage(Image.open(f'images/covers/{titles[i]}.jpg').resize((190, 300))))
            self.bookbuttons.append(Button(self.root, image=self.booklogos[-1]))
            self.bookbuttons[-1].image = self.booklogos[-1]
            self.buttoncanvasses.append(self.canvas1.create_window(num, 100, anchor = "nw",window=self.bookbuttons[-1]))
            
            self.booklabels.append(Label(
                self.root, 
                text=titles[i],
                font=("Arial Italic Bold",13),
                fg=rgb_to_hex(0,0,0),
                bg=rgb_to_hex(255, 255, 255),
                image=self.pixel,
                compound="center", 
                width=190
                ))
            self.booklabelcanvasses.append(self.canvas1.create_window(num,415, anchor="nw", window=self.booklabels[-1],))
            num += 300





    def search(self,*h):
        inpt = self.searchbox.get().lower().strip()
        if len(inpt) == 0:
            if self.resultstext:
                self.canvas1.delete(self.resultstext)
            return    
        self.searchbox.delete(0,'end')
        self.root.focus_set()
        titles = [item.lower() for item in mydata.fetch_titles()]
        ratios = {}
        for i in range(len(titles)):
            ratios.update({SequenceMatcher(None, inpt, titles[i]).ratio():titles[i]})
        
        maxes = sorted(list(ratios.keys()))
        if maxes[-1] > 0.45:
            i = -1
            while True:
                if maxes[i] > 0.45:
                    print(maxes[i],ratios[maxes[i]])
                    i -= 1
                else:
                    break
        else:
            if len(inpt) > 2:
                i=1
                for n in titles:
                    if inpt in n.lower():
                        print(n)
                        i+=1
                        if i>4:
                            break
        if self.resultstext:
            self.canvas1.delete(self.resultstext)
        self.resultstext = self.canvas1.create_text(20,20, anchor="nw", text=f"results for '{inpt}':", font=("Consolas",15))


def rgb_to_hex(r, g, b):
    return '#{:02x}{:02x}{:02x}'. format(r, g, b)



mydata = data.DataClient()
mygui = Gui(mydata)
mygui.load_images()
mygui.start()






mygui.root.mainloop()