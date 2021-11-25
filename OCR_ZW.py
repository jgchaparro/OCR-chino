# Author: Jaime García Chaparro
# coding=utf-8

from PIL import ImageGrab
from easyocr import Reader
from pyautogui import hotkey
from pyperclip import copy
import jieba
import os
import numpy
import pandas as pd
import re
import ctypes
from OCR_functions import *

# Mandatory parameters
ix, iy, fx, fy = 160, 700, 860, 850 # Screenshot area: initial X, initial Y. final X and final Y.
screen_mult = 1

# Optional parameters
ss_filename = 'OCR_ZW_screenshot.png' # Name of the screenshot. Add extension, preferably .png.
simplified = False # Set to True to detect simplified Chinese. 
macro = 'shift', 'alt', 'o' # Macro combination to integrate with other macro programs.
always_slice = False #  Set to True to get the individual characters a word is composed of.

#===============

# Resize variables

ix = ix * screen_mult
iy = iy * screen_mult
fx = fx * screen_mult
fy = fy * screen_mult

# Initialization and basic variables

print('Initializing.')
script_dir = os.path.dirname(__file__)
img_dir = os.path.join(script_dir, 'Files', ss_filename)

jieba.set_dictionary(os.path.join(script_dir, 'Files', 'dict.txt.big.txt'))

#==============

reader = Reader(['ch_tra', 'en'])
if simplified:
    print('Switching to simplified Chinese mode.')
    reader = Reader(['ch_sim', 'en'])

# Tkinter window

user32 = ctypes.windll.user32
screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
root_size = 'x'.join([str(int(elem/2)) for elem in screensize])
root.geometry(root_size) 

generate_lists(script_dir)

canvas = Canvas(root)
canvas.grid(rowspan=24, columnspan=4)

# Header

instructions = Label(root, text = 'test')
instructions.grid(row=0, column=0)

# Configuration and start

#auto_mode variables in functions file
auto_mode_cbx.grid(row=0, column=3, sticky='w')

capture_text = StringVar()
capture_btn = Button(root, textvariable=capture_text, 
            command=lambda: auto_mode(root, reader) if auto_mode_var.get() == 1
                    else translate_sub(root, reader))
capture_text.set('Capture')
capture_btn.grid(row=0, column=2)

# bauto_mode_var = IntVar()
# bauto_mode_text = StringVar()
# bauto_mode_cbx = Checkbutton(root, text= 'Auto mode', variable = auto_mode_var, 
#                             onvalue=1, offvalue=0)
# bauto_mode_cbx.grid(row=0, column=4, sticky='w')

options_text = StringVar()
options_btn = Button(root, textvariable=options_text, command= lambda: process(root, ['我', '喜歡', '中國']))
options_text.set('Options')
options_btn.grid(row=1, column=2, columnspan=1)


delete_text = StringVar()
delete_btn = Button(root, textvariable=delete_text, command= lambda: delete_labels(root))
delete_text.set('Delete')
delete_btn.grid(row=1, column=3, columnspan=1, sticky='w')  

# OCR-ed words

number_title = Label(root, text= 'No.')
number_title.config(font=('Arial', 14))
number_title.grid(row=4, column=0)

chinese_title = Label(root, text= 'Chinese')
chinese_title.config(font=('Arial', 14))
chinese_title.grid(row=4, column=1)

pinyin_title = Label(root, text= 'Pinyin')
pinyin_title.config(font=('Arial', 14))
pinyin_title.grid(row=4, column=2)

translation_title = Label(root, text='Translation', anchor='w')
translation_title.config(font=('Arial', 14))
translation_title.grid(row=4, column=3)

# OCR dictionary

root.mainloop()