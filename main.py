
from core import data
from login import Authentication

#stop_thread = False
mydata = data.DataClient()
client = Authentication(mydata)
client.doit()
#client.shift()

#mygui = gui_main.Gui(mydata,gui_core)
#mygui.load_images()
#mygui.start()

#mygui.root.mainloop()