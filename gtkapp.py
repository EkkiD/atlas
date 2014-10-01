from gi.repository import Gtk, Gdk, GLib, GdkPixbuf
from PIL import Image
import re
from collections import deque

DISTANCE_THRESHOLD = 100
READING_THRESHOLD = 1


def alleq(iterable):
    return len(set(iterable)) <= 1


class Application(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Hello World")
        self.connect("key_press_event",self.keyPress)
        

        self.hbox = Gtk.HBox()
        self.hbox.show()
        self.add(self.hbox)

        self.createImage()
        
        self.readings = [deque(maxlen=READING_THRESHOLD),
                         deque(maxlen=READING_THRESHOLD),
                         deque(maxlen=READING_THRESHOLD)]
        self.r2 = '80|80|80'

        self.state = [False, False, False]
        self.imageIdx = 0

        self.is_full = False

        GLib.timeout_add(50, self.update)


    def change(self):
        self.r2 = '11|111|11' if self.r2 == '80|80|80' else '80|80|80'
        print self.r2

    def toggle_fullscreen(self):
        if self.is_full:
            self.is_full = False
            self.unfullscreen()
        else:
            self.is_full = True
            self.fullscreen()

    def createImage(self):
        self.image_files = [  
                  'image0.gif',
                  'image1.jpg',
                  'image2.jpg',
                  'image3.jpg',
                  'image4.jpg',
                  'image5.jpg',
                  'image6.jpg',
                  'image7.jpg',
               ]

        self.image = Gtk.Image()
        self.image.set_from_file(self.image_files[0])
        self.image.show()
        self.hbox.add(self.image)


    def keyPress(self, widget, event):
        key = Gdk.keyval_name(event.get_keyval()[1])
        if key == 'Escape':
            Gtk.main_quit()
            exit(0)
        elif key == 'f':
            self.toggle_fullscreen()
        elif key == 'c':
            self.change()
        

    def evaluateResults(self):
        requirement = '\d+|\d+|\d+'
        results = self.r2 #self.serialInput.readline() # Read the newest output from the Arduino
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
        width, height = self.get_size()
        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(self.image_files[self.imageIdx], width, height)
        self.image.set_from_pixbuf(pixbuf)
        self.image.show()

        return True


    def mainloop(self):
        self.frame.update()
        self.update()
        self.frame.mainloop()


if __name__ == '__main__':
    import signal
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    app = Application()
    app.connect("delete-event", Gtk.main_quit)
    app.show_all()
    Gtk.main()

