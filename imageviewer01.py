#  from Tkinter import Tk
import sys
if sys.version_info.major == 3:
	from tkinter import *
else:
	from Tkinter import *
from PIL import Image

root = Tk()
root.title("viewer")

view = ImageView(root)
view.pack()

image = Image.open(sys.argv[1])

view.setimage(image)
view.config(width=image.size[0], height=image.size[1])

root.mainloop()