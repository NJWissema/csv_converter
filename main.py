from wordpress_user import *

import tkinter
from tkinter.filedialog import askopenfilename

def main():
    user = WordpressUser()
    print("Hello from csv-converter!")
    user.test()


if __name__ == "__main__":
    main()
