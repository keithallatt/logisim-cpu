"""

IDE.PY

IDE for assembly for the 4-bit cpu designed in Logisim. The objective of this
is to be able to write, run, and test code without a physical board.

Written by: Keith Allatt
Date:       January 31st, 2019

Tasks:
    - Create a window to write and re-write code
    - Be able to pass code to a virtual board.
    - Memory Allocation
        - Create custom command for allocating a memory slot and use that
          reference later to facilitate jumps and memory access
    - Create path for programming the board (least number of switch flipping)
        - This is completely optional but would be interesting to implement

"""

from tkinter import *
from plistlib import *
import os


""" Write config info as a p-list file. """


def write_to_plist(value: Dict, filepath: str):
    dump(value, open(filepath, 'wb'))


""" Read config file as a p-list file. """


def read_plist(filepath: str):
    if os.path.isfile(filepath):
        pass  # read plist
    else:
        pass  # config DNE


class IDE_GUI:
    def __init__(self, master):
        self.master = master
        master.title("ASSEMBLY IDE")
        master.geometry("500x500") # controls size

        self.text_window = Text(master=master)
        self.text_window.pack()


    def greet(self):
        print("Greetings!")