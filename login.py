from tkinter import *
import tkinter.font as tkfont
from PIL import ImageTk,Image
from core import data
from gui import gui_main,gui_core

class Authentication:
    def __init__(self):
        self.window=Tk()
        self.window.title("LOGIN")
        self.window.attributes("-fullscreen",True)
        self.window.configure(bg="#333333")
        self.window.bind("<F11>",lambda event:self.togglewindowstate())
        self.window.bind("<Button-1>", self.callback)
        self.window.bind_all('<Enter>',self.on_enter)
        self.window.bind_all('<Leave>',self.on_leave)
        self.usernameentry=None
        self.passwordentry=None
        self.current = ""
        font = tkfont.Font(family="Consolas", size=15, weight="normal")
        self.m_len = font.measure("0")



    def doit(self):
        x=self.window.winfo_screenwidth()
        y=self.window.winfo_screenheight()
        self.x = x
        self.y = y

        
        self.imalogin = ImageTk.PhotoImage(Image.open(r"images/LOGIN.png").resize((x,y)))
        self.imasignup = ImageTk.PhotoImage(Image.open(r"images/sign up.png").resize((x,y)))

        self.mycanvas=Canvas(self.window,width=x,height=y,relief="flat",highlightthickness=0)
        self.mycanvas.create_image(0,0,image=self.imalogin,anchor="nw")

        self.switch_label = Label(self.window, text="dont have an account?",font=("Arial Italic Bold",10),fg="#342c5a",bg="#FFFFFF")
        self.mycanvas.create_window(x/1.943, y/1.87, anchor = "nw",window=self.switch_label,tags=("todel"))
        self.bout = self.mycanvas.create_rectangle(
            (597/1600)*self.x,(555/900)*self.y, (986/1600)*self.x,(614/900)*self.y,
            outline="#5442f5",
            fill=None,
            width=0,
            tags=("self.bout")
        )


        self.mycanvas.bind('<Motion>', self.motion)
            #x.bind('<Enter>', lambda x: self.OnHover(x))tagOrId
            #x.bind('<Leave>', lambda x: self.UnHover(x))
        #self.mycanvas.tag_bind("outline", '<Enter>', lambda event: self.OnHover(event.widget))
        #self.mycanvas.tag_bind("outline", '<Leave>', lambda event: self.UnHover(event.widget))        
        self.mycanvas.pack()
        self.window.mainloop()

    def togglewindowstate(self):
        if self.window.attributes('-fullscreen'):
            self.window.attributes('-fullscreen', False)
        else:
            self.window.attributes('-fullscreen', True)

    def motion(self,event):
        x, y = event.x, event.y
        x = x*(1600/self.x)
        y = y*(900/self.y)
        if x>=597 and x<=984 and y>=555 and y<=614:
            self.mycanvas.itemconfig(self.bout, width=2)
        else:
            self.mycanvas.itemconfig(self.bout,width=0)     

    def callback(self,event):
        if "label" in self.current:
            yn = self.y/1.87
            if self.switch_label['text'] == "already have an account?":
                text1 = "dont have an account?"
                xn = self.x/1.943
            else:
                text1 = "already have an account?"
                xn = self.x/1.999

            self.mycanvas.delete("todel")
            del self.switch_label
            self.switch_label = Label(self.window, text=text1,font=("Arial Italic Bold",10),fg="#342c5a",bg="#FFFFFF")
            self.mycanvas.create_window(xn, yn, anchor = "nw",window=self.switch_label,tags=("todel"))

            if self.switch_label['text'][0] == "d":
                self.mycanvas.create_image(0,0,image=self.imalogin,anchor="nw")
            else:
                self.mycanvas.create_image(0,0,image=self.imasignup,anchor="nw")
            self.bout = self.mycanvas.create_rectangle((597/1600)*self.x,(555/900)*self.y, (986/1600)*self.x,(614/900)*self.y,outline="#5442f5",fill=None,width=0,tags=("self.bout"))

        else:
            x = self.mycanvas.canvasx(event.x)
            x = x*(1600/self.x)
            y = self.mycanvas.canvasy(event.y)
            y = y*(900/self.y)
            
            nchars = round((0.21*self.x)/self.m_len)
            if x>=600 and x<=975 and y>=340 and y<=380:
                if not self.usernameentry:
                    self.usernameentry = Entry(self.window, width=nchars,font=("Consolas",15),highlightthickness=0,relief=FLAT,bg="#e7e7e7",fg="#393747")
                    self.mycanvas.create_window(0.385*self.x,0.384*self.y,anchor="nw",window=self.usernameentry)
                    self.usernameentry.focus_set()
                if self.passwordentry and self.passwordentry.get()=="":
                    self.padentry.destroy()
                    self.passwordentry = None

            #515,363
            elif x>=600 and x<=975 and y>=415 and y<=465:
                if not self.passwordentry:
                    self.passwordentry = Entry(self.window, width=nchars,font=("Consolas",15),highlightthickness=0,relief=FLAT,bg="#e7e7e7",fg="#393747",show="*")
                    self.mycanvas.create_window(0.385*self.x,0.47*self.y,anchor="nw",window=self.passwordentry)
                    self.passwordentry.focus_set()
                if self.usernameentry and self.usernameentry.get()=="":
                    self.usernameentry.destroy()
                    self.usernameentry = None

            elif x>=597 and x<=984 and y>=555 and y<=614:
                self.mycanvas.itemconfig(self.bout,outline="white",width=4)
                self.window.after(100,self.shift)
                #self.mycanvas.itemconfig(self.bout,outline="#5442f5")  
                #self.window.destroy()
           

            else:
                if self.usernameentry and self.usernameentry.get()=="":                    
                    self.usernameentry.destroy()
                    self.usernameentry = None
                if self.passwordentry and self.passwordentry.get()=="":
                    self.passwordentry.destroy()
                    self.passwordentry = None

    def on_enter(self,*h):
        self.current = str(h[0].widget)
    
    def shift(self):
        self.mycanvas.itemconfig(self.bout,outline="#5442f5",width=2)
        stop_thread = False
        mydata = data.DataClient()
        mygui = gui_main.Gui(mydata,gui_core,self.window,self.mycanvas)
        mygui.load_images()
        mygui.start()    
        mygui.root.mainloop() 
        
    def on_leave(self,*h):
        self.current = ""

