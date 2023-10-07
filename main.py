
from core import data
from gui import gui_main,gui_core


stop_thread = False




mydata = data.DataClient()

mygui = gui_main.Gui(mydata,gui_core)
mygui.load_images()
mygui.start()



mygui.root.mainloop()