from tkinter import *
from PIL import ImageTk,Image

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
        self.current = ""

    def doit(self):
        x=self.window.winfo_screenwidth()
        y=self.window.winfo_screenheight()
        self.x = x
        self.y = y

        self.imasignup = ImageTk.PhotoImage(Image.open("images/sign up.png").resize((x,y)))
        self.imalogin = ImageTk.PhotoImage(Image.open("images/login.png").resize((x,y)))

        self.mycanvas=Canvas(self.window,width=x,height=y,relief="flat",highlightthickness=0)
        self.mycanvas.create_image(0,0,image=self.imalogin,anchor="nw")

        self.switch_label = Label(self.window, text="dont have an account?",font=("Arial Italic Bold",10),fg="#342c5a",bg="#FFFFFF")
        self.mycanvas.create_window(x/1.943, y/1.87, anchor = "nw",window=self.switch_label,tags=("todel"))

        self.mycanvas.pack()
        self.window.mainloop()


    def togglewindowstate(self):
        if self.window.attributes('-fullscreen'):
            self.window.attributes('-fullscreen', False)
        else:
            self.window.attributes('-fullscreen', True)

    def callback(self,event):
        if "label" in self.current:
            yn = self.y/1.87
            if self.switch_label['text'] == "already have an account?":
                text1 = "dont have an account?"
                xn = self.x/1.943
            else:
                text1 = "already have an account?"
                xn = self.x/1.99

            self.mycanvas.delete("todel")
            del self.switch_label
            self.switch_label = Label(self.window, text=text1,font=("Arial Italic Bold",10),fg="#342c5a",bg="#FFFFFF")
            self.mycanvas.create_window(xn, yn, anchor = "nw",window=self.switch_label,tags=("todel"))

            if self.switch_label['text'][0] == "d":
                self.mycanvas.create_image(0,0,image=self.imalogin,anchor="nw")
            else:
                self.mycanvas.create_image(0,0,image=self.imasignup,anchor="nw")

    def on_enter(self,*h):
        self.current = str(h[0].widget)

    def on_leave(self,*h):
        self.current = ""

client = Authentication()
client.doit()