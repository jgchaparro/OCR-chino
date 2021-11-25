from tkinter import *
import pandas as pd
import os
import re
from PIL import ImageGrab
from easyocr import Reader
from pyautogui import hotkey
from pyperclip import copy
import jieba
import numpy
import time

# Tkinter base

root = Tk()

# Translation functions

last_OCR = 'dummy_text!'
ix, iy, fx, fy = 85, 700, 870, 850

def read_ocr(reader):
    """Takes and reads screenshot."""
    global ix, iy, fx, fy
    global last_OCR

    print('Reading screen.')
    image = ImageGrab.grab(bbox=(ix, iy, fx, fy))
    #image.save(r'C:\Users\jgcha\Desktop\Python\Python\OCR chino\Files\OCR_ZW_screenshot.png')

    #result = reader.readtext(img_dir, detail = 0, paragraph = True)
    raw_ocr_result = reader.readtext(numpy.array(image), detail = 0, paragraph = True)
    
    try:
        ocr_result = ''.join(raw_ocr_result)
    except:
        ocr_result = ''

    return ocr_result

def process_ocr(root, ocr_result):
    """Slices with Jieba the results of the OCR screen reader."""
    # Slice with Jieba


    cut_subt = jieba.lcut(ocr_result)
    print(cut_subt)
    process(root, cut_subt)

def translate_sub(root, reader):
    """Merges read_ocr and process_ocr"""

    delete_labels(root)

    ocr_result = read_ocr(reader)
    process_ocr(root, ocr_result)

# Tkinter variables

no_i = 1
row = 5

auto_mode_var = IntVar()
auto_mode_text = StringVar()
auto_mode_cbx = Checkbutton(root, text= 'Auto mode', variable = auto_mode_var, 
                            onvalue=1, offvalue=0)


# Tkinter functions

def delete_labels(root):
    for label in root.grid_slaves():
        if int(label.grid_info()["row"]) > 4:
            label.grid_forget()
    
    global no_i
    global row

    no_i = 1
    row = 5

def add_word(root, word, pinyin, translation, is_zi = False, procedence = 2):
    global row
    global no_i

    no_label = Label(root, text=no_i)
    no_label.config(font=('Arial', 14))
    no_label.grid(row = row, column=0)

    word_label = Label(root, text=word)
    word_label.config(font=('DengXian', 14))
    word_label.grid(row=row, column=1)

    pinyin_label = Label(root, text=pinyin)
    pinyin_label.config(font=('Arial', 14))
    pinyin_label.grid(row=row, column=2)

    translation_label = Label(root, text=translation, anchor='w')
    translation_label.config(font=('Arial', 14))
    translation_label.grid(row=row, column=3, sticky= W)

    row += 1
    no_i += 1

def auto_mode(root, reader):
    global last_OCR
    global auto_mode_var

    if auto_mode_var.get() == 1:
        temp_subt = read_ocr(reader)

        if last_OCR != temp_subt and temp_subt != '':
            delete_labels(root)
            last_OCR = temp_subt           
            process_ocr(root, temp_subt)
        
        root.after(100, auto_mode, root, reader)

def simple_or_auto_translation(auto_var, root, reader):
    if auto_var.get():
        auto_mode()
    else:
        translate_sub(root, reader)

# Dictionary variables

always_slice = False
simplified = False

current_words = []
current_indices = []


# Dictionary functions

def generate_lists(script_dir):
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

def process(root, words):
    """Search the words or characters in the lists."""
    
    n_words = len(words)
    i = 1

    for word in words:
        print(f'Processing word {i} out of {n_words}')
        i += 1
        if word in ['\n', '「', '」', '，', '。'] or (re.search('[0-9]', word) != None):
               pass
        elif word != '':
                search(root, word)

def search(root, word, is_zi = False, procedence = 2):
    if len(word) == 1:
        if is_zi == True:
            if procedence != 3:
                procedence = ''
        else:   # Set procedence to 1 if non-zi word is 1 char long.
            procedence = 1

    if word in current_words:
        retrieve_from_current(root, word, is_zi, procedence)

    elif word in full_dic:
        retrieve_from_dictionary(root, word, is_zi, procedence)
    
    else:
        out_of_dictionary(root, word, is_zi)


def retrieve_from_current(root, word, is_zi = False, procedence = 2):
        i = current_indices[current_words.index(word)]

        word, pinyin, defs = extract_info(i)
        add_word(root, word, pinyin, defs, is_zi = is_zi, procedence = procedence)

        if always_slice == True and (not is_zi) and len(word) > 1:
            slice_into_zis(root, word, procedence = "")

def extract_info(index):
    if simplified == False:
        word = df_words.iloc[index, 0]
    else:
        word = df_words.iloc[index, 1]
    pinyin = df_words.iloc[index, 2]
    defs = df_words.iloc[index, 3]
    
    return word, pinyin, defs

def slice_into_zis(root, word, procedence = ''):
    for i in range(0, len(word)):
        search(root, word[i], is_zi = True, procedence = procedence)

def retrieve_from_dictionary(root, word, is_zi = False, procedence = 2):
    df_i = full_dic.index(word)

    word, pinyin, defs = extract_info(df_i)

    if is_zi == False:
        add_word(root, word, pinyin, defs, procedence = procedence)
    else:
        add_word(root, word, pinyin, defs, procedence = procedence, is_zi = True)

    add_to_current(word, df_i)

    if always_slice == True and is_zi == False and len(word) > 1:
        slice_into_zis(root, word, procedence = "")

def add_to_current(word, index):
    current_words.append(word)
    current_indices.append(index)

def out_of_dictionary(root, word, is_zi = False):
    if is_zi == False:
        rescue_word(root, word)
    else:
        add_word(root, word, 'X', 'Not availible.', procedence = 3)

def rescue_word(root, word):
    if len(word) == 2:
        slice_into_zis(root, word, procedence = 3)

    elif len(word) == 3:
        if word[:2] in full_dic:
            process(root, word[:2])
            process(root, word[2])
        elif word[1:] in full_dic:
            process(root, word[0])
            process(root, word[1:])
        else:
            slice_into_zis(root, word, procedence = 3)

    elif len(word) == 4:
        if word[:2] in full_dic and word[2:] in full_dic:
            process(root, word[:2])
            process(root, word[2:])
        elif word[:2] in full_dic and word[2:] not in full_dic:
            process(root, word[:2])
            combined_pinyin = ''
            for zi in word[2:]:
                try:
                    combined_pinyin += (df_words.iloc[(full_dic.index(zi)), 2] + ' ')
                except:
                    combined_pinyin += ' X '
            add_word(root, word[2:], combined_pinyin, 'X', procedence = 3)
        elif word[:2] not in full_dic and word[2:] in full_dic:
            combined_pinyin = ''
            for zi in word[:2]:
                try:
                    combined_pinyin += (df_words.iloc[(full_dic.index(zi)), 2] + ' ')
                except:
                    combined_pinyin += ' X '
            add_word(root, word[:2], combined_pinyin, 'X', procedence = 3)
            process(root, word[2:])
        elif word[:-1] in full_dic:
            process(root, word[:-1])
            process(root, word[-1])
        elif word[1:] in full_dic:
            process(root, word[0])
            process(root, word[1:])
        else:
            slice_into_zis(root, word, procedence = 3)
    
    else:
        combined_pinyin = ''
        for zi in word:
            try:
                combined_pinyin += (df_words.iloc[(full_dic.index(zi)), 2] + ' ')
            except:
                combined_pinyin += ' X '
        add_word(root, word, combined_pinyin, 'X', procedence = 3)
