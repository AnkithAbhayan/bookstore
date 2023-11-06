
#from core import data
#from gui import gui_main,gui_core
from login import Authentication

#stop_thread = False
client = Authentication()
client.doit()
#mydata = data.DataClient()

#mygui = gui_main.Gui(mydata,gui_core)
#mygui.load_images()
#mygui.start()

#mygui.root.mainloop()