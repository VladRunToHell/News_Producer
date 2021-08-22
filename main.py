import PySimpleGUI as sg
import pandas as pd
import keras as keras
import tensorflow as tf
import pickle
import numpy as np
from keras.models import Sequential
from keras.layers import LSTM,Dense,Dropout,Embedding,CuDNNLSTM,Bidirectional
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.layers import concatenate, SpatialDropout1D
from keras.layers.core import Activation
from keras.layers.wrappers import TimeDistributed
from keras.layers.recurrent import LSTM
from keras.layers.embeddings import Embedding
from keras.regularizers import l2
from tqdm import tqdm
import tqdm
from keras.layers import Attention
from tensorflow.keras.layers import Input
from keras.layers import Lambda
from keras import backend as K
from tensorflow.keras.models import Model
from tensorflow.keras.callbacks import EarlyStopping
import json
import sys
import os
import random

x = 575 # Координаты расположения начального окна
y = 200
var1 = 0
var2 = 1
var3 = 2
var4 = 3
var5 = 4

model = keras.models.load_model('model')
encoder_model = keras.models.load_model('encoder_model')
decoder_model = keras.models.load_model('decoder_model')
with open('x_tokenizer.pickle', 'rb') as handle:
    x_tokenizer = pickle.load(handle)
with open('y_tokenizer.pickle', 'rb') as handle:
    y_tokenizer = pickle.load(handle)

reverse_target_word_index = y_tokenizer.index_word
reverse_source_word_index = x_tokenizer.index_word
target_word_index = y_tokenizer.word_index

def seq(headlines):
    itog = x_tokenizer.texts_to_sequences(headlines)
    return itog


def decode_sequence(input_seq):
    (e_out, e_h, e_c) = encoder_model.predict(input_seq)
    target_seq = np.zeros((1, 1))

    target_seq[0, 0] = target_word_index['begin']

    stop_condition = False
    decoded_sentence = ''

    while not stop_condition:
        (output_tokens, h, c) = decoder_model.predict([target_seq]
                                                      + [e_out, e_h, e_c])

        sampled_token_index = np.argmax(output_tokens[0, -1, :])
        sampled_token = reverse_target_word_index[sampled_token_index]

        if sampled_token != 'end':
            decoded_sentence += ' ' + sampled_token

        if sampled_token == 'end' or len(decoded_sentence.split()) \
                >= 12 - 1:
            stop_condition = True

        target_seq = np.zeros((1, 1))
        target_seq[0, 0] = sampled_token_index

        (e_h, e_c) = (h, c)

    return decoded_sentence



sg.theme('LightBlue6')
name = ""
layout = [  [sg.Button('Сгенерировать',
                       size=(100, 2), font=('Roboto', 13, 'bold'), pad=((0,0), (7, 3)))],

            [sg.Button('Следуюшие новости',
                       size=(100, 1), font=('Roboto', 11, 'bold'), pad=((0, 0), (3, 3)))],

            # Название сюжета
            [sg.Text('Название сюжета', key='-MAINTITLE-', auto_size_text=True,
                     size=(100,1), text_color='White', font=('Roboto', 16, 'bold'), pad=((0, 0),(10, 10)),
                     relief=sg.RELIEF_RIDGE, background_color='slategray', expand_x= True, justification='centre', visible=False)],

            # Заголовок 1
            [sg.Text(name, key='-TITLE1-', visible=False, enable_events=True, auto_size_text=True,
                     size=(55, 2), background_color='lightcyan', font=('Roboto', 11, 'italic'),
                     pad=((0, 0),(10, 6)), relief=sg.RELIEF_GROOVE, expand_x= True)],

            # Заголовок 2
            [sg.Text(name, key='-TITLE2-', visible=False, enable_events=True, auto_size_text=True,
                     size=(55, 2), background_color='lightcyan', font=('Roboto', 11, 'italic'),
                     pad=((0, 0),(6, 6)), relief=sg.RELIEF_GROOVE, expand_x= True)],

            # Заголовок 3
            [sg.Text(name, key='-TITLE3-', visible=False, enable_events=True, auto_size_text=True,
                     size=(55, 2), background_color='lightcyan', font=('Roboto', 11, 'italic'),
                     pad=((0, 0),(6, 6)), relief=sg.RELIEF_GROOVE, expand_x= True)],

            # Заголовок 4
            [sg.Text(name, key='-TITLE4-', visible=False, enable_events=True, auto_size_text=True,
                     size=(55, 2), background_color='lightcyan', font=('Roboto', 11, 'italic'),
                     pad=((0, 0),(6, 6)), relief=sg.RELIEF_GROOVE, expand_x= True)],

            # Заголовок 5
            [sg.Text(name, key='-TITLE5-', visible=False, enable_events=True, auto_size_text=True,
                     size=(55, 2), background_color='lightcyan', font=('Roboto', 11, 'italic'),
                     pad=((0, 0),(6, 6)), relief=sg.RELIEF_GROOVE, expand_x= True)]]

