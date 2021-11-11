# Author: Jaime García Chaparro
# coding=utf-8

# Mandatory parameters
ix, iy, fx, fy = 140, 660, 820, 725 # Screenshot area: initial X, initial Y. final X and final Y.

# Optional parameters
ss_filename = 'OCR_ZW_screenshot.png' # Name of the screenshot. Add extension, preferably .png.
simplified = False # Set to True to detect simplified Chinese. 
macro = 'shift', 'alt', 'o' # Macro combination to integrate with other macro programs.
always_slice = False #  Set to True to get the individual characters a word is composed of.

# ====================

from PIL import ImageGrab
from easyocr import Reader
from pyautogui import hotkey
from pyperclip import copy
import jieba
import os
import numpy
import pandas as pd
import re
from functions import *

# Initialization and basic variables

print('Initializing.')
script_dir = os.path.dirname(__file__)
img_dir = os.path.join(script_dir, 'Files', ss_filename)

jieba.set_dictionary(os.path.join(script_dir, 'Files', 'dict.txt.big.txt'))

# Create empty lists for the current article words, zis, pinyins and definitions

current_words, current_indices = [], []

def generate_lists():
    """Creates a list of the words in the dicitonary."""

    print('Generating list and data frame.')

    global df_words
    global full_dic
    global full_dic_simp
    df_words = pd.read_csv(os.path.join(script_dir, 'Files', 'Dictionary 3.2.csv'), sep='\\', encoding='utf-8')
    df_words = df_words.sort_values(by=['freq', 'pinyin'], ascending=[False, False])
    full_dic = df_words.loc[:,'trad'].tolist()
    full_dic_simp = df_words.loc[:,'simp'].tolist()

    print('Lists and data frames generated.')

def process(words):
    """Search the words or characters in the lists."""
    
    n_words = len(words)
    i = 1

    for word in words:
        print(f'Processing word {i} out of {n_words}')
        i += 1
        if word in ['\n', '「', '」', '，', '。'] or (re.search('[0-9]', word) != None):
               pass
        elif word != '':
                search(word)

def search(word, is_zi = False, procedence = 2):
    if len(word) == 1:
        if is_zi == True:
            if procedence != 3:
                procedence = ''
        else:   # Set procedence to 1 if non-zi word is 1 char long.
            procedence = 1

    if word in current_words:
        retrieve_from_current(word, is_zi, procedence)

    elif word in full_dic:
        retrieve_from_dictionary(word, is_zi, procedence)
    
    else:
        out_of_dictionary(word, is_zi)

def extract_info(index):
    if simplified == False:
        word = df_words.iloc[index, 0]
    else:
        word = df_words.iloc[index, 1]

    pinyin = df_words.iloc[index, 2]
    defs = df_words.iloc[index, 3]
    
    return word, pinyin, defs

def retrieve_from_current(word, is_zi = False, procedence = 2):
        i = current_indices[current_words.index(word)]

        word, pinyin, defs = extract_info(i)
        add_word(word, pinyin, defs, is_zi = is_zi, procedence = procedence)

        if always_slice == True and (not is_zi) and len(word) > 1:
            slice_into_zis(word, procedence = "")


def rescue_word(word):
    if len(word) == 2:
        slice_into_zis(word, procedence = 3)

    elif len(word) == 3:
        if word[:2] in full_dic:
            process(word[:2])
            process(word[2])
        elif word[1:] in full_dic:
            process(word[0])
            process(word[1:])
        else:
            slice_into_zis(word, procedence = 3)

    elif len(word) == 4:
        if word[:2] in full_dic and word[2:] in full_dic:
            process(word[:2])
            process(word[2:])
        elif word[:2] in full_dic and word[2:] not in full_dic:
            process(word[:2])
            combined_pinyin = ''
            for zi in word[2:]:
                try:
                    combined_pinyin += (df_words.iloc[(full_dic.index(zi)), 2] + ' ')
                except:
                    combined_pinyin += ' X '
            add_word(word[2:], combined_pinyin, 'X', procedence = 3)
        elif word[:2] not in full_dic and word[2:] in full_dic:
            combined_pinyin = ''
            for zi in word[:2]:
                try:
                    combined_pinyin += (df_words.iloc[(full_dic.index(zi)), 2] + ' ')
                except:
                    combined_pinyin += ' X '
            add_word(word[:2], combined_pinyin, 'X', procedence = 3)
            process(word[2:])
        elif word[:-1] in full_dic:
            process(word[:-1])
            process(word[-1])
        elif word[1:] in full_dic:
            process(word[0])
            process(word[1:])
        else:
            slice_into_zis(word, procedence = 3)
    
    else:
        combined_pinyin = ''
        for zi in word:
            try:
                combined_pinyin += (df_words.iloc[(full_dic.index(zi)), 2] + ' ')
            except:
                combined_pinyin += ' X '
        add_word(word, combined_pinyin, 'X', procedence = 3)

def retrieve_from_dictionary(word, is_zi = False, procedence = 2):
    df_i = full_dic.index(word)

    word, pinyin, defs = extract_info(df_i)

    if is_zi == False:
        add_word(word, pinyin, defs, index = df_i, procedence = procedence)
    else:
        add_word(word, pinyin, defs, procedence = procedence, is_zi = True)

    add_to_current(word, df_i)

    if always_slice == True and is_zi == False and len(word) > 1:
        slice_into_zis(word, procedence = "")

def slice_into_zis(word, procedence = ''):
    for i in range(0, len(word)):
        search(word[i], is_zi = True, procedence = procedence)

def out_of_dictionary(word, is_zi = False):
    if is_zi == False:
        rescue_word(word)

    else:
        add_word(word, 'X', 'Not availible.', procedence = 3)


def add_word(word, pinyin, defs, is_zi = False, procedence = 2):
    pass



#==============

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