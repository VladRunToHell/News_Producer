import PySimpleGUI as sg
import sys
import os
import random

sg.theme('Dark')
layout = [  [sg.Button('Generate'),],
            [sg.Text('main title')],
            [sg.Button('title1'), ],
            [sg.Button('title2')],
            [sg.Button('title3')],
            [sg.Button('title4')]]

window = sg.Window('Desgator', layout, size=(400,400))

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancel':
        break

    if event == 'generate':
        sg.popup_get_file('Enter PATH')

    if event == 'title1':
        sg.popup_scrolled('h')

    if event == 'title2':
        sg.popup_scrolled('h')

    if event == 'title3':
        sg.popup_scrolled('h')

    if event == 'title4':
        sg.popup_scrolled('h')

window.close()
