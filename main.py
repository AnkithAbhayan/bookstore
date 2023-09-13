from tkinter import *
from PIL import ImageTk, Image
import threading
import time

root = Tk()
stop_thread = False
root.geometry('1366x768')
root.title("Bookshop")

class Gui:
    def __init__(self):
        pass

    def bgchange(self):
        r,g,b=255,255,255
        f=False
        for i in range(75): #red
            b -= 1
            g -= 1
            time.sleep(0.01)
            root["bg"] = rgb_to_hex(r, g, b)

        for i in range(75): #green
            g+=1
            r-=1
            time.sleep(0.01)
            root["bg"] = rgb_to_hex(r, g, b)

        for i in range(75): #blue
            b += 1
            g -= 1
            time.sleep(0.01)
            root["bg"] = rgb_to_hex(r, g, b)

        for i in range(75):
            r+=1
            g+=1
            time.sleep(0.01)
            root["bg"] = rgb_to_hex(r, g, b)

        root["bg"] = rgb_to_hex(255, 255, 255)

    def start(self):
        self.mainlogo=Image.open('images\\logo.jpg').resize((200, 200))
        self.mainlogo=ImageTk.PhotoImage(self.mainlogo)



        #self.mainicon = Frame(root, height=1366, width=768, bg="#f5f5dc")
        #self.mainicon.grid(row=0,column=0)

        self.mainlogopic = Label(root,image=self.mainlogo,bg="#f5f5dc")
        self.mainlogopic.image = self.mainlogo
        self.mainlogopic.place(relx=.5, rely=.5,anchor= CENTER)
        t = threading.Thread(target=self.bgchange, daemon=True)
        t.start()
        self.mainlogopic.after(5000, self.load_screen)
        
    def load_screen(self):
        global stop_thread
        stop_thread = True
        self.mainlogopic.destroy()
        self.menubar = Frame(root,height=60,width=10000,bg="#0F1111")
        self.menubar.grid(row=0,column=0)

        self.title = Label(
            self.menubar,
            text="BOOKSHOP",
            font=("Arial Bold Italic",20),
            fg=rgb_to_hex(255,255,255),
            bg="#0F1111",
        )

        self.searchbox = Entry(
            self.menubar,
            width=60,
            font=("Consolas",15),
        )
        self.search_logo = Image.open('images\\mag.jpg')
        self.search_logo = ImageTk.PhotoImage(self.search_logo)

        
        self.search_icon = Button(self.menubar, image=self.search_logo, command = self.search)
        self.search_icon.image = self.search_logo
        self.searchbox.place(x=250,y=13)
        self.title.place(x=10,y=10)
        self.search_icon.place(x=930,y=11)



    def search(self,*h):
        print("you seached:",self.searchbox.get())
        self.searchbox.delete(0,'end')


def rgb_to_hex(r, g, b):
    return '#{:02x}{:02x}{:02x}'. format(r, g, b)




mygui = Gui()
mygui.start()




root.bind('<Return>', mygui.search)
root.mainloop()