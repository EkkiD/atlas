import Tkinter as tk
from PIL import Image, ImageTk
import serial
import re
from StringIO import StringIO
from urllib2 import urlopen
from collections import deque

DISTANCE_THRESHOLD = 100
READING_THRESHOLD = 1


def alleq(iterable):
    return len(set(iterable)) <= 1


class Application(object):
    def __init__(self, master=None):
        self.frame = tk.Tk(master)
        
        self.frame.attributes("-toolwindow", 1)
        self.frame.attributes("-fullscreen", True)
        self.frame.bind("<Escape>", self.destroy)


        self.createImage()

        self.serialInput = serial.Serial('COM4', 9600) # Establish the connection on a specific port

        self.readings = [deque(maxlen=READING_THRESHOLD),
                         deque(maxlen=READING_THRESHOLD),
                         deque(maxlen=READING_THRESHOLD)]

        self.state = [False, False, False]
        self.imageIdx = 0

    def destroy(self, e):
        self.frame.destroy()
        exit(0)

    def createImage(self):
        files = [  
                  'image0.gif',
                  'image1.jpg',
                  'image2.jpg',
                  'image3.jpg',
                  'image4.jpg',
                  'image5.jpg',
                  'image6.jpg',
                  'image7.jpg',
               ]
        self.rawImages = map(lambda f: Image.open(f), files)

        self.tkImage = ImageTk.PhotoImage(self.rawImages[0])
        self.panel = tk.Label(self.frame, image=self.tkImage)
        self.panel.pack()

    def evaluateResults(self):
        requirement = '\d+|\d+|\d+'
        results = self.serialInput.readline() # Read the newest output from the Arduino
        print results
        if not re.match(requirement, results):
            return

        distances = map(lambda x: int(x), results.split('|'))

        for i, distance in enumerate(distances):
            reading = True if distance < DISTANCE_THRESHOLD else False
            self.readings[i].append(reading)

            if alleq(self.readings[i]):
                self.state[i] = self.readings[i][0]

        self.imageIdx = 1 if self.state[0] else 0
        self.imageIdx +=  2 if self.state[1] else 0
        self.imageIdx +=  4 if self.state[2] else 0

    def update(self):
        self.evaluateResults()

        print self.imageIdx
        imageToUse = self.rawImages[self.imageIdx]

        self.rawImage = imageToUse.resize((self.frame.winfo_width(), self.frame.winfo_height()))
        self.tkImage = ImageTk.PhotoImage(self.rawImage)
        self.panel.configure(image = self.tkImage)

        self.frame.after(50, self.update)


    def mainloop(self):
        self.frame.update()
        self.update()
        self.frame.mainloop()


app = Application()
app.mainloop()

