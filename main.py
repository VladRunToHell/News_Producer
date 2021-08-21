import PySimpleGUI as sg
import pandas as pd
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

# sg.theme_previewer()

sg.theme('LightBlue6')
name = ""
layout = [  [sg.Button('Сгенерировать',
                       size=(100, 2), font=('Roboto', 13, 'bold'), pad=((0,0), (7, 3)))],

            [sg.Button('Следуюшие новости',
                       size=(100, 1), font=('Roboto', 11, 'bold'), pad=((0, 0), (3, 3)))],

            # Название сюжета
            [sg.Text('Название сюжета', key='-MAINTITLE-', auto_size_text=True,
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
        print(data.head(10))
        newsForTitleOne = data['news'][var1]['body']
        name = data['news'][var1]['headline']
        window.Element('-TITLE1-').Update(name, visible=True)

        data = pd.read_json(path)
        newsForTitleTwo = data['news'][var2]['body']
        name = data['news'][var2]['headline']
        window.Element('-TITLE2-').Update(name, visible=True)

        data = pd.read_json(path)
        newsForTitleThree = data['news'][var3]['body']
        name = data['news'][var3]['headline']
        window.Element('-TITLE3-').Update(name, visible=True)

        data = pd.read_json(path)
        newsForTitleFour = data['news'][var4]['body']
        name = data['news'][var4]['headline']
        window.Element('-TITLE4-').Update(name, visible=True)

        data = pd.read_json(path)
        newsForTitleFive = data['news'][var5]['body']
        name = data['news'][var5]['headline']
        window.Element('-TITLE5-').Update(name, visible=True)

    if event == 'Следующие новости':
        var1 += 5
        var2 += 5
        var3 += 5
        var4 += 5
        var5 += 5

        data = pd.read_json(path)
        newsForTitleOne = data['news'][var1]['body']
        name = data['news'][var1]['headline']
        window.Element('-TITLE1-').Update(name, visible=True)

        data = pd.read_json(path)
        newsForTitleTwo = data['news'][var2]['body']
        name = data['news'][var2]['headline']
        window.Element('-TITLE2-').Update(name, visible=True)

        data = pd.read_json(path)
        newsForTitleThree = data['news'][var3]['body']
        name = data['news'][var3]['headline']
        window.Element('-TITLE3-').Update(name, visible=True)

        data = pd.read_json(path)
        newsForTitleFour = data['news'][var4]['body']
        name = data['news'][var4]['headline']
        window.Element('-TITLE4-').Update(name, visible=True)

        data = pd.read_json(path)
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