from tkinter import *
from PIL import ImageTk, Image
from difflib import SequenceMatcher
from math import floor
import threading
from time import sleep


class Gui:
    def __init__(self,mydata,gui_core,window,canvas):
        self.mycanvas = canvas
        self.root = window
        self.root.title("Bookshop")
        self.root.geometry("1366x768")
        self.root.attributes('-fullscreen', True)
        self.mygui_core = gui_core.gui_core(self.root)

        self.root.unbind("<F11>")
        self.root.unbind("<Button-1>")
        self.root.unbind_all('<Enter>')
        self.root.unbind_all('<Leave>')

        self.root.bind("<F11>", lambda event: self.mygui_core.togglewindowstate())

        self.root.bind('<Return>', self.deltextandsearch)
        self.root.bind_all('<Button>',self.mygui_core.change_focus)
        self.root.bind_all('<Enter>',self.mygui_core.on_enter)
        self.root.bind_all('<Leave>',self.mygui_core.on_leave)
        self.br = ""
        self.tl = ""
        self.arrowstate = True
        self.s,self.e=0,8

        self.pixel = PhotoImage(width=1, height=1)
        self.mydata = mydata      

        self.scr_width = self.root.winfo_screenwidth()
        self.scr_height = self.root.winfo_screenheight()

        #ratios
        self.bgap = round(self.scr_width*0.066)
        self.lrgap = round(self.scr_width*0.1)
        self.bookx = round(self.scr_width*0.15)
        self.booky = round((16*self.bookx)/9)

    def callback2(self,event):
        x = self.canvas2.canvasx(event.x)
        y = self.canvas2.canvasy(event.y)
        if x>=10 and x<=60 and y>=10 and y<=60:
            self.canvas2.grid_forget()
            self.canvas1.grid(row=1,column=0,sticky="EW")
            self.vbar.config(command=self.canvas1.yview)

    def showbookdetails(self,book):
        self.canvas1.grid_forget()

        self.canvas2 = Canvas(self.root, width = self.root.winfo_screenwidth()-20,height = self.scr_height-60,relief='flat',highlightthickness=0,scrollregion=(0,0,700,self.scr_height*1.33))

        self.vbar.config(command=self.canvas2.yview)
        self.canvas2.config(xscrollcommand=self.hbar.set, yscrollcommand=self.vbar.set,yscrollincrement=10)

        self.canvas2.grid(row=1,column=0,sticky="EW")
        self.canvas2.bind("<Button-1>", self.callback2)

        points = [0,self.scr_height,self.scr_width,self.scr_height,self.scr_width,self.scr_height*1.34,0,self.scr_height*1.34]
        self.canvas2.create_polygon(points,fill="black",outline="grey")
        
        #self.bufferimg = ImageTk.PhotoImage(Image.open(f"images/covers/{book}.jpg").resize((round(self.scr_width//4.5),round((16*self.scr_width//4.5)/9)))) 
        self.bg_image2 = ImageTk.PhotoImage(Image.open("images/AMERICAN PSYCHO.jpeg").resize((self.scr_width-20,self.scr_height-60)))
        self.canvas2.create_image(0,0,image=self.bg_image2,anchor="nw")
        

        #self.canvas2.create_image( 125, 75, image = self.bufferimg,anchor = "nw")

        self.canvas2.create_oval(10,10,60,60, fill="white",outline="grey",activeoutline="cyan",width=3,tags=("arrows"))        
        self.canvas2.create_polygon(
            self.mygui_core.generate_coordinates(15, 15,40,40,"left","arrow"),
            fill = "black",tags=("arrows")
        )

        """data = self.mydata.fetch_bookdetails(book)

        n=50
        if len(book)>25:
            n=30

        self.titlelbl = Label(self.root,text=data["title"],font=("Liberation Serif",n))
        self.authorlbl = Label(self.root,text=f'- {data["author"]}',font=("Liberation Serif",25))
        self.pricelbl = Label(self.root,text=f"Rs.{data['price']}",font=("Liberation Serif",50))

        xl = round(self.scr_width//4.5)
        self.canvas2.create_window(xl+200, 100, anchor = "nw",window=self.titlelbl)
        self.canvas2.create_window(xl+210, 200, anchor = "nw",window=self.authorlbl)
        self.canvas2.create_window(xl+200, 400, anchor="nw",window=self.pricelbl)"""
        self.menubar.lift()
        #


    def load_images(self):
        self.search_logo = ImageTk.PhotoImage(Image.open('images/icons/mag.jpg').resize((30,30)))
        self.cart_logo = ImageTk.PhotoImage(Image.open('images/icons/cart.jpg').resize((30, 30)))
        self.bg_image=ImageTk.PhotoImage(Image.open('images/icons/background 3.jpg').resize((self.scr_width, 1250)))
        self.booklogos = []
        self.bookbuttons = []
        self.bookprices = []
        self.booknamelabels = []

        self.titles,self.prices = self.mydata.fetch_titles(price=True)
        for i in range(len(self.titles)):
            self.booklogos.append(ImageTk.PhotoImage(Image.open(f'images/covers/{self.titles[i]}.jpg').resize((self.bookx, self.booky))))
            self.bookbuttons.append(Button(self.root, image=self.booklogos[-1],borderwidth=0,bd=0,command=lambda i=i:self.showbookdetails(self.titles[i])))
            self.bookbuttons[-1].image = self.booklogos[-1]

            self.booknamelabels.append(
                Label(
                    self.root, 
                    text=self.titles[i],
                    font=("Arial Italic Bold",11),
                    fg=self.mygui_core.rgb_to_hex(0,0,0),
                    bg=self.mygui_core.rgb_to_hex(255, 255, 255),
                    image=self.pixel,
                    compound="center", 
                    width=self.bookx-5
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
                    width=self.bookx-5
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
        self.mycanvas.destroy()
        
     
    def load_screen(self):
        global stop_thread
        stop_thread = True
        self.mainlogopic.destroy()
        self.menubar = Frame(self.root,height=60,width=self.root.winfo_screenwidth(),bg="#0F1111",relief='flat')
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



        self.title = Label(
            self.menubar,
            text="KITAB",
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
        self.searchbox.bind('<KeyRelease>',self.search)
        self.search_icon = Button(self.menubar, image=self.search_logo, highlightthickness=2,command = self.search)
        self.search_icon.image = self.search_logo

        self.cart_icon = Button(self.menubar, image=self.cart_logo,highlightthickness=2)
        self.cart_icon.image = self.cart_logo

        self.title.place(relx=0.07,rely=0.5,anchor=CENTER)
        self.searchbox.place(relx=0.40,rely=0.5,anchor=CENTER)
        self.search_icon.place(relx=0.685,rely=0.5,anchor=CENTER)
        self.cart_icon.place(relx=0.78,rely=0.5,anchor=CENTER)

        # Create Canvas
        self.canvas1 = Canvas(self.root, width = self.root.winfo_screenwidth()-20,height = 708,relief='flat',highlightthickness=0,scrollregion=(0,0,700,1450))
        
        self.hbar=Scrollbar(self.root,orient=HORIZONTAL)
        self.hbar.grid(row=2,column=0)
        self.hbar.config(command=self.canvas1.xview)
        
        
        self.vbar=Scrollbar(self.root,orient=VERTICAL)
        self.vbar.grid(row=1, column=1,sticky="NSEW")
        self.vbar.config(command=self.canvas1.yview)
        
        
        self.canvas1.config(xscrollcommand=self.hbar.set, yscrollcommand=self.vbar.set,yscrollincrement=10)
        self.canvas1.bind("<Button-1>", self.callback)

        self.canvas1.grid(row=1,column=0,sticky="EW")
        # Display image
        x = self.root.winfo_screenwidth()-20
        
        points = [0,1250,x,1250,x,1460,0,1460]
        self.canvas1.create_polygon(points,fill="black",outline="grey")
        self.canvas1.create_text(20,1275, anchor="nw", text="Made by Ankith Abhayan and Rajath Valsan.",fill="grey",font=("Courier New",15))
        self.canvas1.create_image( 0, 0, image = self.bg_image,anchor = "nw")

        self.updatearrowmarks()
        self.l = list(range(0,8))
        self.display_books(f=True)
        self.menubar.lift()
        
    
    def callback(self, event):
        lc = [self.scr_width-200,1150,self.scr_width-150,1200]
        rc = [self.scr_width-125,1150,self.scr_width-75,1200]

        x = self.canvas1.canvasx(event.x)
        y = self.canvas1.canvasy(event.y)
        if self.arrowstate == True:        
            if x>=self.scr_width-200 and x<=self.scr_width-150 and y>=1150 and y<=1200:
                self.change_page("left")                    
            elif x>=self.scr_width-125 and x<=self.scr_width-75 and y>=1150 and y<=1200:
                self.change_page("right")
        
        if self.br and self.tl:
            if x>=self.br[0]+25 and x<=self.br[0]+60 and y>=self.tl[1] and y<=self.tl[1]+37:
                self.canvas1.delete("todel2")
                self.searchbox.delete(0,'end')
                self.updatearrowmarks()
                self.display_books(self.s,self.e)
                self.vbar.grid(row=1, column=1,sticky="NSEW")

    def updatearrowmarks(self):
        self.arrowstate = True

        lc = [self.scr_width-200,1150,self.scr_width-150,1200]
        rc = [self.scr_width-125,1150,self.scr_width-75,1200]
        #self.lcirc = self.canvas1.create_oval(1100,1100,1150,1150, fill="white",outline="white",activeoutline="cyan",width=3,tags=("arrows"))
        #self.rcirc = self.canvas1.create_oval(1175,1100,1225,1150, fill="white",outline="white",activeoutline="cyan",width=3,tags=("arrows"))
        
        self.lcirc = self.canvas1.create_oval(lc, fill="white",outline="white",activeoutline="cyan",width=3,tags=("arrows"))
        self.rcirc = self.canvas1.create_oval(rc, fill="white",outline="white",activeoutline="cyan",width=3,tags=("arrows"))
        
        self.larrow = self.canvas1.create_polygon(
            self.mygui_core.generate_coordinates(lc[0]+5, 1155,40,40,"left","arrow"),
            fill = "black",tags=("arrows")
        )
        self.rarrow = self.canvas1.create_polygon(
            self.mygui_core.generate_coordinates(rc[0]+5, 1155,40,40,"right","arrow"), 
            fill = "black",tags=("arrows")
        )

        if self.pgno == 0:
            self.canvas1.itemconfig(self.lcirc,fill="grey")
            self.canvas1.itemconfig(self.lcirc,outline='grey')
            self.canvas1.itemconfig(self.lcirc,activeoutline="grey")
    
        elif self.pgno == len(self.pagedist)-1:
            self.canvas1.itemconfig(self.rcirc,fill="grey")
            self.canvas1.itemconfig(self.rcirc,outline='grey')
            self.canvas1.itemconfig(self.rcirc,activeoutline = "grey") 

    def change_page(self, side):
        if side == "right":
            if self.pgno == len(self.pagedist)-1:
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
        self.s = s
        self.e = e
        
        scrlthread = threading.Thread(target=self.smoothscrolltotop,daemon=True)
        scrlthread.start()
        self.display_books(s,e)
        self.updatearrowmarks()

    def smoothscrolltotop(self):   
        for i in range(100,0,-1):
            self.canvas1.yview_moveto(i/100)
            
    
    def display_books(self,s=0,e=8,l=None,f=False):
        if l==None:
            l = list(range(s,e))

        if l==self.l and f==False:
            return
        
        self.canvas1.delete("todel")
            
        self.l = l
        xnum = self.lrgap
        ynum = round(self.lrgap*0.75)
        
        for i in l:
            self.bookbuttons[i].image = self.booklogos[i]
            self.canvas1.create_window(xnum, ynum, anchor = "nw",window=self.bookbuttons[i],tags=("todel"))
            self.bookbuttons[i].lift()
            self.canvas1.create_window(xnum,(ynum+self.booky)+15, anchor="nw", window=self.booknamelabels[i],tags=("todel"))
            self.booknamelabels[i].lift()
            self.canvas1.create_window(xnum,(ynum+self.booky)+40, anchor="nw", window=self.bookprices[i],tags=("todel"))
            self.bookprices[i].lift()
            xnum += self.bookx+self.bgap

            if len(l)>4:
                if i==s+3:
                    xnum = self.lrgap
                    ynum += self.booky*1.5
        self.menubar.lift()
        self.pgstatus = self.canvas1.create_text(self.scr_width-125,1275,text=f"showing page {self.pgno+1} of 3",fill="white", font=("Consolas",13),tags=("todel"))

    def deltextandsearch(self,*h):
        self.searchbox.delete(0,'end')
        self.root.focus_set()
        
        
    def search(self,*h):
        inpt = self.searchbox.get().lower().strip()
        self.canvas1.delete("todel2")
        if len(inpt) == 0:
            self.updatearrowmarks()
            self.display_books(self.s,self.e)
            self.vbar.grid(row=1, column=1,sticky="NSEW")
            return    
            
        titles = self.mydata.fetch_titles()
        ratios = {}
        for i in range(len(titles)):
            ratios.update({SequenceMatcher(None, inpt, titles[i].lower()).ratio():titles[i]})
        
        list1 = []
        maxes = sorted(list(ratios.keys()))
        
        if maxes[-1] > 0.8:
            list1.append(ratios[maxes[-1]])
        else:
            i=1
            for n in titles:
                if inpt.lower() in n.lower():
                    list1.append(n)
                    i+=1
                if i>4:
                    break
        
        indices = []
        for item in list1:
            indices.append(self.titles.index(item))

        self.canvas1.delete("arrows")
        self.arrowstate = False
        self.display_books(l=indices)
        tl = (35,14)
        br = (tl[0]+165+(len(inpt)*13),51)
        self.canvas1.yview_moveto(0)
        """
        self.canvas1.create_arc(20,15,50,50,start=90,extent=180,fill="white",width=0,style=CHORD,outline="white")
        self.canvas1.create_polygon(36,14, 234,14, 234,51, 36,51,fill="white")
        self.canvas1.create_arc(220,15,250,50,start=270,extent=180,fill="white",width=0,style=CHORD,outline="white")
        """

        self.larc = self.canvas1.create_arc(tl[0]-16,tl[1],br[1]-1,br[1]-1,start=90,extent=180,fill="white",width=0,style=CHORD,outline="white",tags="todel2")
        self.rect = self.canvas1.create_polygon(tl[0],tl[1], br[0],tl[1], br[0],br[1], tl[0],br[1],fill="white",tags="todel2")
        self.rarc = self.canvas1.create_arc(br[0]-16,tl[1]+1,br[0]+16,br[1]-1,start=270,extent=180,fill="white",width=0,style=CHORD,outline="white",tags="todel2")

        self.resultstext = self.canvas1.create_text(tl[0],tl[1]+6, anchor="nw", text=f"results for: '{inpt}'", font=("Consolas",15),tags="todel2")
        
       
        self.circlex = self.canvas1.create_oval(br[0]+25,tl[1],br[0]+62,br[1], fill="white",outline="white",tags="todel2")
        self.xsymbol = self.canvas1.create_polygon(
            self.mygui_core.generate_coordinates(br[0]+30, tl[1]+5,27,27,"right","x"),
            fill="black",tags="todel2"
        )
        self.tl = tl
        self.br = br

        self.vbar.grid_forget()