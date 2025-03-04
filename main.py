# Generated with tkedit (tkedit.glitch.me)

import tkinter as tk
from tkinter.filedialog import askopenfilename, asksaveasfilename

from users import *

application_font = ('arial', 12, 'normal')
application_background_colour = '#F0F8FF'

users = Users()

wordpressButton: tk.Button
zoomButton: tk.Button

# Get the selected list box value
def getListboxValue():
	itemSelected = OutputListBox.curselection()
	return itemSelected

#**
# Functions
#**
def LoadWordpressFile():
    filename = askopenfilename()
    if users.loadWordpressFile(filename):
        zoomButton["state"] = "normal"
        wordpressButton["state"] = "disabled"


def LoadZoomFile():
    filename = askopenfilename()
    if users.loadZoomFile(filename):
        zoomButton["state"] = "normal"

def SaveFile():
    filename = asksaveasfilename(defaultextension=".csv", filetypes=(("CSV file", "*.csv"),("All Files", "*.*") ))
    print(filename)
    # newFilename = filename.split(".")[0] + "_converted" + filename.split(".")[1]
    # print(newFilename)


#**
# GUI Layout
#**
root = tk.Tk()

root.geometry('1024x600')
root.configure(background= application_background_colour)
root.title('Zoom CSV Converter')


# Create a button
wordpressButton = tk.Button(root, text='Upload Wordpress .csv', bg=application_background_colour, font=application_font, command=LoadWordpressFile)
wordpressButton.place(x=15, y=15)

# Create a button
zoomButton = tk.Button(root, text='Upload Zoom Attendance .csv', bg=application_background_colour, font=application_font, command=LoadZoomFile)
zoomButton["state"] = "disabled"
zoomButton.place(x=200, y=15)

# Create a listbox
OutputListBox=tk.Listbox(root, bg=application_background_colour, font=application_font, width=0, height=0)
OutputListBox.place(x=15, y=60)

# Create a button
tk.Button(root, text='Save', bg=application_background_colour, font=application_font, command=SaveFile).place(x=604, y=425)



def main():
    root.mainloop()

if __name__ == "__main__":
    main()