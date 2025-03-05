# Generated with tkedit (tkedit.glitch.me)

import tkinter as tk
from tkinter.filedialog import askopenfilename, asksaveasfilename

from users import *

application_font = ('arial', 12, 'normal')
application_background_colour = '#F0F8FF'

users = Users()

# Get the selected list box value
def getListboxValue():
	itemSelected = OutputListBox.curselection()
	return itemSelected

#**
# Functions
#**
def LoadWordpressFile():
    filename = askopenfilename()
    if filename != '':
        if users.loadWordpressFile( filename ):
            zoomButton["state"] = "normal"
            wordpressButton["state"] = "disabled"


def LoadZoomFile():
    filename = askopenfilename()
    if filename != '':
        if users.loadZoomFile( filename ):
            zoomButton["state"] = "normal"

def SaveCertificate():
    event_name_text = event_name_input.get(1.0, "end-1c")
    event_date_text = event_date_input.get(1.0, "end-1c")
    event_time_hr_text = int(event_time_hr_input.get(1.0, "end-1c"))
    event_time_min_text = int(event_time_min_input.get(1.0, "end-1c"))
    event_time_threshhold_text = int(event_time_threshhold_input.get(1.0, "end-1c"))

    filename = asksaveasfilename(defaultextension=".csv", filetypes=(("CSV file", "*.csv"),("All Files", "*.*") ))
    if filename != '':
        users.exportCertificate( filename, event_name_text, event_date_text, event_time_hr_text, event_time_min_text, event_time_threshhold_text )
    # newFilename = filename.split(".")[0] + "_converted" + filename.split(".")[1]
    # print(newFilename)

def SaveBrevo():
    filename = asksaveasfilename(defaultextension=".csv", filetypes=(("CSV file", "*.csv"),("All Files", "*.*") ))
    if filename != '':
        users.exportBrevo( filename )
    # newFilename = filename.split(".")[0] + "_converted" + filename.split(".")[1]
    # print(newFilename)



#**
# GUI Layout
#**
root = tk.Tk()

root.geometry('480x400')
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
brevoButton = tk.Button(root, text='Save Brevo', bg=application_background_colour, font=application_font, command=SaveBrevo)
brevoButton.place(x=200, y=350)

certificateButton = tk.Button(root, text='Save Cerificate', bg=application_background_colour, font=application_font, command=SaveCertificate)
certificateButton.place(x=15, y=350)

event_name_input = tk.Text(root, height = 5, width = 20) 
event_name_input.place(x=15, y= 200)

event_date_input = tk.Text(root, height = 5, width = 20) 
event_date_input.place(x=15, y= 200)

event_time_hr_input = tk.Text(root, height = 5, width = 20) 
event_time_hr_input.place(x=15, y= 200)

event_time_min_input = tk.Text(root, height = 5, width = 20) 
event_time_min_input.place(x=15, y= 200)

event_time_threshhold_input = tk.Text(root, height = 5, width = 20) 
event_time_threshhold_input.place(x=15, y= 200)

def main():
    root.mainloop()

if __name__ == "__main__":
    main()