window = sg.Window('Desgator', layout, size=(500, 450), location=(x, y), background_color='azure',
                   element_justification='centre')

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancel':
        break

    # Если нажимаем кнопку, то можем выбрать путь, потом меняется текст у кнопки title1 на name, также в переменную
    # newsForTitleOne суется датасет
    if event == 'Сгенерировать':
        path = sg.popup_get_file('Введите путь', location=(x+520, y), font=('Roboto', 11, 'roman'),
                                 background_color='azure')

        data = pd.read_json(path)
        headlines = []
        for i in range(len(data['news'])):
            headlines.append(data['news'][i]['headline'])
        itog = seq(headlines)
        fin = []
        for i in range(len(itog)):
            for j in range(len(itog[i])):
                fin.append(itog[i][j])
        fin = np.asarray(fin)
        itog = pad_sequences(itog, maxlen=20, padding='post')
        itog = decode_sequence(itog.reshape(1, 100))
        window.Element('-MAINTITLE-').Update((itog), visible=True)
        newsForTitleOne = data['news'][var1]['body']
        name = data['news'][var1]['headline']
        window.Element('-TITLE1-').Update(name, visible=True)


        newsForTitleTwo = data['news'][var2]['body']
        name = data['news'][var2]['headline']
        window.Element('-TITLE2-').Update(name, visible=True)


        newsForTitleThree = data['news'][var3]['body']
        name = data['news'][var3]['headline']
        window.Element('-TITLE3-').Update(name, visible=True)


        newsForTitleFour = data['news'][var4]['body']
        name = data['news'][var4]['headline']
        window.Element('-TITLE4-').Update(name, visible=True)


        newsForTitleFive = data['news'][var5]['body']
        name = data['news'][var5]['headline']
        window.Element('-TITLE5-').Update(name, visible=True)

    if event == 'Следующие новости':
        var1 += 5
        var2 += 5
        var3 += 5
        var4 += 5
        var5 += 5


        newsForTitleOne = data['news'][var1]['body']
        name = data['news'][var1]['headline']
        window.Element('-TITLE1-').Update(name, visible=True)


        newsForTitleTwo = data['news'][var2]['body']
        name = data['news'][var2]['headline']
        window.Element('-TITLE2-').Update(name, visible=True)


        newsForTitleThree = data['news'][var3]['body']
        name = data['news'][var3]['headline']
        window.Element('-TITLE3-').Update(name, visible=True)


        newsForTitleFour = data['news'][var4]['body']
        name = data['news'][var4]['headline']
        window.Element('-TITLE4-').Update(name, visible=True)


        newsForTitleFive = data['news'][var5]['body']
        name = data['news'][var5]['headline']
        window.Element('-TITLE5-').Update(name, visible=True)

    if event == '-TITLE1-':
        sg.popup_scrolled(newsForTitleOne, title=data['news'][var1]['headline'],
                          size=(55, 30), location=(x-510, y-100), font=('Roboto', 11, 'roman'))

    if event == '-TITLE2-':
        sg.popup_scrolled(newsForTitleTwo, data['news'][var2]['headline'],
                          size=(55, 30), location=(x-510, y-100), font=('Roboto', 11, 'roman'))

    if event == '-TITLE3-':
        sg.popup_scrolled(newsForTitleThree, data['news'][var3]['headline'],
                          size=(55, 30), location=(x-510, y-100), font=('Roboto', 11, 'roman'))

    if event == '-TITLE4-':
        sg.popup_scrolled(newsForTitleFour, data['news'][var4]['headline'],
                          size=(55, 30), location=(x-510, y-100), font=('Roboto', 11, 'roman'))

    if event == '-TITLE5-':
        sg.popup_scrolled(newsForTitleFive, data['news'][var5]['headline'],
                          size=(55, 30), location=(x-510, y-100), font=('Roboto', 11, 'roman'))

window.close()