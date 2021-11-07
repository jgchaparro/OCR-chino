# Author: Jaime García Chaparro
# coding=utf-8

# Mandatory parameters
ix, iy, fx, fy = 140, 660, 820, 725 # Screenshot area: initial X, initial Y. final X and final Y.

# Optional parameters
ss_filename = 'OCR_ZW_screenshot.png' # Name of the screenshot. Add extension, preferably .png.
simplified = False # Set to True to detect simplified Chinese. 
macro = 'shift', 'alt', 'o' # Macro combination to integrate with other macro programs.

# ====================

from PIL import ImageGrab
from easyocr import Reader
from pyautogui import hotkey
from pyperclip import copy
import jieba
import os
import numpy

# Initialization and basic variables

print('Initializing.')
script_dir = os.path.dirname(__file__)
img_dir = os.path.join(script_dir, 'Files', ss_filename)

jieba.set_dictionary(os.path.join(script_dir, 'Files', 'dict.txt.big.txt'))

reader = Reader(['ch_tra', 'en'])
if simplified:
    print('Switching to simplified Chinese mode.')
    reader = Reader(['ch_sim', 'en'])

def translate_sub():
    """Translates subtitles.
    Requires subtitiles to be at a spefic location."""
    
    # Take screenshot and extract subtitles
    image = ImageGrab.grab(bbox=(ix, iy, fx, fy))
    #image.save(img_dir)

    #result = reader.readtext(img_dir, detail = 0, paragraph = True)
    result = reader.readtext(numpy.array(image), detail = 0, paragraph = True)
    try:
        subt = ''.join(result)
    except:
        subt = ''

    # Slice with Jieba

    cut_subt = jieba.lcut(subt)
    cut_subt.append(subt) # Full subt at the end
    enum_subt = list(enumerate(cut_subt, 1)) 
    paperclip = ''
    for i, zi in enum_subt:
        paperclip = paperclip + str(i) + ' - ' + zi + '\n'

    copy(paperclip)

    if type(macro) == tuple:
        hotkey(*macro)

    input('Press enter to continue.')

input('Press enter to start.')

while True:
    translate_sub()