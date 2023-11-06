from tkinter import *
import tkinter.font as tkfont
from PIL import ImageTk,Image
from core import data
from gui import gui_main,gui_core
import threading

class Authentication:
    def __init__(self,mydata):
        self.mydata = mydata
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
        self.buttonbusy = False
        self.passout,self.userout = "",""
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
        #self.window.mainloop()
        self.shift()

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
            if self.usernameentry:
                self.usernameentry.destroy()
            if self.passwordentry:
                self.passwordentry.destroy()
            self.usernameentry = ""
            self.passwordentry = ""
            self.bout = self.mycanvas.create_rectangle((597/1600)*self.x,(555/900)*self.y, (986/1600)*self.x,(614/900)*self.y,outline="#5442f5",fill=None,width=0,tags=("self.bout"))

        else:
            if self.buttonbusy:
                return
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
                self.window.after(100, lambda:self.mycanvas.itemconfig(self.bout,outline="#5442f5",width=2))

                mode = "login"
                if self.switch_label['text'][0] == "a":
                    mode = "sign up"

                uname,pass1 = self.fetch_entry()
                if uname=="" and pass1=="":
                    self.show_error("Username and password fields empty",user=True,pass1=True)
                    return

                elif uname=="":
                    self.show_error("Username field empty",user=True)
                    return
                elif pass1=="":
                    self.show_error("Password field empty",pass1=True)
                    return

                if mode == "login":
                    if self.mydata.userexists(uname,pass1):
                        self.show_error("Correct! Loading...",True)
                        
                    else:
                        self.show_error("Incorrect username or password",user=True,pass1=True)

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
        stop_thread = False
        
        mygui = gui_main.Gui(self.mydata,gui_core,self.window,self.mycanvas)
        mygui.load_images()
        mygui.start()    
        mygui.root.mainloop() 
        
    def on_leave(self,*h):
        self.current = ""

    def fetch_entry(self):
        uname,pass1 = "", ""
        if self.usernameentry:
            uname = self.usernameentry.get()
        if self.passwordentry:
            pass1 = self.passwordentry.get()
        return uname, pass1


    def show_error(self,msg,t=False,user=False,pass1=False):
        color = "red"
        if t==True:
            color = "green"
        gap = (35-len(msg))//2
        msg = (" "*gap)+msg+(" "*gap)
        self.errorinfo = Label(self.window, width=35,font=("Consolas",12),highlightthickness=0,relief=FLAT,bg="white",fg=color,text=msg)
        self.mycanvas.create_window(0.375*self.x,0.7*self.y,anchor="nw",window=self.errorinfo)
        if t==True:
            self.window.after(100,self.shift)
        else:
            if user:
                self.userout = self.mycanvas.create_rectangle((597/1600)*self.x,(331/900)*self.y, (986/1600)*self.x,(392/900)*self.y,outline="red",fill=None,width=2,tags=("self.bout"))
            if pass1:
                self.passout = self.mycanvas.create_rectangle((597/1600)*self.x,(406/900)*self.y, (986/1600)*self.x,(471/900)*self.y,outline="red",fill=None,width=2,tags=("self.bout"))
            
            scrlthread = threading.Thread(target=self.deleteerrormsgs,daemon=True)
            self.buttonbusy = True
            self.window.after(1200, scrlthread.start)

    def deleteerrormsgs(self):
        for i in range(1,256):
            color = '#{:02x}{:02x}{:02x}'.format(255, i, i)
            if self.passout:
                self.mycanvas.itemconfig(self.passout,outline=color)
            if self.userout:
                self.mycanvas.itemconfig(self.userout,outline=color)

        self.errorinfo.destroy()
        if self.userout:
            self.mycanvas.delete(self.userout)
        if self.passout:
            self.mycanvas.delete(self.passout)
        self.buttonbusy = False