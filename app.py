import Tkinter as tk
from PIL import Image, ImageTk

class Application(object):
    def __init__(self, master=None):
        self.frame = tk.Tk(master)
        self.createWidgets()
        self.createImage()

    def createWidgets(self):
        self.quitButton = tk.Button(self.frame, text="Quit", command=self.frame.quit)
        self.quitButton.pack()


    def createImage(self):
        self.rawImage = Image.open('placekitten.jpg')
        self.tkInage = ImageTk.PhotoImage(self.rawImage)
        self.panel = tk.Label(self.frame, image=self.tkInage)
        self.panel.pack()

    def update(self):
        self.frame.after(1000, self.update)
        self.rawImage = self.rawImage.resize((self.frame.winfo_width(), self.frame.winfo_height()))
        self.tkImage = ImageTk.PhotoImage(self.rawImage)
        self.panel.configure(image = self.tkImage)


    def mainloop(self):
        self.frame.update()
        self.update()
        self.frame.mainloop()


app = Application()
app.mainloop()

