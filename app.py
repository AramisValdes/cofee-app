import database
import PySimpleGUI as sg


MENU_PROMPT = """-- Coffee Bean App --

Please choose one of these options:

1) Add new bean.
2) See all beans.
3) Find a bean by name.
4) See which preparation method is best for a bean.
5) Exit.

Your selection:"""


sg.theme('DarkAmber')   # Add a touch of color
# All the stuff inside your window.
layout = [  [sg.Text('Please select one of these options:')],
            [sg.Text('Enter something on Row 2'), sg.InputText()],
            [sg.Button('Add New Bean')],
            [sg.Button('Ok'), sg.Button('Cancel')] ]

# Create the Window
window = sg.Window('Coffee Bean Database', layout)
# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
        break
    print('You entered ', values[0])

window.close()



def menu():
    connection = database.connect()
    database.create_tables(connection)

    while (use_input := input(MENU_PROMPT)) != "5":
        if use_input == "1":
            name = input("Enter bean name: ")
            method = input("Enter how you've prepared it: ")
            rating = int(input("Enter your rating score (0-100): "))

            database.add_bean(connection, name, method, rating)
        elif use_input == "2":
            beans = database.get_all_beans(connection)

            for bean in beans:
                print(f"{bean[1]} ({bean[2]}) - {bean[3]}/100")
        elif use_input == "3":
            name = input("Enter bean name to find: ")
            beans = database.get_beans_by_name(connection, name)

            for bean in beans:
                print(f"{bean[1]} ({bean[2]}) - {bean[3]}/100")
        elif use_input == "4":
            name = input("Enter bean name to find preparation method: ")
            best_method = database.get_best_preparation_for_bean(connection, name)

            print(f"The best preparation method for {name} is: {best_method[2]}")
        else:
            print("Invalid input. Please try again!")


menu()
