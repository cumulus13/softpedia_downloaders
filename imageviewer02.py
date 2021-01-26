#!c:/SDK/Anaconda2/python.exe
import glob
import sys
if sys.version_info.major == 3:
    import tkinter as tk
else:
    import Tkinter as tk

from PIL import Image, ImageTk

class Viewer(object):
    def __init__(self, master):
        self.labels = []
        self.n = 1
        self.images = glob.glob("temp/*.png")
        self.master = master

    def setThumb(self, im):
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        if screen_width < im.size[0]:
            x = screen_width / 2
            y = screen_height / 2
        else:
            x = im.size[0] /  1.5
            y = im.size[1] / 1.5
            
        im.thumbnail((x, y), Image.ANTIALIAS)

    def quitX(self, event):
        self.master.destroy()
        sys.exit()
    
    def run(self, event):
        self.show(self.n)
        self.n += 1
    
    def show(self, n):
        jpeg = self.images[n-1]
        print "jpeg =", jpeg
        self.n = self.n + 1
        im = Image.open(jpeg)
        #im.thumbnail((96, 170), Image.ANTIALIAS)
        self.setThumb(im)
        photo = ImageTk.PhotoImage(im)
        label = tk.Label(self.master, image=photo)
        label.pack()    
        label.img = photo # *
        # * Each time thru the loop, the name 'photo' has a different
        # photoimage assigned to it.
        # This means that you need to create a separate, 'longer-lived'
        # reference to each photoimage in order to prevent it from
        # being garbage collected.
        # Note that simply passing a photoimage to a Tkinter widget
        # is not enough to keep that photoimage alive.    
        self.labels.append(label)

if __name__ == '__main__':    
    root = tk.Tk()
    c = Viewer(root)
    root.bind("n", c.run)
    root.bind("q", c.quitX)
    root.mainloop()