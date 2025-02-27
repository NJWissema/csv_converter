#**
# To convert a zoom meeting attendance csv into the desired format
#**
import tkinter
from tkinter.filedialog import askopenfilename


#**
# Variables
#**
page = tkinter.Tk()
page.title("Zoom CSV Converter")

filename : str = ""

#**
# Functions
#**
def loadFile():
    filename = askopenfilename()
    print(filename)

def SaveFile():
    print(filename)
    # newFilename = filename.split(".")[0] + "_converted" + filename.split(".")[1]
    # print(newFilename)

#**
# Widgets
#**
button = tkinter.Button(page, text="Load file", command=loadFile)
button.pack()

button = tkinter.Button(page, text="Save file", command=SaveFile)
button.pack()

page.mainloop()