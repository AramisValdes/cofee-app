import PySimpleGUI as sg
import database

MAIN_MENU = [
    [
        [
            [sg.Button('Add New Bean', key="-new_bean-"), sg.Button('See all beans', key="-all_beans-"),
             sg.Button('Search', key="-search-"), sg.Button('Best Method', key="-best_method-")],
            [sg.Exit()]
        ]
    ]
]

ADD_NEW_BEAN = [
    [
        [
            [sg.Text('Please fill out the following fields:')],
            [sg.Text('Bean Name', size=(15, 1)), sg.InputText(key='-name-', do_not_clear=False)],
            [sg.Text('Preparation Method', size=(15, 1)), sg.InputText(key='-method-', do_not_clear=False)],
            [sg.Text('Enter your rating score (0-100)', size=(15, 1)), sg.InputText(key='-rating-', do_not_clear=False), ],
            [sg.Submit('Submit'),sg.Exit()]

        ]
    ]
]

sg.theme('DarkAmber')  # Add a touch of color
# All the stuff inside your window.

# Create the Window
Wmenu = sg.Window('Coffee Bean Database', MAIN_MENU)
Wnew_bean = sg.Window('Add New Coffee Been', ADD_NEW_BEAN)

# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = Wmenu.read()
    if event == sg.WIN_CLOSED or event == 'Exit':  # if user closes window or clicks cancel
        break
    if event == '-new_bean-':
        while True:
            event, values = Wnew_bean.read()
            connection = database.connect()
            if event == 'Submit':
                database.add_bean(connection, values['-name-'], values['-method-'], values['-rating-'])
                sg.popup('Data saved!')
            if event == sg.WIN_CLOSED or event == 'Exit':  # if user closes window or clicks cancel
                break
        Wnew_bean.close()

    continue
Wmenu.close()
