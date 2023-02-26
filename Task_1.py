import os.path as op
import pandas as pd
import numpy as np

def continuation(): # Выбор продолжить - завершить
    return input('Для продолжения операций введите 1,\n'
                 'для завершения - любой другой символ:\n')

def generate_num_list(numbered_list): # Генерация списка номеров позиций меню
    list_of_numbers = []
    i = 0
    while i < len(numbered_list):
        num = ''
        while '0' <= numbered_list[i] <= '9':
            num += numbered_list[i]
            i += 1
            if i >= len(numbered_list):
                break
        if num != '':
            list_of_numbers.append(num)
        i += 1
    return list_of_numbers

def num_validation_check(entered_num, num_menu): # Проверка корректности номера введённой операции из меню
    if entered_num not in num_menu:
        print(f'Вы ввели отсутствующий в меню номер операции {entered_num}.\n')
        return False
    return True

def menu(menu_display): # Выбор номера операции из меню
    correct_num = False
    cont = True
    while not correct_num:
        entered_num = input('Выберите номер операции из меню:\n'
                            f'{menu_display}\n')
        correct_num = num_validation_check(entered_num, num_menu)
        if correct_num == False:
            if continuation() != '1':
                correct_num = True
                cont = False
    if cont == True:
        return entered_num

def choice_option(user_frame):
    act = input('Если Вы знаете индекс контакта, введите "0".\n'
                'Для просмотра всей телефонной книги введите "1".\n'
                'Для поиска контактов введите "2":\n')
    match act:
        case '0':
            pass
        case '1':
            print(f'\n    Телефонная книга:\n{user_frame}\n')
        case '2':
            data_search(user_frame)

def data_search(user_frame): # Поиск контактов
    ind = int(input('Выберите поле для поиска контактов.\n'
          'Для поиска по фамилии введите "0"б,\nдля поиска по имени = "1":\n'))
    simb = input('Введите несколько букв с соблюдением регистра:\n')
    print(user_frame[user_frame[data_title[ind]].str.contains(simb)])

def adding_data(user_frame, message): # Добавление контакта в рабочий фрейм
    user_text = input(f'Введите {message} в формате "Фамилия; Имя; Отчество; Номер телефона;":\n')
    user_frame.loc[len(user_frame.index)] = user_text.replace('; ', ';').split(';')
    return user_frame

def data_deletion(user_frame): # Удаление контакта
    choice_option(user_frame)
    del_line = int(input('Введите индекс удаляемой записи (строки):\n'))
    user_frame = user_frame.drop (index = del_line )
    return user_frame

def data_editing(user_frame, message): # Редактирование контакта
    choice_option(user_frame)
    del_line = int(input('Введите индекс редактируемой записи (строки):\n'))
    adding_data(user_frame, message)
    user_frame = user_frame.drop (index = del_line )
    return user_frame 

def data_recording(user_file, user_frame): # Перезапись изменённой базы в файл
    with open(user_file, 'w', encoding='utf-8') as file:
        file.write(''.join([';'.join(elem) + ';\n' for elem in user_frame.values.tolist()]))

def reading_data_frame(user_file): # Формирование списка списков из файла базы данных
    with open(user_file, 'r', encoding='utf-8') as file:         
        data = file.readlines()
    data_list = [elem.replace(';\n', '').split(';') for elem in data]
    data_frame = pd.DataFrame(data_list, columns = data_title)
    return data_frame

def controller_actions():
    work_frame = reading_data_frame(data_file)
    next_act = '1'
    while next_act == '1':
        num_menu = menu(menu_display)
        match num_menu:
            case '1': # Просмотр всех записей
                print(f'\n    Телефонная книга:\n{work_frame}\n')
            case '2': # Поиск контактов
                data_search(work_frame)
            case '3': # Добавление контакта
                message = 'новый контакт'
                work_frame = adding_data(work_frame, message)
                data_recording(data_file, work_frame)
                work_frame = reading_data_frame(data_file)
            case '4': # Удаление контакта
                work_frame = data_deletion(work_frame)
                data_recording(data_file, work_frame)
                work_frame = reading_data_frame(data_file)
            case '5': # Редактирование контакта
                message = 'новую редакцию контакта'
                work_frame = data_editing(work_frame, message)
                data_recording(data_file, work_frame)
                work_frame = reading_data_frame(data_file)
        next_act = continuation()

if __name__ == '__main__': 
    data_file = 'data_file.txt' # файл базы данных
    if not op.isfile(data_file):
        data_recording(data_file, '')
    data_title = ['Фамилия', 'Имя', 'Отчество', 'Номер телефона']
    menu_display = ('Меню операций:\n'
                    '    1. Просмотр всех записей;\n'
                    '    2. Поиск контактов;\n'
                    '    3. Добавление контакта;\n'
                    '    4. Удаление контакта;\n'
                    '    5. Редактирование контакта.')
    num_menu = generate_num_list(menu_display)
    controller_actions()

