#**
# To convert a zoom meeting attendance csv into the desired format
#**
import tkinter
from tkinter.filedialog import askopenfilename, asksaveasfilename

from users import *


#**
# Variables
#**
page = tkinter.Tk()
page.title("Zoom CSV Converter")

users = Users()

#**
# Functions
#**
def loadWordpressFile():
    filename = askopenfilename()
    users.loadWordpressFile(filename)


def loadZoomFile():
    filename = askopenfilename()
    users.loadZoomFile(filename)

def SaveFile():
    filename = asksaveasfilename(defaultextension=".csv", filetypes=(("CSV file", "*.csv"),("All Files", "*.*") ))
    print(filename)
    # newFilename = filename.split(".")[0] + "_converted" + filename.split(".")[1]
    # print(newFilename)

#**
# Widgets
#**
button = tkinter.Button(page, text="Load Wordpress event", command=loadWordpressFile)
button.pack()

button = tkinter.Button(page, text="Load Zoom attendence report", command=loadZoomFile)
button.pack()

button = tkinter.Button(page, text="Save file", command=SaveFile)
button.pack()



def main():
    page.mainloop()

if __name__ == "__main__":
    main()
