import pandas as pd
import os
import re

script_dir = os.path.dirname(__file__)


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
