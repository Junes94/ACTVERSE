import tkinter as tk
from tkinter import simpledialog
from easygui import *
import sys


def extract(data,joint):
    # the input dialog

    joint_num = simpledialog.askstring(title="Data structure",
                                      prompt="How many joints does your data have?:")
    coord_num = simpledialog.askstring(title="Data structure",
                                      prompt="How many dimensions does your data have?:")

    print(joint_num, coord_num)