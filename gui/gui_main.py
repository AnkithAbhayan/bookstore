from tkinter import *
from PIL import ImageTk, Image
from difflib import SequenceMatcher
from math import floor
import threading
from time import sleep
import os
import sys

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

        self.cart = mydata.fetch_cart(mydata.uname)
        print(self.cart)

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

    def callback3(self,event):
        x = self.canvas3.canvasx(event.x)
        y = self.canvas3.canvasy(event.y)

        if x>=10 and x<=60 and y>=10 and y<=60:
            self.canvas3.grid_forget()
            self.canvas1.grid(row=1,column=0,sticky="EW")
            self.vbar.config(command=self.canvas1.yview)

    def callback2(self,event):
        x = self.canvas2.canvasx(event.x)
        y = self.canvas2.canvasy(event.y)

        if x>=10 and x<=60 and y>=10 and y<=60:
            self.canvas2.grid_forget()
            self.canvas1.grid(row=1,column=0,sticky="EW")
            self.vbar.config(command=self.canvas1.yview)

        if x>=(1283/1600)*(self.scr_width-20) and x<=(1391/1600)*(self.scr_width-20) and y >= (718/900)*(self.scr_height-60) and y<= (790/900)*(self.scr_height-60):
            book = self.data1["title"]
            for item in self.cart:
                if item[1] == int(self.data1["BookNo"]):
                    return
            self.w["state"] = "disabled"
            self.bout = self.canvas2.create_rectangle(
                (1283/1600)*(self.scr_width-20),(718/900)*(self.scr_height-60), (1391/1600)*(self.scr_width-20),(790/900)*(self.scr_height-60),
                outline="#5442f5",
                fill="green",
                width=0,
                tags=("booked")
            )
            self.bout1 = self.canvas2.create_text((1337/1600)*(self.scr_width-20),(754/900)*(self.scr_height-60),text="✓",font=("consolas",45))
            self.bout2 = Label(self.root,text="IN CART", font=("Consolas",17),fg="green")
            self.canvas2.create_window((1280/1600)*(self.scr_width-20),(805/900)*(self.scr_height-60),anchor="nw",window=self.bout2)
            self.cart.append((self.mydata.uname,self.data1["BookNo"],self.w.get()))
            self.mydata.addtocart(self.mydata.uname,self.data1["BookNo"],self.w.get())

    def showcart(self):
        self.canvas1.grid_forget()

        h=self.scr_height-60
        if (a:=(220+(100*len(self.cart))+300))>h:
            h = a

        print(h)

        self.canvas3 = Canvas(self.root, width = self.root.winfo_screenwidth()-20,height = self.scr_height-60,relief='flat',highlightthickness=0,scrollregion=(0,0,700,h+300))
        
        self.vbar.grid(row=1, column=1,sticky="NSEW")
        self.vbar.config(command=self.canvas3.yview)
        self.canvas3.config(xscrollcommand=self.hbar.set, yscrollcommand=self.vbar.set,yscrollincrement=10)

        self.canvas3.grid(row=1,column=0,sticky="EW")
        self.canvas3.bind("<Button-1>", self.callback3)

        points = [0,h,self.scr_width,h,self.scr_width,h+320,0,h+320]
        self.canvas3.create_polygon(points,fill="black",outline="grey")
        
        self.bg_image3 = ImageTk.PhotoImage(Image.open(f"images/icons/background 4.jpg").resize((self.scr_width-20,h)))
        self.canvas3.create_image(0,0,image=self.bg_image3,anchor="nw")      

        self.canvas3.create_oval(10,10,60,60, fill="white",outline="grey",activeoutline="cyan",width=3,tags=("arrows"))        
        self.canvas3.create_polygon(
            self.mygui_core.generate_coordinates(15, 15,40,40,"left","arrow"),
            fill = "black",tags=("arrows")
        )

        self.greettext = self.canvas3.create_text(self.scr_width//2,40,text="Welcome! "+self.mydata.uname,font=("Liberation Serif",30))
        self.canvas3.create_line(0,75,self.scr_width,75,width=2,fill="black")

        self.cartlabel = Label(self.root,image=self.cart_logo2)
        self.canvas3.create_window(50,120,window=self.cartlabel)

        self.modeshiftbtn = Button(self.root,text="View Purchases",font=("Liberation Serif",15))
        self.canvas3.create_window(self.scr_width*0.90, 40, window=self.modeshiftbtn)

        #self.modelabel = Label(self.root, text="Your Cart:",font=("Liberation Serif",25))
        self.canvas3.create_text(self.scr_width//8, 120, text="Your Cart:",font=("Liberation Serif",25))


        self.setcart()


    def setcart(self):
        self.frames = []
        self.qtys = []
        self.cartprices = []
        self.delbuttons = []
        for i in range(len(self.cart)):
            entry = self.cart[i]
            data = self.mydata.fetch_bookdetailsid(entry[1])
            if not data:
                data = {"title":self.titles[entry[1]-1],"author":"Ankith Abhayan","price":self.prices[entry[1]-1]}

            menubar = Frame(self.root,height=80,width=self.scr_width*0.7,bg="white",relief='flat')
            menubar["highlightthickness"]=2
            menubar["highlightbackground"]="black"
            menubar.grid_propagate(False)
            title = Label(
                menubar,text=f'{data["title"]} - {data["author"]}',font=("Liberation Serif",20),
                image=self.pixel,
                compound="center", 
                width=(self.scr_width*0.7)*0.65
            )
            self.var = DoubleVar(value=entry[2])
            w = Spinbox(menubar, bg="white",fg="black",font=("Consolas",30),width=1,relief="flat",from_=1,bd=3,to=9,wrap=True,buttondownrelief="flat",buttonuprelief="flat",textvariable=self.var,state="readonly")        
            w["command"] = lambda i=i,data=data:self.editprice2(i,data['price'])
            price = Label(menubar, font=("Liberation Serif",25),text=f"Rs.{int(entry[2])*int(data['price'])}")
            btn = Button(self.root,image=self.closebtn,command=lambda i=i:self.removecart(i),background="black",relief="flat")
            self.delbuttons.append(btn)

            title.grid(row=0,column=0,pady=20)
            w.grid(row=0,column=1,pady=10,padx=40)
            price.grid(row=0,column=2,pady=10,padx=40)

            self.frames.append(menubar)
            self.qtys.append(w)
            self.cartprices.append(price)

        y=220
        for i in range(len(self.frames)):
            self.canvas3.create_window(self.scr_width//2.25,y,window=self.frames[i],tags=("cart"))
            self.canvas3.create_window(self.scr_width*0.824,y,window=self.delbuttons[i],tags=("cart"))
            y+=100

        if len(self.cart)!=0:
            self.confirmbtn = Button(self.root,text="Confirm purchase",bg="#56f545",font=("Liberation Serif",20),relief="flat")
            self.canvas3.create_window(self.scr_width//6,y+50,window=self.confirmbtn,tags=("cart"))

            sum1 = 0
            for lab in self.cartprices:
                sum1+=int(lab["text"][3:])

            self.totalcost = Label(self.root,text=f"Total: {sum1}Rs.",font=("Liberation Serif",35),borderwidth=1,relief="solid")
            self.canvas3.create_window(self.scr_width*0.7,y+50,window=self.totalcost,tags=("cart"))

        self.menubar.lift()

    def removecart(self,i):
        del self.cart[i]
        self.canvas3.delete("cart")
        self.setcart()
        pass

    def showbookdetails(self,book):
        self.data1 = self.mydata.fetch_bookdetails(book)

        self.canvas1.grid_forget()

        self.canvas2 = Canvas(self.root, width = self.root.winfo_screenwidth()-20,height = self.scr_height-60,relief='flat',highlightthickness=0,scrollregion=(0,0,700,(self.scr_height-60)*1.2))

        self.vbar.grid(row=1, column=1,sticky="NSEW")
        self.vbar.config(command=self.canvas2.yview)
        self.canvas2.config(xscrollcommand=self.hbar.set, yscrollcommand=self.vbar.set,yscrollincrement=10)

        self.canvas2.grid(row=1,column=0,sticky="EW")
        self.canvas2.bind("<Button-1>", self.callback2)

        points = [0,self.scr_height-60,self.scr_width,self.scr_height-60,self.scr_width,self.scr_height*1.2,0,self.scr_height*1.2]
        self.canvas2.create_polygon(points,fill="black",outline="grey")
        
        self.bg_image2 = ImageTk.PhotoImage(Image.open(f"images/book/{self.data1['BookNo']}.jpg").resize((self.scr_width-20,self.scr_height-60)))
        self.canvas2.create_image(0,0,image=self.bg_image2,anchor="nw")
        

        #self.canvas2.create_image( 125, 75, image = self.bufferimg,anchor = "nw")

        self.canvas2.create_oval(10,10,60,60, fill="white",outline="grey",activeoutline="cyan",width=3,tags=("arrows"))        
        self.canvas2.create_polygon(
            self.mygui_core.generate_coordinates(15, 15,40,40,"left","arrow"),
            fill = "black",tags=("arrows")
        )

        y = False
        for item in self.cart:
            if item[1] == int(self.data1["BookNo"]):
                k = item
                y = True
                break
            
        self.w=""
        self.var = DoubleVar(value=1)
        self.w = Spinbox(
            self.root, 
            bg="white",
            fg="black",
            font=("Consolas",35),
            width=1,
            relief="flat",
            from_=1,
            to=9,
            bd=0,
            wrap=True,
            buttondownrelief="flat",
            buttonuprelief="flat",
            textvariable=self.var,
            state="readonly",
        )
        self.w['command'] = self.editprice
        self.canvas2.create_window(self.scr_width*0.873, self.scr_height*0.735, anchor = "nw",window=self.w)
        if y:
            self.w.delete(0,"end")
            self.w.insert(0,int(k[2]))
            self.w["from_"] = int(k[2])
            self.var.set(int(k[2]))
            self.w["state"] = "disabled"
            
            self.pricelbl = self.canvas2.create_text(self.scr_width*0.38, self.scr_height*0.72, anchor="nw",text=f"Rs.{int(self.data1['price'])*int(k[2])}",font=("Liberation Serif",50),tags=("price"))
            self.bout = self.canvas2.create_rectangle(
                (1283/1600)*(self.scr_width-20),(718/900)*(self.scr_height-60), (1391/1600)*(self.scr_width-20),(790/900)*(self.scr_height-60),
                outline="#5442f5",
                fill="green",
                width=0,
                tags=("booked")
            )
            self.bout1 = self.canvas2.create_text((1337/1600)*(self.scr_width-20),(754/900)*(self.scr_height-60),text="✓",font=("consolas",45))
            self.bout2 = Label(self.root,text="IN CART", font=("Consolas",17),fg="green")
            self.canvas2.create_window((1280/1600)*(self.scr_width-20),(805/900)*(self.scr_height-60),anchor="nw",window=self.bout2)

        else:
            self.pricelbl = self.canvas2.create_text(self.scr_width*0.38, self.scr_height*0.72, anchor="nw",text=f"Rs.{self.data1['price']}",font=("Liberation Serif",50),tags=("price"))
        self.canvas2.create_text(20,self.scr_height-40, anchor="nw", text="Made by Ankith Abhayan and Rajath Valsan.",fill="grey",font=("Courier New",15))
        self.menubar.lift()
        #

    def editprice2(self,i,price):
        self.cartprices[i]["text"] = f"Rs.{int(price)*int(self.qtys[i].get())}"
        sum1 = 0
        for lab in self.cartprices:
            sum1+=int(lab["text"][3:])

        self.totalcost["text"]=f"Total: {sum1}Rs."
        self.cart[i] = (self.cart[i][0],self.cart[i][1],int(self.qtys[i].get()))

    def editprice(self):
        self.canvas2.delete("price")
        price = int(self.w.get())*int(self.data1['price'])
        self.pricelbl = self.canvas2.create_text(self.scr_width*0.38, self.scr_height*0.72, anchor="nw",text=f"Rs.{price}",font=("Liberation Serif",50),tags=("price"))

    def load_images(self):
        self.search_logo = ImageTk.PhotoImage(Image.open('images/icons/mag.jpg').resize((30,30)))
        self.cart_logo = ImageTk.PhotoImage(Image.open('images/icons/cart.jpg').resize((30, 30)))
        self.cart_logo2 = ImageTk.PhotoImage(Image.open('images/icons/cart.jpg').resize((50, 50)))

        self.closebtn = ImageTk.PhotoImage(Image.open('images/icons/closebtn.png'))
        self.bg_image=ImageTk.PhotoImage(Image.open('images/icons/background 3.jpg').resize((self.scr_width, 1250)))
        self.logoutpic = ImageTk.PhotoImage(Image.open('images/icons/logout.jpg'))
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

        self.cart_icon = Button(self.menubar, image=self.cart_logo,highlightthickness=2, command=self.showcart)
        self.cart_icon.image = self.cart_logo
        self.logout_label = Label(self.menubar,text=self.mydata.uname,font=("consolas",17),bg="#0F1111",fg="white")
        self.logout_button = Button(self.menubar, image=self.logoutpic,command=self.goback)
        self.logout_button.image = self.logoutpic

        self.title.place(relx=0.07,rely=0.5,anchor=CENTER)
        self.searchbox.place(relx=0.40,rely=0.5,anchor=CENTER)
        self.search_icon.place(relx=0.68,rely=0.5,anchor=CENTER)
        self.cart_icon.place(relx=0.73,rely=0.5,anchor=CENTER)
        self.logout_label.place(relx=0.87,rely=0.5,anchor=CENTER)
        self.logout_button.place(relx=0.97,rely=0.5,anchor=CENTER)

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
        

    def goback(self):
        self.root.destroy()
        os.system("python3 main.py")

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
            
        titles = self.mydata.fetch_titles()[0]
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