from tkinter import *
from PIL import ImageTk, Image
root = Tk()

root.geometry('1366x768')
root.title("Bookshop")

class Gui:
    def __init__(self):
        pass

    def start(self):
        mainlogo1=Image.open('logo.jpg').resize((100, 100))
        mainlogo=ImageTk.PhotoImage(mainlogo1)


        self.mainicon = Frame(root, height=1366, width=768, bg="#f5f5dc")
        self.mainicon.grid(row=0,column=0)

        self.mainlogopic = Label(self.mainicon,image=mainlogo,bg="#f5f5dc")
        self.mainlogopic.place(x=600,y=700, anchor=CENTER)

        self.mainicon.after(3000, self.load_screen)
        
    def load_screen(self):
        self.mainicon.destroy()
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
        image=Image.open('mag.png').resize((30, 30))
        my_img=ImageTk.PhotoImage(image)

        
        self.search_icon = Button(self.menubar, image=my_img, command = self.search)

        self.searchbox.place(x=250,y=13)
        self.title.place(x=10,y=10)
        self.search_icon.place(x=990,y=11)

    def search(self,*h):
        print("you seached:",self.searchbox.get())
        self.searchbox.delete(0,'end')


def rgb_to_hex(r, g, b):
    return '#{:02x}{:02x}{:02x}'. format(r, g, b)




mygui = Gui()
mygui.start()




root.bind('<Return>', mygui.search)
root.mainloop()
print("hello")
