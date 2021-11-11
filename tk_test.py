# Author: Jaime García Chaparro
# coding=utf-8

from tkinter import *

root = Tk()

canvas = Canvas(root)
canvas.grid(rowspan=24, columnspan=4)

# Header

instructions = Label(root, text = 'test')
instructions.grid(rowspan=2, columnspan=2, row=0, column=0)

# Configuration and start

capture_text = StringVar()
capture_btn = Button(root, textvariable=capture_text)
capture_text.set('Capture')
capture_btn.grid(row= 0, column=3, columnspan=2)

options_text = StringVar()
options_btn = Button(root, textvariable=options_text)
options_text.set('Options')
options_btn.grid(row=1, column=3, columnspan=2)

# OCR-ed words

number_title = Label(root, text= 'No.')
number_title.grid(row=4, column=0)

chinese_title = Label(root, text= 'Chinese')
chinese_title.grid(row=4, column=1)

pinyin_title = Label(root, text= 'Pinyin')
pinyin_title.grid(row=4, column=2)

traslation_title = Label(root, text='Translation')
traslation_title.grid(row=4, column=3)

# OCR dictionary

row = 5
no_i = 1

def add_word(word, pinyin, translation):
    global row
    global no_i

    no_label = Label(root, text=no_i)
    no_label.grid(row = row, column=0)

    word_label = Label(root, text=word)
    word_label.grid(row=row, column=1)

    pinyin_label = Label(root, text=pinyin)
    pinyin_label.grid(row=row, column=2)

    translation_label = Label(root, text=translation)
    translation_label.grid(row=row, column=3)

    row += 1
    no_i += 1

add_word('我們', 'women', 'nosotros')
add_word('我們', 'women', 'nosotros')


root.mainloop()