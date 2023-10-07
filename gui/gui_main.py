from tkinter import *
from PIL import ImageTk, Image
from difflib import SequenceMatcher
from math import floor
import threading
import time


class Gui:
    def __init__(self,mydata,gui_core):
        
        self.root = Tk()
        self.root.title("Bookshop")
        self.root.geometry("1366x768")
        #self.root.attributes('-fullscreen', True)
        self.mygui_core = gui_core.gui_core(self.root)
        self.root.bind("<F11>", lambda event: self.mygui_core.togglewindowstate())

        self.root.bind('<Return>', self.search)
        self.root.bind_all('<Button>',self.mygui_core.change_focus)
        self.root.bind_all('<Enter>',self.mygui_core.on_enter)
        self.root.bind_all('<Leave>',self.mygui_core.on_leave)

        self.pixel = PhotoImage(width=1, height=1)
        self.resultstext = ""
        self.mydata = mydata

        
        pass




    def load_images(self):
        self.search_logo = ImageTk.PhotoImage(Image.open('images/icons/mag.jpg').resize((30,30)))
        self.cart_logo = ImageTk.PhotoImage(Image.open('images/icons/cart.jpg').resize((30, 30)))
        self.bg_image=ImageTk.PhotoImage(Image.open('images/icons/background 3.jpg').resize((1366, 1250)))
        self.booklogos = []
        self.bookbuttons = []
        self.bookprices = []
        self.booknamelabels = []

        self.titles,self.prices = self.mydata.fetch_titles(price=True)
        for i in range(len(self.titles)):
            self.booklogos.append(ImageTk.PhotoImage(Image.open(f'images/covers/{self.titles[i]}.jpg').resize((190, 300))))
            self.bookbuttons.append(Button(self.root, image=self.booklogos[-1],borderwidth=0,bd=0))
            self.bookbuttons[-1].image = self.booklogos[-1]

            self.booknamelabels.append(Label(
                    self.root, 
                    text=self.titles[i],
                    font=("Arial Italic Bold",11),
                    fg=self.mygui_core.rgb_to_hex(0,0,0),
                    bg=self.mygui_core.rgb_to_hex(255, 255, 255),
                    image=self.pixel,
                    compound="center", 
                    width=190
                )
            )
            self.bookprices.append(Label(
                    self.root, 
                    text=f"Rs. {self.prices[i]}-",
                    font=("Arial Italic Bold",11),
                    fg=self.mygui_core.rgb_to_hex(0,0,0),
                    bg=self.mygui_core.rgb_to_hex(255, 255, 255),
                    image=self.pixel,
                    compound="center", 
                    width=190
                )
            )
        print("images loaded.")



    def start(self):
        self.mainlogo=ImageTk.PhotoImage(Image.open('images/icons/book 2.jpg').resize((200, 200)))
        t = threading.Thread(target=self.mygui_core.bgchange, daemon=True)
        t.start()
        
        #loading data
        self.mainlogopic = Label(self.root,image=self.mainlogo,bg="#f5f5dc")
        self.mainlogopic.image = self.mainlogo
        self.mainlogopic.place(relx=.5, rely=.5,anchor= CENTER)
        self.mainlogopic.after(5000, self.load_screen)
        


     
    def load_screen(self):
        global stop_thread
        stop_thread = True
        self.mainlogopic.destroy()
        self.menubar = Frame(self.root,height=60,width=1285,bg="#0F1111",relief='flat')
        self.menubar["highlightthickness"]=0
        self.menubar["borderwidth"]=0
        self.menubar.grid(row=0,column=0,sticky="W",columnspan=2)
        self.menubar.grid_propagate(0)

        self.pgno = 0
        n1 = len(self.titles)
        self.pagedist = []

        while True:
            if n1>=8:
                self.pagedist.append(8)
                n1 -= 8
            else:
                self.pagedist.append(n1)
                break

        print(self.pagedist)


        self.title = Label(
            self.menubar,
            text="BOOKSHOP",
            font=("Arial Bold Italic",20),
            fg=self.mygui_core.rgb_to_hex(255,255,255),
            bg="#0F1111",
        )

        self.searchbox = Entry(
            self.menubar,
            width=55,
            font=("Consolas",16),
            highlightthickness=2,
            highlightcolor=self.mygui_core.rgb_to_hex(0, 0, 255),
            highlightbackground=self.mygui_core.rgb_to_hex(100, 100, 100)
        )

        self.search_icon = Button(self.menubar, image=self.search_logo, highlightthickness=2,command = self.search)
        self.search_icon.image = self.search_logo

        self.cart_icon = Button(self.menubar, image=self.cart_logo,highlightthickness=2)
        self.cart_icon.image = self.cart_logo

        self.title.place(relx=0.07,rely=0.5,anchor=CENTER)
        self.searchbox.place(relx=0.40,rely=0.5,anchor=CENTER)
        self.search_icon.place(relx=0.685,rely=0.5,anchor=CENTER)
        self.cart_icon.place(relx=0.78,rely=0.5,anchor=CENTER)

        # Create Canvas
        self.canvas1 = Canvas(self.root, width = 1260,height = 708,relief='flat',highlightthickness=0,scrollregion=(0,0,700,1250))
        
        self.hbar=Scrollbar(self.root,orient=HORIZONTAL)
        self.hbar.grid(row=2,column=0)
        self.hbar.config(command=self.canvas1.xview)
        
        
        self.vbar=Scrollbar(self.root,orient=VERTICAL)
        self.vbar.grid(row=1, column=1,sticky="NSEW")
        self.vbar.config(command=self.canvas1.yview)
        
        
        self.canvas1.config(xscrollcommand=self.hbar.set, yscrollcommand=self.vbar.set)
        self.canvas1.bind("<Button-1>", self.callback)

        self.canvas1.grid(row=1,column=0,sticky="EW")
        # Display image
        self.canvas1.create_image( 0, 0, image = self.bg_image,anchor = "nw")
        self.canvas1.create_oval(1175,1100,1225,1150, fill="white",outline="white")
        self.canvas1.create_oval(1100,1100,1150,1150, fill="white",outline="white")

        self.canvas1.create_polygon(
            self.mygui_core.generate_arrow_coordinates(1105, 1105,40,40,"left"), 
            fill="black"
        )
        self.canvas1.create_polygon(
            self.mygui_core.generate_arrow_coordinates(1180, 1105,40,40,"right"), 
            fill="black"
        )

        self.display_books()
    
    def callback(self, event):
        x = self.canvas1.canvasx(event.x)
        y = self.canvas1.canvasy(event.y)

        if x>=1105 and x<=1150 and y>=1105 and y<=1150:
            self.change_page("left")
            pass    
        elif x>=1175 and x<=1225 and y>=1105 and y<=1150:
            self.change_page("right")
            pass


    def change_page(self, side):
        if side == "right":
            if self.pgno == len(self.pagedist):
                return
            else:
                self.canvas1.delete("todel")
                s = sum(self.pagedist[0:self.pgno+1])
                e = s+self.pagedist[self.pgno+1] 
                self.pgno += 1     
        else:
            if self.pgno == 0:
                return
            else:
                self.canvas1.delete("todel")
                e = sum(self.pagedist[0:self.pgno])
                s = e-self.pagedist[self.pgno-1] 
                self.pgno -=1
        self.canvas1.yview_moveto(0.0)
        self.display_books(s,e)
    
    def display_books(self,s=0,e=8):
        xnum = 100
        ynum = 100
        for i in range(s,e):
            self.bookbuttons[i].image = self.booklogos[i]
            self.canvas1.create_window(xnum, ynum, anchor = "nw",window=self.bookbuttons[i],tags=("todel"))
            self.bookbuttons[i].lift()
            self.canvas1.create_window(xnum,ynum+315, anchor="nw", window=self.booknamelabels[i],tags=("todel"))
            self.booknamelabels[i].lift()
            self.canvas1.create_window(xnum,ynum+340, anchor="nw", window=self.bookprices[i],tags=("todel"))
            self.bookprices[i].lift()
            if i==s+3:
                xnum = 100
                ynum += 500
            else: 
                xnum += 300

    def search(self,*h):
        inpt = self.searchbox.get().lower().strip()
        if len(inpt) == 0:
            if self.resultstext:
                self.canvas1.delete(self.resultstext)
            return    
        self.searchbox.delete(0,'end')
        self.root.focus_set()
        titles = [item.lower() for item in self.mydata.fetch_titles()]
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

