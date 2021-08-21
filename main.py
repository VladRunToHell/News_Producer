import PySimpleGUI as sg
import pandas as pd
import sys
import os
import random

sg.theme('Dark')
name = ""
layout = [  [sg.Button('Сгенерировать'),],
            [sg.Button(name, key='title1', visible=False)],
            [sg.Button('title2')],
            [sg.Button('title3')],
            [sg.Button('title4')]]

window = sg.Window('Desgator', layout, size=(400,400))

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancel':
        break

    # Если нажимаем кнопку, то можем выбрать путь, потом меняется текст у кнопки title1 на name, также в переменную
    # newsForTitleOne суется датасет
    if event == 'Сгенерировать':
        path = sg.popup_get_file('Введите путь')
        data = pd.read_json(path)
        newsForTitleOne = data
        name = data['title'][0]
        window.Element('title1').Update(name, visible=True)



    if event == 'title1':
        sg.popup_scrolled(newsForTitleOne)

    if event == 'title2':
        sg.popup_scrolled('h')

    if event == 'title3':
        sg.popup_scrolled('h')

    if event == 'title4':
        sg.popup_scrolled('h')

window.close()
