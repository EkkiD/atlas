import Tkinter as tk
from PIL import Image, ImageTk
import serial
import re
from StringIO import StringIO
from urllib2 import urlopen


class Application(object):
    def __init__(self, master=None):
        self.frame = tk.Tk(master)
        self.createImage()
        self.serialInput = serial.Serial('/dev/ttyUSB0', 9600) # Establish the connection on a specific port
        self.selectedImage = 1

    def createImage(self):
        urlprefix = 'http://placekitten.com/'
        url1 = urlprefix + '960/540'
        url2 = urlprefix + '1920/1080'
        print url1
        print url2
        self.rawImage1 = Image.open(StringIO(urlopen(url1).read()))
        self.rawImage2 = Image.open(StringIO(urlopen(url2).read()))
        self.tkImage = ImageTk.PhotoImage(self.rawImage1)
        self.panel = tk.Label(self.frame, image=self.tkImage)
        self.panel.pack()

    def evaluateResults(self):
        requirement = '\d+|\d+|\d+'
        results = self.serialInput.readline() # Read the newest output from the Arduino
        if not re.match(requirement, results):
            return

        distances = map(lambda x: int(x), results.split('|'))
        average = sum(distances) / len(distances)
        
        self.selectedImage =  2 if average < 50 else 1


    def update(self):

        self.evaluateResults()

        imageToUse = self.rawImage1 if self.selectedImage == 1 else self.rawImage2

        print self.frame.winfo_width(), self.frame.winfo_height()
        self.rawImage = imageToUse.resize((self.frame.winfo_width(), self.frame.winfo_height()))
        self.tkImage = ImageTk.PhotoImage(self.rawImage)
        self.panel.configure(image = self.tkImage)

        self.frame.after(100, self.update)


    def mainloop(self):
        self.frame.update()
        self.update()
        self.frame.mainloop()


app = Application()
app.mainloop()

