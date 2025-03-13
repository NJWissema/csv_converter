# Generated with tkedit (tkedit.glitch.me)

import tkinter as tk
from tkinter.filedialog import askopenfilename, asksaveasfilename
import sys

from users import *

application_font = ('arial', 12, 'normal')
application_background_colour = '#F0F8FF'

users = Users()

#**
# Functions
#**
def LoadWordpressFile():
    filename = askopenfilename()
    if filename != '':
        if users.loadWordpressFile( filename ):
            zoomButton["state"] = "normal"
            wordpressButton["state"] = "disabled"
            print(f"Finished with Wordpress upload. Successful")
        else:
            print(f"FAILED. Please restart and retry")


def LoadZoomFile():
    filename = askopenfilename()
    if filename != '':
        if users.loadZoomFile( filename ):
            zoomButton["state"] = "normal"
            print(f"Finished with attendance upload. Successful")
        else:
            print(f"FAILED. Please restart and retry")

def SaveParticipantCertificate():
    event_name_text = event_name_input.get(1.0, "end-1c")
    event_date_text = event_date_input.get(1.0, "end-1c")
    event_time_hr_text = event_time_hr_input.get(1.0, "end-1c")
    event_time_min_text = int(event_time_min_input.get(1.0, "end-1c"))
    event_time_threshhold_text = int(event_time_threshhold_input.get(1.0, "end-1c"))

    filename = asksaveasfilename(defaultextension=".csv", filetypes=(("CSV file", "*.csv"),("All Files", "*.*") ))
    if filename != '':
        users.exportParticipantCertificate( filename, event_name_text, event_date_text, event_time_hr_text, event_time_min_text, event_time_threshhold_text )
    # newFilename = filename.split(".")[0] + "_converted" + filename.split(".")[1]
    # print(newFilename)

def SavePanalistCertificate():
    event_name_text = event_name_input.get(1.0, "end-1c")
    event_date_text = event_date_input.get(1.0, "end-1c")
    event_time_hr_text = event_time_hr_input.get(1.0, "end-1c")
    event_time_min_text = int(event_time_min_input.get(1.0, "end-1c"))

    filename = asksaveasfilename(defaultextension=".csv", filetypes=(("CSV file", "*.csv"),("All Files", "*.*") ))
    if filename != '':
        users.exportPanalistCertificate( filename, event_name_text, event_date_text, event_time_hr_text, event_time_min_text )
    # newFilename = filename.split(".")[0] + "_converted" + filename.split(".")[1]
    # print(newFilename)

def SaveBrevo():
    filename = asksaveasfilename(defaultextension=".csv", filetypes=(("CSV file", "*.csv"),("All Files", "*.*") ))
    if filename != '':
        users.exportBrevo( filename )
    # newFilename = filename.split(".")[0] + "_converted" + filename.split(".")[1]
    # print(newFilename)

class Consoleredirect:
    def __init__(self, console):
        self.console = console
    def write(self, msg):
        console["state"] = "normal"
        self.console.insert(tk.END, msg)
        self.console.see(tk.END)
        console["state"] = "disabled"
    def flush(self):
        pass

#**
# GUI Layout
#**
root = tk.Tk()

# root.geometry('960x400')
root.configure(background= application_background_colour)
root.title('Zoom CSV Converter')

main_frame = tk.Frame(root, bg=application_background_colour, height=480)
main_frame.pack(side=tk.TOP, fill="x")

save_frame = tk.Frame(root, bg=application_background_colour, height=480)
save_frame.pack(side=tk.TOP, fill="x")

console_frame = tk.Frame(root, bg=application_background_colour, height=480)
console_frame.pack(side=tk.TOP, fill="x")

console = tk.Text(console_frame, font=application_font, wrap="word",state='disabled')
console.pack(side=tk.LEFT)
redirected = Consoleredirect(console)
sys.stdout = redirected

# Create a button
wordpressButton = tk.Button(main_frame, text='Upload Wordpress .csv', bg=application_background_colour, font=application_font, command=LoadWordpressFile)
wordpressButton.grid(row=0, column=0)

# Create a button
zoomButton = tk.Button(main_frame, text='Upload Zoom Attendance .csv', bg=application_background_colour, font=application_font, command=LoadZoomFile)
zoomButton["state"] = "disabled"
zoomButton.grid(row=0, column=1)

# Create a listbox
# OutputListBox=tk.Listbox(root, bg=application_background_colour, font=application_font, width=0, height=0)
# OutputListBox.pack()

#Input fields
event_name_frame = tk.Frame(main_frame, bg=application_background_colour)
event_name_label = tk.Label(event_name_frame, text="Event Name", bg=application_background_colour)
event_name_label.pack(side=tk.LEFT)
event_name_input = tk.Text(event_name_frame, width=20, height=1) 
event_name_input.pack(side=tk.RIGHT)
event_name_frame.grid(row=1, column=0)


event_date_frame = tk.Frame(main_frame, bg=application_background_colour)
event_date_label = tk.Label(event_date_frame, text="Event Date", bg=application_background_colour)
event_date_label.pack(side=tk.LEFT)
event_date_input = tk.Text(event_date_frame, width=20, height=1) 
event_date_input.pack(side=tk.RIGHT)
event_date_frame.grid(row=2, column=0)

event_time_hr_frame = tk.Frame(main_frame, bg=application_background_colour)
event_time_hr_label = tk.Label(event_time_hr_frame, text="Event Time (in text)", bg=application_background_colour)
event_time_hr_label.pack(side=tk.LEFT)
event_time_hr_input = tk.Text(event_time_hr_frame, width=20, height=1) 
event_time_hr_input.pack(side=tk.RIGHT)
event_time_hr_frame.grid(row=3, column=0)
# event_time_hr_input.pack()

event_time_min_frame = tk.Frame(main_frame, bg=application_background_colour)
event_time_min_label = tk.Label(event_time_min_frame, text="Event Time (mins)", bg=application_background_colour)
event_time_min_label.pack(side=tk.LEFT)
event_time_min_input = tk.Text(event_time_min_frame, width=20, height=1) 
event_time_min_input.pack(side=tk.RIGHT)
event_time_min_frame.grid(row=4, column=0)
# event_time_min_input.pack()

event_time_threshhold_frame = tk.Frame(main_frame, bg=application_background_colour)
event_time_threshhold_label = tk.Label(event_time_threshhold_frame, text="Full event Threshhold (min)", bg=application_background_colour)
event_time_threshhold_label.pack(side=tk.LEFT)
event_time_threshhold_input = tk.Text(event_time_threshhold_frame, width=20, height=1) 
event_time_threshhold_input.pack(side=tk.RIGHT)
event_time_threshhold_frame.grid(row=5, column=0)
# event_time_threshhold_input.pack()

# Create a button
brevoButton = tk.Button(save_frame, text='Save Brevo', bg=application_background_colour, font=application_font, command=SaveBrevo)
brevoButton.grid(row=0, column=0)

certificateButton = tk.Button(save_frame, text='Save Part Cerificates', bg=application_background_colour, font=application_font, command=SaveParticipantCertificate)
certificateButton.grid(row=0, column=1)

certificateButton = tk.Button(save_frame, text='Save Panal Cerificates', bg=application_background_colour, font=application_font, command=SavePanalistCertificate)
certificateButton.grid(row=0, column=2)

def main():
    root.mainloop()

if __name__ == "__main__":
    main()