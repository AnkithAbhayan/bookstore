from core import data
from login import Authentication


mydata = data.DataClient()
client = Authentication(mydata)
client.doit()
