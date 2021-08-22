import PySimpleGUI as sg
import pandas as pd
import keras as keras
import pickle
import numpy as np
from keras.preprocessing.sequence import pad_sequences

# Координаты расположения начального окна
x = 575
y = 200

# Индексы хедлайнов
var1 = 0
var2 = 1
var3 = 2
var4 = 3
var5 = 4
spisok = ''

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

# Токенизирует подающийся текст
def seq(headlines):
    itog = x_tokenizer.texts_to_sequences(headlines)

    sum=len(itog)*len(itog[0])

    while sum>=80:
      neg=len(itog)*len(itog[len(itog)-1])
      itog.pop(len(itog)-1)
      sum=sum-neg
    return itog

#
def decode_sequence(input_seq):
    (e_out, e_h, e_c) = encoder_model.predict(input_seq)
    target_seq = np.zeros((1, 1))

    target_seq[0, 0] = target_word_index['begin']

    stop_condition = False
    decoded_sentence = ''

    while not stop_condition:
        (output_tokens, h, c) = decoder_model.predict([target_seq] + [e_out, e_h, e_c])

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

            [sg.Button('Следующие новости', visible= False, key= '-NEXT-',
                       size=(100, 1), font=('Roboto', 11, 'bold'), pad=((0, 0), (3, 3)))],

            # Название сюжета
            [sg.Text('Название сюжета', key='-MAINTITLE-',visible=False, auto_size_text=True,
                     size=(100,1), text_color='White', font=('Roboto', 16, 'bold'), pad=((0, 0),(10, 10)),
                     relief=sg.RELIEF_RIDGE, background_color='slategray', expand_x= True, justification='centre')],

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
                     pad=((0, 0),(6, 6)), relief=sg.RELIEF_GROOVE, expand_x= True)],

            # Кнопка, вызывающая список генерируемых названий сюжетов
            [sg.Button('Список названий', key='-SPISOK-', visible= False,
                        size=(100, 1), font=('Roboto', 11, 'bold'), pad=((0, 0), (3, 3)))]]

window = sg.Window('Desgator', layout, size=(510, 450), location=(x, y), background_color='azure',
                   element_justification='centre')

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancel':
        break

    # Кнопка "Сгенерировать". Вызвает попап гетфайл для получения пути к файлу. Засовывает хедлайны из новостей в
    # кликабельные лейблы. Запускает окно со всеми генируемыми названиями сюжетов
    # P.S. Да, много чего можно было сделать через цикл, но нам не хотелось думать
    if event == 'Сгенерировать':
        path = sg.popup_get_file('Введите путь', no_window=True)
        if not path:
            sg.popup_error(('Ошибка'))
            exit()
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
        spisok += itog + '\n'
        window.Element('-MAINTITLE-').Update((itog), visible=True)

        # Ниже будут блоки когда, которые подгружают заголовки новостей в лейблы и делают их видимыми
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

        window.Element('-SPISOK-').Update(visible=True)
        window.Element('-NEXT-').Update(visible=True)

    # Кнопка "Следующие новости". Обновляет индексы новостей и показывает следующие 5 из сюжета.
    # P.S Всё ещё не хотелось думать
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

    # Обработка нажатия на лейбл
    if event == '-TITLE1-':
        sg.popup_scrolled(newsForTitleOne, title=data['news'][var1]['headline'],
                          size=(47, 30), location=(x - 460, y), font=('Roboto', 11, 'roman'), modal=False)

    if event == '-TITLE2-':
        sg.popup_scrolled(newsForTitleTwo, data['news'][var2]['headline'],
                          size=(55, 30), location=(x - 460, y - 50), font=('Roboto', 11, 'roman'), modal=False)

    if event == '-TITLE3-':
        sg.popup_scrolled(newsForTitleThree, data['news'][var3]['headline'],
                          size=(55, 30), location=(x - 460, y - 50), font=('Roboto', 11, 'roman'))

    if event == '-TITLE4-':
        sg.popup_scrolled(newsForTitleFour, data['news'][var4]['headline'],
                          size=(55, 30), location=(x - 460, y - 50), font=('Roboto', 11, 'roman'))

    if event == '-TITLE5-':
        sg.popup_scrolled(newsForTitleFive, data['news'][var5]['headline'],
                          size=(55, 30), location=(x - 460, y - 50), font=('Roboto', 11, 'roman'))

    if event == '-SPISOK-':
        sg.popup_scrolled(spisok, size=(47, 30), location=(x + 520, y - 50), font=('Roboto', 11, 'roman'),
                          no_titlebar=True, no_sizegrip=True)

window.close()