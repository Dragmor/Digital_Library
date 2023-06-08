'''This is Graphic User Interface for DigitalLibrary'''
import tkinter
import subprocess
from tkinter import ttk
from tkinter.ttk import Combobox
from tkinter import messagebox

import tkinter as tk # Python 3

import maincode

class GraphicUserInterface():
    """ create graphic window """

    def __init__(self):
        ''' creating main wiindow '''
        self.window = tkinter.Tk()
        self.window.title("Цифровая библиотека ФКУ-ИК 26")
        self.window.wm_iconbitmap("img/icons/icon.ico") #load icon
        self.version = 'версия 0.9.9 от 26.05.2022 by Kenny'


    def create_notebook_widget(self):
        ''' method create notebook widget '''

        self.tab_control = ttk.Notebook(self.window)
        #adding frames to notebook widget
        self.tab_main = ttk.Frame(self.tab_control)
        self.tab_search_books = ttk.Frame(self.tab_control)
        self.tab_search_card = ttk.Frame(self.tab_control)
        self.tab_adding = ttk.Frame(self.tab_control)
        self.tab_settings = ttk.Frame(self.tab_control)

        self.tab_control.add(self.tab_main, text='главная')
        self.tab_control.add(self.tab_search_books, text='поиск книг')
        self.tab_control.add(self.tab_search_card, text='читатели')
        self.tab_control.add(self.tab_adding, text='добавить')
        self.tab_control.add(self.tab_settings, text='настройки')

        self.tab_control.pack(expand=1, fill='both') #draw notebook on screen

    def create_interface_elements(self):
        #=====================ALL_TABS========================================#
        #add text-label 'всего читателей' on all tabs
        self.all_readers = tkinter.Label(self.window, font='bold',
         text='Всего читателей: '+str(library.cursor.execute('''
                                                                SELECT COUNT(*) 
                                                                FROM readers
                                                            ''').fetchone()[0]))
        #add text 'всего книг:'
        self.all_books = tkinter.Label(self.window, font='bold',
         text='Всего книг: '+str(library.cursor.execute('''
                                                            SELECT COUNT(*) 
                                                            FROM books
                                                        ''').fetchone()[0]))

        #=====================MAIN_TAB========================================#

        self.text_book_title = tkinter.Label(self.tab_main, 
            text='Название книги:', font='system')

        self.entry_book_title = Combobox(self.tab_main, width=10) #book title
        self.entry_book_title.bind("<KeyRelease>", 
            ButtonsFunc.refresh_books_list)

        self.books_display = tkinter.Listbox(self.tab_main, height='7', 
            font='courier', relief="solid")

        self.books_display.bind("<Key-Return>", ButtonsFunc.set_book)
        self.books_display.bind("<Double-ButtonPress>", ButtonsFunc.set_book)
        self.text_enter_f_name = tkinter.Label(self.tab_main, 
            text='Фамилия (или id):', font='system')

        self.entry_f_name = Combobox(self.tab_main, width=10) #reader f_name
        self.entry_f_name.bind("<KeyRelease>", ButtonsFunc.refresh_fnames_list)
        self.readers_display = tkinter.Listbox(self.tab_main, height='7', 
            font='courier', relief="solid")

        self.readers_display.bind("<Key-Return>", ButtonsFunc.set_readers)
        self.readers_display.bind("<Double-ButtonPress>", 
            ButtonsFunc.set_readers)

        self.rb_modes = tkinter.IntVar()
        self.rb_modes.set(1)
        self.rb_give_mode = tkinter.Radiobutton(self.tab_main, value=1, 
            var=self.rb_modes, text='выдать книгу ' ,font='courier')

        self.rb_get_mode = tkinter.Radiobutton(self.tab_main, value=0, 
            var=self.rb_modes, text='принять книгу', font='courier')

        self.processing_book = tkinter.Button(self.tab_main, font='bold',
            text='ОК', command=ButtonsFunc.processing_button_get_give, 
            bg='lightblue')

        #=====================TAB_SEARCH_BOOKS================================#

        self.search_books_mode = tkinter.IntVar()
        self.sb_radio_from_name = tkinter.Radiobutton(self.tab_search_books, 
            value=0, var=self.search_books_mode, text='по названию', 
            command=ButtonsFunc.sb_radiobuttons_processing)

        self.sb_radio_from_author = tkinter.Radiobutton(self.tab_search_books, 
            value=1, var=self.search_books_mode, text='по автору', 
            command=ButtonsFunc.sb_radiobuttons_processing)

        self.sb_radio_from_genre = tkinter.Radiobutton(self.tab_search_books, 
            value=2, var=self.search_books_mode, text='по жанру', 
            command=ButtonsFunc.sb_radiobuttons_processing)

        self.sb_radio_from_id = tkinter.Radiobutton(self.tab_search_books, 
            value=3, var=self.search_books_mode, text='по id', 
            command=ButtonsFunc.sb_radiobuttons_processing)

        self.choose_book_params = Combobox(self.tab_search_books) 
        self.choose_book_params.bind("<KeyRelease>", ButtonsFunc.search_books)
        self.choose_book_params.bind("<Key-Return>", ButtonsFunc.search_books) 
        self.btn_search_books = tkinter.Button(self.tab_search_books, 
            font='system', text='НАЙТИ', bg='lightgreen', 
            command=ButtonsFunc.search_books)

        self.output_book_display = tkinter.Listbox(self.tab_search_books, 
            height='40',font='courier', relief="solid")

        self.output_book_display.bind("<Double-ButtonPress>", 
            ButtonsFunc.view_book_history) 

        self.output_book_display.bind("<Key-Return>", 
            ButtonsFunc.view_book_history)

        self.output_book_display.bind("<Key-Delete>", ButtonsFunc.delete_book)

        #=====================TAB_SEARCH_CARDS================================#
        self.search_cards_mode = tkinter.IntVar()
        self.sc_radio_from_last_name = tkinter.Radiobutton(self.tab_search_card, 
            value=0, var=self.search_cards_mode, text='по фамилии', 
            command=ButtonsFunc.sr_radiobuttons_processing)

        self.sc_radio_from_dormitory = tkinter.Radiobutton(self.tab_search_card, 
            value=1, var=self.search_cards_mode, text='по отряду', 
            command=ButtonsFunc.sr_radiobuttons_processing)

        self.sc_radio_from_id = tkinter.Radiobutton(self.tab_search_card, 
            value=2, var=self.search_cards_mode, text='по id', 
            command=ButtonsFunc.sr_radiobuttons_processing)

        self.choose_reader_params = Combobox(self.tab_search_card) #create combobox
        self.choose_reader_params.bind("<KeyRelease>", ButtonsFunc.search_card)
        self.choose_reader_params.bind("<Key-Return>", ButtonsFunc.search_card)
        self.btn_search_card = tkinter.Button(self.tab_search_card, 
            font='system', text='НАЙТИ', bg='lightgreen', 
            command=ButtonsFunc.search_card)

        self.output_card_display = tkinter.Listbox(self.tab_search_card, 
            height='40',font='courier', relief="solid")

        self.output_card_display.bind("<Double-ButtonPress>", 
            ButtonsFunc.view_reader_card) 

        self.output_card_display.bind("<Key-Return>", 
            ButtonsFunc.view_reader_card)

        self.output_card_display.bind("<Key-Delete>", 
            ButtonsFunc.delete_reader)

        #=====================TAB_ADDING======================================#
        self.text_enter_book_name = tkinter.Label(self.tab_adding, 
            text='Название:', font='system')

        self.entry_book_name = tkinter.Entry(self.tab_adding, width=10)
        self.text_enter_book_author = tkinter.Label(self.tab_adding, 
            text='Автор:', font='system')

        self.entry_book_author = tkinter.Entry(self.tab_adding, width=10)
        self.genres_combobox = Combobox(self.tab_adding) #create combobox
        self.text_genre = tkinter.Label(self.tab_adding, text='Жанр:', 
            font='system')

        genres = []
        for genre in library.view_all_genres():
            genres.append(genre[1]) 
        self.genres_combobox['values'] = genres
        try:
            self.genres_combobox.current(0)
        except:
            pass
        self.add_book_button = tkinter.Button(self.tab_adding, font='bold', 
            text='добавить книгу', bg='lightgreen', 
            command=ButtonsFunc.add_book)
                                   #============#
        self.text_enter_reader_lname = tkinter.Label(self.tab_adding, 
            text='Фамилия:', font='system')

        self.entry_reader_lname = tkinter.Entry(self.tab_adding, width=10)
        self.text_enter_reader_fname = tkinter.Label(self.tab_adding, 
            text='Имя:', font='system')

        self.entry_reader_fname = tkinter.Entry(self.tab_adding, width=10)
        self.text_enter_reader_patronymic = tkinter.Label(self.tab_adding, 
            text='Отчество:', font='system')

        self.entry_reader_patronymic = tkinter.Entry(self.tab_adding, width=10)
        self.text_enter_reader_dormitory = tkinter.Label(self.tab_adding, 
            text='Отряд:', font='system')

        self.dormitory_combobox = Combobox(self.tab_adding)
        dormitorys = []
        for dorm in library.view_all_dormitorys():
            dormitorys.append(dorm[1])
        self.dormitory_combobox['values'] = dormitorys
        try:
            self.dormitory_combobox.current(0)
        except:
            pass
        self.add_reader_button = tkinter.Button(self.tab_adding, 
            bg='lightblue', font='bold', text='добавить читателя', 
            command=ButtonsFunc.add_reader)

        #=====================TAB_SETTINGS====================================#
        self.text_enter_for_developer = tkinter.Label(self.tab_settings, 
            text='для разработчика', font='system')

        self.text_enter_py_command = tkinter.Label(self.tab_settings, 
            text='Выполнить код python')

        self.button_exec_py = tkinter.Button(self.tab_settings, 
            text='execute python code', bg='lightblue', 
            command=ButtonsFunc.exec_py_code)

        self.entry_py_command = tkinter.Entry(self.tab_settings, 
            width=10, font='code')

        self.text_enter_sql_command = tkinter.Label(self.tab_settings, 
            text='Выполнить SQL запрос')

        self.button_exec_sql = tkinter.Button(self.tab_settings, 
            text='execute sql code', bg='lightblue', 
            command=ButtonsFunc.exec_sql_code)

        self.entry_sql_command = tkinter.Entry(self.tab_settings, 
            width=10, font='code')
        self.text_ver = tkinter.Label(self.tab_settings, 
            text=self.version)

    
    def interface_elements_placement(self):
        self.all_readers.pack(side='bottom', anchor='s') #text 'всего читателей:'
        self.all_books.pack(side='bottom', anchor='s') #text 'всего книг:'

        #=====================TAB_MAIN========================================#
        self.text_book_title.pack(fill='both', padx='5')
        self.entry_book_title.pack(fill='both', padx='6')
        self.books_display.pack(fill='both', padx='5')
        self.text_enter_f_name.pack(fill='both', padx='5')
        self.entry_f_name.pack(fill='both', padx='6')
        self.readers_display.pack(fill='both', padx='5')
        self.rb_give_mode.pack(side='top', anchor='n')
        self.rb_get_mode.pack(side='top', anchor='n')
        self.processing_book.pack(fill='both', pady='7') #button 'принять книгу'

        #=====================TAB_SEARCH_BOOKS================================#
        self.output_book_display.pack(padx='5', pady='5', fill='both')

        self.sb_radio_from_name.pack(anchor='w', side='left')
        self.sb_radio_from_author.pack(anchor='w', side='left')
        self.sb_radio_from_genre.pack(anchor='w', side='left')
        self.sb_radio_from_id.pack(anchor='w', side='left')

        self.btn_search_books.pack(pady='7', padx='5', side='right')
        self.choose_book_params.pack(pady='7', padx='5', side='right') #

        #=====================TAB_SEARCH_CARDS================================#
        self.output_card_display.pack(padx='5', pady='5', fill='both') #

        self.sc_radio_from_last_name.pack(anchor='w', side='left')
        self.sc_radio_from_dormitory.pack(anchor='w', side='left')
        self.sc_radio_from_id.pack(anchor='w', side='left')

        self.btn_search_card.pack(pady='7', padx='5', side='right') #
        self.choose_reader_params.pack(pady='7', padx='5', side='right') #

        #=====================ADD_BOOKS=======================================#
        self.text_enter_book_name.pack()
        self.entry_book_name.pack(fill='both', padx='5')
        self.text_enter_book_author.pack()
        self.entry_book_author.pack(fill='both', padx='5')
        self.text_genre.pack()
        self.genres_combobox.pack(fill='both', padx='5')
        self.add_book_button.pack(fill='both', pady='10') #button 'добавить книгу'

        #=====================ADD_READER======================================#
        self.text_enter_reader_lname.pack() #'по названию'
        self.entry_reader_lname.pack(fill='both', padx='5')
        self.text_enter_reader_fname.pack()
        self.entry_reader_fname.pack(fill='both', padx='5')
        self.text_enter_reader_patronymic.pack()
        self.entry_reader_patronymic.pack(fill='both', padx='5')
        self.text_enter_reader_dormitory.pack()
        self.dormitory_combobox.pack(fill='both', padx='5')
        self.add_reader_button.pack(fill='both', pady='10') #button 'добавить читателя'

        #=====================TAB_SETTINGS====================================#
        self.text_enter_for_developer.pack()
        self.text_enter_py_command.pack()
        self.entry_py_command.pack(fill='both', padx='5')
        self.button_exec_py.pack(fill='both', pady='7')
        self.text_enter_sql_command.pack()
        self.entry_sql_command.pack(fill='both', padx='5')
        self.button_exec_sql.pack(fill='both', pady='7') #btn "exec"
        self.text_ver.pack(side='bottom', anchor='s')      
        #=====================================================================#

    def first_launch(self):
        #add data in screen 'список книг'
        ButtonsFunc.search_books()

        #add data in screen 'список читателей'
        ButtonsFunc.search_card()

        #book display on tab_main
        ButtonsFunc.refresh_books_list()
        ButtonsFunc.refresh_fnames_list()


class ButtonsFunc():
    '''class realese functions for GUI buttons''' 
    def __init__(self):
        pass

    def delete_book(*args):
        if GUI.search_books_mode.get() >= 0 and GUI.search_books_mode.get() <= 2:
            delete_id = int((GUI.output_book_display.get(GUI.output_book_display.curselection()).split())[-1])
        else:
            delete_id = int((GUI.output_book_display.get(GUI.output_book_display.curselection()).split())[0])

        book_name = library.cursor.execute('''
                                                SELECT name 
                                                FROM books 
                                                WHERE id=%i
                                            ''' %delete_id).fetchone()
        book_name = str(book_name[0])

        if messagebox.askyesno(title='Внимание!', message='Вы действительно хотите удалить книгу: "%s"?' %book_name.upper()) == False:
            return
        else:
            library.delete_book(book_id=delete_id)

        GUI.all_books.configure(text='Всего книг: '+str(library.cursor.execute('''SELECT COUNT(*) FROM books''').fetchone()[0])) #refresh data
        ButtonsFunc.search_books()
        ButtonsFunc.refresh_books_list()


    def delete_reader(*args):

        if GUI.search_cards_mode.get() == 0 or GUI.search_cards_mode.get() == 1:
            delete_id = int((GUI.output_card_display.get(GUI.output_card_display.curselection()).split())[-1])
        else:
            delete_id = int((GUI.output_card_display.get(GUI.output_card_display.curselection()).split())[0])

        output = library.cursor.execute('''
                                            SELECT first_name, last_name, patronymic 
                                            FROM readers 
                                            WHERE id=%i
                                        ''' %delete_id).fetchone()

        output = output[0] +' '+ output[1]+' '+ output[2]


        if messagebox.askyesno(title='Внимание!', message='Вы действительно хотите удалить карточку читателя: "%s"?' %output.upper()) == False:
            return
        else:
            library.delete_reader(reader_id=delete_id)

        GUI.all_readers.configure(text='Всего читателей: '+str(len(library.view_all_readers()))) #refresh data
        ButtonsFunc.refresh_fnames_list()
        ButtonsFunc.search_card()


    def view_book_history(*args):
        file = open('output.txt', 'w') #create output file

        if GUI.search_books_mode.get() >= 0 and GUI.search_books_mode.get() <= 2:
            book_id = int((GUI.output_book_display.get(GUI.output_book_display.curselection()).split())[-1])
        else:
            book_id = int((GUI.output_book_display.get(GUI.output_book_display.curselection()).split())[0])

        file.write('НАЗВАНИЕ КНИГИ: ')
        data = library.cursor.execute('''
                                        SELECT name FROM books 
                                        WHERE id=%i
                                    ''' %book_id).fetchone()
        data = data[0]
        file.write(str(data).capitalize())

        file.write('\nЖАНР: ')
        for data in library.cursor.execute('''
                    SELECT genres.title 
                    FROM books_genres 
                    INNER JOIN genres 
                    ON books_genres.genre_id = genres.id 
                    WHERE book_id=%i
                    ''' %book_id).fetchall():
            file.write(str(data[0]).capitalize()+', ')

        file.write('\nАВТОР: ')
        for data in library.cursor.execute('''
                    SELECT authors.name 
                    FROM books_authors 
                    INNER JOIN authors
                    ON authors.id = books_authors.author_id
                    WHERE book_id=%i
                    ''' %book_id).fetchall():
            file.write(str(data[0]).capitalize()+', ')

        file.write('\n\nИСТОРИЯ КНИГИ:\n')
        for data in library.cursor.execute('''
                    SELECT  books_readers.datetime, 
                            readers.first_name, 
                            readers.last_name, 
                            readers.patronymic, 
                            readers.dormitory, 
                            books_readers.extradition 
                    FROM books_readers 
                    INNER JOIN readers
                    ON readers.id = books_readers.reader_id
                    WHERE book_id=%i''' %book_id).fetchall():
            file.write(str(data[0])+'  ')
            file.write(str(data[1]).capitalize()+' ')
            file.write(str(data[2]).capitalize()+' ')
            file.write(str(data[3]).capitalize()+'  (')
            file.write(str(data[4]).capitalize()+' отряд)  ')
            if int(data[5]) == 0:
                file.write('ВЕРНУЛ\n')
            else:
                file.write('ВЗЯЛ\n')

        file.close()
        subprocess.getoutput('explorer "output.txt"')


    def view_reader_card(*args):
        file = open('output.txt', 'w') #create output file

        if GUI.search_cards_mode.get() == 0 or GUI.search_cards_mode.get() == 1:
            reader_id = int((GUI.output_card_display.get(GUI.output_card_display.curselection()).split())[-1])
        else:
            reader_id = int((GUI.output_card_display.get(GUI.output_card_display.curselection()).split())[0])

        file.write('ФАМИЛИЯ: ')
        data = library.cursor.execute('''
                                        SELECT first_name FROM readers 
                                        WHERE id=%i
                                    ''' %reader_id).fetchone()
        data = data[0]
        file.write(str(data).capitalize())

        file.write('\nИМЯ: ')
        data = library.cursor.execute('''
                                        SELECT last_name FROM readers 
                                        WHERE id=%i
                                    ''' %reader_id).fetchone()
        data = data[0]
        file.write(str(data).capitalize())

        file.write('\nОТЧЕСТВО: ')
        data = library.cursor.execute('''
                                        SELECT patronymic FROM readers 
                                        WHERE id=%i
                                    ''' %reader_id).fetchone()
        data = data[0]
        file.write(str(data).capitalize())

        file.write('\nОТРЯД: ')
        data = library.cursor.execute('''
                                        SELECT dormitory FROM readers 
                                        WHERE id=%i
                                    ''' %reader_id).fetchone()
        data = data[0]
        file.write(str(data).capitalize())

        file.write('\n\nИСТОРИЯ:\n')
        for data in library.cursor.execute('''
                    SELECT  books_readers.datetime, 
                            books.name, 
                            books_readers.extradition 
                    FROM books_readers 
                    INNER JOIN books
                    ON books.id = books_readers.book_id
                    WHERE reader_id=%i''' %reader_id).fetchall():
            file.write(str(data[0])+'  ')
            file.write('"'+str(data[1]).capitalize()+'"  ')
            if int(data[2]) == 0:
                file.write('ВЕРНУЛ\n')
            else:
                file.write('ВЗЯЛ\n')

        file.close()
        subprocess.getoutput('explorer "output.txt"')


    def refresh_books_list(*args):
        '''for auto-update info in books-list'''
        GUI.books_display.delete(0, tkinter.END)
        count = 0
        if len(str(GUI.entry_book_title.get())) >= 2:
            entered = str(GUI.entry_book_title.get())

            for name in library.cursor.execute('''
                SELECT books.name 
                FROM books 
                WHERE name 
                LIKE "%%%s%%" 
                ORDER BY name DESC''' %entered.lower()).fetchall():

                GUI.books_display.insert(0, str(name[0]).capitalize())
                if count % 2 == 0:
                    GUI.books_display.itemconfig(index=0, bg='lightgray')
                count += 1

        else:
            for name in library.cursor.execute('''
                SELECT books.name 
                FROM books 
                ORDER BY name DESC
                ''').fetchall():

                GUI.books_display.insert(0, str(name[0]).capitalize())
                if count % 2 == 0:
                    GUI.books_display.itemconfig(index=0, bg='lightgray')
                count += 1


    def set_book(*args):
        GUI.entry_book_title.set(str(GUI.books_display.get(GUI.books_display.curselection())))



    def refresh_fnames_list(*args):
        '''for auto-update info in fnames-list'''
        GUI.readers_display.delete(0, tkinter.END)
        count = 0

        if len(str(GUI.entry_f_name.get())) >= 2:
            entered = str(GUI.entry_f_name.get())
            for name in library.cursor.execute('''
                SELECT readers.first_name, 
                        readers.last_name, 
                        readers.patronymic, 
                        readers.dormitory, 
                        readers.id  
                FROM readers 
                WHERE first_name 
                LIKE "%%%s%%" 
                ORDER BY first_name DESC''' %entered.lower()).fetchall():

                GUI.readers_display.insert(0, str(name[0]).capitalize()+' '+str(name[1]).capitalize()+' '+str(name[2]).capitalize()+'  '+str(name[3]).capitalize()+'  '+str(name[-1]).capitalize())
                if count % 2 == 0:
                    GUI.readers_display.itemconfig(index=0, bg='lightgray')
                count += 1
        else:
            for name in library.cursor.execute('''
                SELECT readers.first_name, 
                        readers.last_name, 
                        readers.patronymic, 
                        readers.dormitory, 
                        readers.id  
                FROM readers 
                ORDER BY first_name DESC
                ''').fetchall():

                GUI.readers_display.insert(0, str(name[0]).capitalize()+' '+str(name[1]).capitalize()+' '+str(name[2]).capitalize()+'  '+str(name[3]).capitalize()+'  '+str(name[-1]).capitalize())
                if count % 2 == 0:
                    GUI.readers_display.itemconfig(index=0, bg='lightgray')
                count += 1
                

    def set_readers(*args):
        GUI.entry_f_name.set(str(GUI.readers_display.get(GUI.readers_display.curselection())))


    def processing_button_get_give(*args):
        
        if len(library.cursor.execute('''
                                        SELECT books.id FROM books 
                                        WHERE name="%s"
                                    ''' %str(GUI.entry_book_title.get()).lower()).fetchall()) != 1:

            messagebox.showwarning(title='Внимание!', message='Книга с названием "%s" не найдена! Проверьте правильность ввода!' %str(GUI.entry_book_title.get()).upper())
            return
        else:
            book_id = library.cursor.execute('''
                                                SELECT books.id FROM books 
                                                WHERE name="%s"
                                            ''' %str(GUI.entry_book_title.get()).lower()).fetchone()
            book_id = book_id[0] #


        
        reader_id = (GUI.entry_f_name.get()).split()
        reader_id = reader_id[-1] #

        extradition = GUI.rb_modes.get()

        if library.book_get_give(book_id, reader_id, extradition) != 707:
            if extradition == 1:
                messagebox.showinfo(title='Успех!', message='Книга выдана!')
            else:
                messagebox.showinfo(title='Успех!', message='Книга принята!')
        else:
            messagebox.showerror(title='Внимание!', 
                message='Произошла непредвиденная ошибка! Перезапустите приложение!')


    def sb_radiobuttons_processing(*args):
        #sb - search books
        if GUI.search_books_mode.get() == 2:
            values = []
            for val in library.view_all_genres():
                values.append(val[1])

            GUI.choose_book_params['values'] = values
            try:
                GUI.choose_book_params.current(0)
            except:
                pass
        else:
            GUI.choose_book_params['values'] = ('',)
            try:
                GUI.choose_book_params.current(0)
            except:
                pass
        ButtonsFunc.search_books()



    def sr_radiobuttons_processing(*args):    
        #sr - search readers
        if GUI.search_cards_mode.get() == 1:
            values = []
            for val in library.view_all_dormitorys():
                values.append(val[1])

            GUI.choose_reader_params['values'] = values
            try:
                GUI.choose_reader_params.current(0)
            except:
                pass
        else:

            GUI.choose_reader_params['values'] = ('',)
            try:
                GUI.choose_reader_params.current(0)
            except:
                pass
        ButtonsFunc.search_card()


    #tab_adding
    def add_book():
        if GUI.entry_book_name.get() != '' and GUI.entry_book_author.get() != '' and library.check_genre(GUI.genres_combobox.get().lower()) == False:
            if messagebox.askyesno(title='Внимание!', message='Жанр: %s не внесён в список жанров! Внести и продолжить?' %GUI.genres_combobox.get().upper()) == False:
                return
            else:
                library.add_genre(GUI.genres_combobox.get().lower())

        elif GUI.entry_book_name.get() == '' and GUI.entry_book_author.get() == '' and library.check_genre(GUI.genres_combobox.get().lower()) == False:
            if messagebox.askyesno(title='Внимание!', message='Внести: %s в список жанров?' %GUI.genres_combobox.get().upper()) == False:
                return
            else:
                library.add_genre(GUI.genres_combobox.get().lower())
                return
                
        if GUI.entry_book_name.get() != '' and GUI.entry_book_author.get() != '':
            library.add_book(GUI.entry_book_name.get(), GUI.entry_book_author.get(), GUI.genres_combobox.get())
            GUI.all_books.configure(text='Всего книг: '+str(len(library.view_all_books()))) #refresh text 'всего книг:'
        else:
            messagebox.showwarning(title='Внимание!', message='Заполните все необходимые поля!')

        genres = []
        for genre in library.view_all_genres():
            genres.append(genre[1]) 
        GUI.genres_combobox['values'] = genres

        ButtonsFunc.search_books() #refresh books_display
        GUI.all_books.configure(text='Всего книг: '+str(library.cursor.execute('''SELECT COUNT(*) FROM books''').fetchone()[0])) #refresh data
        #book display on tab_main
        ButtonsFunc.refresh_books_list()
        

        
    def add_reader():

        if library.check_dormitory(GUI.dormitory_combobox.get().lower()) == 0 and GUI.entry_reader_fname.get() == '' and GUI.entry_reader_lname.get() == '':
            if messagebox.askyesno(title='Внимание!', message='Указанный отряд: %s не внесён в список отрядов! Внести?' %GUI.dormitory_combobox.get().upper()) == False:
                    return
            else:
                library.add_dormitory(GUI.dormitory_combobox.get())
        elif GUI.entry_reader_fname.get() == '' or GUI.entry_reader_lname.get() == '':
            messagebox.showwarning(title='Внимание!', message='Заполните все необходимые поля!')
            return
        else:
            if GUI.entry_reader_patronymic.get() == '':
                if messagebox.askyesno(title='Внимание!', message='Не указано отчество! Продолжить?') == False:
                    return
                else:
                    if library.check_dormitory(GUI.dormitory_combobox.get().lower()) == 0:
                        if messagebox.askyesno(title='Внимание!', message='Указанный отряд: %s не внесён в список отрядов! Внести и продолжить?' %GUI.dormitory_combobox.get().upper()) == False:
                            return
                        else:
                            library.add_dormitory(GUI.dormitory_combobox.get())
                    if library.add_reader(GUI.entry_reader_fname.get().lower(), GUI.entry_reader_lname.get().lower(), '-', GUI.dormitory_combobox.get()) == 100:
                        messagebox.showwarning(title='Внимание!', message='Читатель с такими данными уже внесён в базу данных!')
                    else:
                        GUI.all_readers.configure(text='Всего читателей: '+str(len(library.view_all_readers()))) #refresh data
                        ButtonsFunc.refresh_fnames_list()
                        ButtonsFunc.search_card()
                    return

            if library.check_dormitory(GUI.dormitory_combobox.get().lower()) == 0:
                if messagebox.askyesno(title='Внимание!', message='Указанный отряд: %s не внесён в список отрядов! Внести и продолжить?' %GUI.dormitory_combobox.get().upper()) == False:
                    return
                else:
                    library.add_dormitory(GUI.dormitory_combobox.get())
                    if library.add_reader(GUI.entry_reader_fname.get().lower(), GUI.entry_reader_lname.get().lower(), GUI.entry_reader_patronymic.get().lower(), GUI.dormitory_combobox.get()) == 100:
                        messagebox.showwarning(title='Внимание!', message='Читатель с такими данными уже внесён в базу данных!')
            else:
                if library.add_reader(GUI.entry_reader_fname.get().lower(), GUI.entry_reader_lname.get().lower(), GUI.entry_reader_patronymic.get().lower(), GUI.dormitory_combobox.get()) == 100:
                    messagebox.showwarning(title='Внимание!', message='Читатель с такими данными уже внесён в базу данных!')
        dormitorys = []
        for dorm in library.view_all_dormitorys():
            dormitorys.append(dorm[1])
        GUI.dormitory_combobox['values'] = dormitorys

        ButtonsFunc.search_card()
        GUI.all_readers.configure(text='Всего читателей: '+str(len(library.view_all_readers()))) #refresh data
        #refresh readers_display on main_tab
        ButtonsFunc.refresh_fnames_list()

    def exec_py_code(*args):
        try:
            exec(GUI.entry_py_command.get())
            GUI.button_exec_py.configure(text='Код python успешно выполнен')
        except:
            GUI.button_exec_py.configure(text='Ошибка при выполнении python-кода!')


    def exec_sql_code(*args):
        try:
            library.cursor.execute(GUI.entry_sql_command.get())
            for out_text in library.cursor.fetchall():
                print(out_text)
            GUI.button_exec_sql.configure(text='SQL запрос выполнен!')
        except:
            GUI.button_exec_sql.configure(text='Ошибка при выполнении SQL запроса!')

    def search_books(*args):

        GUI.output_book_display.delete(0, tkinter.END)
        count = 0
        if GUI.choose_book_params.get() == '' and GUI.search_books_mode.get() == 0: #search from name

            library.cursor.execute('''
                    SELECT books.name, authors.name, genres.title, books.id 
                    FROM books_authors, books_genres 
                    INNER JOIN books, authors
                    ON books.id = books_authors.book_id
                    AND authors.id = books_authors.author_id
                    INNER JOIN genres 
                    ON books_authors.book_id = books_genres.book_id
                    AND books_genres.genre_id = genres.id 
                    ORDER BY books.name DESC
                    ''')
                    

        elif GUI.choose_book_params.get() != '' and GUI.search_books_mode.get() == 0: #search from name
            library.cursor.execute('''
                    SELECT books.name, authors.name, genres.title, books.id 
                    FROM books_authors, books_genres 
                    INNER JOIN books, authors
                    ON books.id = books_authors.book_id
                    AND authors.id = books_authors.author_id
                    INNER JOIN genres 
                    ON books_authors.book_id = books_genres.book_id
                    AND books_genres.genre_id = genres.id 
                    WHERE books.name LIKE "%%%s%%"
                    ''' %str(GUI.choose_book_params.get().lower()))


        elif GUI.choose_book_params.get() == '' and GUI.search_books_mode.get() == 1: #search from author
            library.cursor.execute('''
                    SELECT authors.name, books.name, genres.title, books.id 
                    FROM books_authors, books_genres 
                    INNER JOIN books, authors
                    ON books.id = books_authors.book_id
                    AND authors.id = books_authors.author_id
                    INNER JOIN genres 
                    ON books_authors.book_id = books_genres.book_id
                    AND books_genres.genre_id = genres.id 
                    ORDER BY authors.name DESC
                    ''')

        elif GUI.choose_book_params.get() != '' and GUI.search_books_mode.get() == 1: #search from author
            library.cursor.execute('''
                    SELECT authors.name, books.name, genres.title, books.id 
                    FROM books_authors, books_genres 
                    INNER JOIN books, authors
                    ON books.id = books_authors.book_id
                    AND authors.id = books_authors.author_id
                    INNER JOIN genres 
                    ON books_authors.book_id = books_genres.book_id
                    AND books_genres.genre_id = genres.id 
                    WHERE authors.name LIKE "%%%s%%"
                    ''' %str(GUI.choose_book_params.get().lower()))


        elif GUI.choose_book_params.get() == '' and GUI.search_books_mode.get() == 2: #search from genre
            library.cursor.execute('''
                    SELECT genres.title, books.name, authors.name, books.id 
                    FROM books_authors, books_genres 
                    INNER JOIN books, authors
                    ON books.id = books_authors.book_id
                    AND authors.id = books_authors.author_id
                    INNER JOIN genres 
                    ON books_authors.book_id = books_genres.book_id
                    AND books_genres.genre_id = genres.id 
                    ORDER BY genres.title DESC
                    ''')

        elif GUI.choose_book_params.get() != '' and GUI.search_books_mode.get() == 2: #search from genre
            library.cursor.execute('''
                    SELECT genres.title, books.name, authors.name, books.id 
                    FROM books_authors, books_genres 
                    INNER JOIN books, authors
                    ON books.id = books_authors.book_id
                    AND authors.id = books_authors.author_id
                    INNER JOIN genres 
                    ON books_authors.book_id = books_genres.book_id
                    AND books_genres.genre_id = genres.id 
                    WHERE genres.title LIKE "%%%s%%"
                    ''' %str(GUI.choose_book_params.get().lower()))

        elif GUI.choose_book_params.get() == '' and GUI.search_books_mode.get() == 3: #search from id
            library.cursor.execute('''
                    SELECT books.id, books.name, authors.name, genres.title 
                    FROM books_authors, books_genres 
                    INNER JOIN books, authors
                    ON books.id = books_authors.book_id
                    AND authors.id = books_authors.author_id
                    INNER JOIN genres 
                    ON books_authors.book_id = books_genres.book_id
                    AND books_genres.genre_id = genres.id 
                    ORDER BY books.id DESC
                    ''')   

        elif GUI.choose_book_params.get() != '' and GUI.search_books_mode.get() == 3: #search from id
            library.cursor.execute('''
                    SELECT books.id, books.name, authors.name, genres.title 
                    FROM books_authors, books_genres 
                    INNER JOIN books, authors
                    ON books.id = books_authors.book_id
                    AND authors.id = books_authors.author_id
                    INNER JOIN genres 
                    ON books_authors.book_id = books_genres.book_id
                    AND books_genres.genre_id = genres.id 
                    WHERE books.id="%s"
                    ''' %GUI.choose_book_params.get())   

        
        for book in library.cursor.fetchall():
            out_data = ''
            if GUI.search_books_mode.get() != 3:
                if len(str(book[0])) > 25:
                    out_data += str(book[0])[0:25]
                else:
                    out_data += str(book[0])+' '*(25-len(str(book[0])))
            else:
                if len(str(book[0])) > 5:
                    out_data += str(book[0])[0:5]
                else:
                    out_data += str(book[0])+' '*(5-len(str(book[0])))
            out_data += ' | '
            
            if len(str(book[1])) > 25:
                out_data += str(book[1][0:25]).capitalize()
            else:
                out_data += str(book[1]).capitalize()+' '*(25-len(str(book[1])))
            out_data += ' | '
            if len(str(book[2])) > 25:
                out_data += str(book[2][0:25]).capitalize()
            else:
                out_data += str(book[2]).capitalize()+' '*(25-len(str(book[2])))
            out_data += ' | '
            if len(str(book[3])) > 25:
                out_data += str(book[3][0:25]).capitalize()
            else:
                out_data += str(book[3]).capitalize()+' '*(25-len(str(book[3])))
            GUI.output_book_display.insert(0, out_data+'  ')
            if count % 2 == 0:
                GUI.output_book_display.itemconfig(index=0, bg='lightgray')
            count += 1


    def search_card(*args):
        GUI.output_card_display.delete(0, tkinter.END)
        count = 0

        if GUI.choose_reader_params.get() == '' and GUI.search_cards_mode.get() == 0: #search from name
            library.cursor.execute('''
                                        SELECT readers.first_name, 
                                                readers.last_name, 
                                                readers.patronymic, 
                                                readers.dormitory, 
                                                readers.id 
                                        FROM readers 
                                        ORDER BY first_name DESC
                                        ''')


        elif GUI.choose_reader_params.get() != '' and GUI.search_cards_mode.get() == 0: #search from name
            library.cursor.execute('''
                                        SELECT readers.first_name, 
                                                readers.last_name, 
                                                readers.patronymic, 
                                                readers.dormitory, 
                                                readers.id 
                                        FROM readers 
                                        WHERE readers.first_name 
                                        LIKE "%%%s%%"
                                    ''' %str(GUI.choose_reader_params.get().lower()))


        elif GUI.choose_reader_params.get() == '' and GUI.search_cards_mode.get() == 1: #search from dormitory
            library.cursor.execute('''
                                    SELECT readers.dormitory, 
                                            readers.first_name, 
                                            readers.last_name, 
                                            readers.patronymic, 
                                            readers.id 
                                    FROM readers 
                                    ORDER BY dormitory
                                    ''')


        elif GUI.choose_reader_params.get() != '' and GUI.search_cards_mode.get() == 1: #search from dormitory
            library.cursor.execute('''
                                    SELECT readers.dormitory, 
                                            readers.first_name, 
                                            readers.last_name, 
                                            readers.patronymic, 
                                            readers.id 
                                    FROM readers 
                                    WHERE readers.dormitory="%s" 
                                    ORDER BY dormitory
                                ''' %str(GUI.choose_reader_params.get().lower()))

        elif GUI.choose_reader_params.get() == '' and GUI.search_cards_mode.get() == 2: #search from id
            library.cursor.execute('''
                                    SELECT readers.id, 
                                            readers.first_name, 
                                            readers.last_name, 
                                            readers.patronymic, 
                                            readers.dormitory 
                                    FROM readers 
                                    ORDER BY id DESC''')

        elif GUI.choose_reader_params.get() != '' and GUI.search_cards_mode.get() == 2: #search from id
            library.cursor.execute('''
                                    SELECT readers.id, 
                                            readers.first_name, 
                                            readers.last_name, 
                                            readers.patronymic, 
                                            readers.dormitory 
                                    FROM readers 
                                    WHERE readers.id="%s" 
                                    ''' %GUI.choose_reader_params.get())

        for user in library.cursor.fetchall():
            out_data = ''
            if GUI.search_cards_mode.get() != 0:
                if len(str(user[0])) > 5:
                    out_data += str(user[0][0:5]).capitalize()
                else:
                    out_data += str(user[0]).capitalize()+' '*(5-len(str(user[0])))
            else:
                if len(str(user[0])) > 20:
                    out_data += str(user[0][0:20]).capitalize()
                else:
                    out_data += str(user[0]).capitalize()+' '*(20-len(str(user[0])))
            out_data += ' | '
            if len(str(user[1])) > 20:
                out_data += str(user[1][0:20]).capitalize()
            else:
                out_data += str(user[1]).capitalize()+' '*(20-len(str(user[1])))
            out_data += ' | '
    
            if len(str(user[2])) > 20:
                out_data += str(user[2][0:20]).capitalize()
            else:
                out_data += str(user[2]).capitalize()+' '*(20-len(str(user[2])))
            out_data += ' | '
    
            if len(str(user[3])) > 20:
                out_data += str(user[3][0:20]).capitalize()
            else:
                out_data += str(user[3]).capitalize()+' '*(20-len(str(user[3])))
            out_data += ' | '
    
            if len(str(user[4])) > 20:
                out_data += str(user[4][0:20]).capitalize()
            else:
                out_data += str(user[4]).capitalize()+' '*(20-len(str(user[4])))
    
            GUI.output_card_display.insert(0, out_data+'  ')
    
            if count % 2 == 0:
                GUI.output_card_display.itemconfig(index=0, bg='lightgray')
            count += 1

    

if __name__ == '__main__':
    '''creating DataBase'''
    library = maincode.DB()
    library.connect_to_db()

#create tables
    #main tables
    library.add_table('books', 'id INTEGER PRIMARY KEY, name')
    library.add_table('authors', 'id INTEGER PRIMARY KEY, name')
    library.add_table('genres', 'id INTEGER PRIMARY KEY, title')
    library.add_table('readers', 'id INTEGER PRIMARY KEY, last_name, first_name, patronymic, dormitory')
    library.add_table('dormitorys', 'id INTEGER PRIMARY KEY, name')
    #joins
    library.add_table('books_genres', 'id INTEGER PRIMARY KEY, book_id INTEGER, genre_id INTEGER')
    library.add_table('books_authors', 'id INTEGER PRIMARY KEY, book_id INTEGER, author_id INTEGER')
    library.add_table('books_readers', 'id INTEGER PRIMARY KEY, book_id INTEGER, reader_id INTEGER, datetime, extradition bool') #extradition 1 - книга была выдана, 0 - принята

    '''User Interface'''
    GUI =  GraphicUserInterface()
    GUI.create_notebook_widget()
    GUI.create_interface_elements()
    GUI.interface_elements_placement()
    GUI.first_launch()
    GUI.window.mainloop()

    '''
self.cursor.execute("ALTER TABLE books ADD COLUMN publisher") <= add column in table "books" with name "publisher"

self.cursor.execute('DELETE books WHERE id=1') #delete from table 'books' data with 'id' 1

self.cursor.execute('UPDATE books SET on_hand=True WHERE id=1') #change data in table 'books'


ИДЕИ:
first_name - ФАМИЛИЯ

добавить больше инфы в карточки читателей и в историю книг

ВРУЧНУЮ ДОБАВИТЬ ВО ВСЕ КОЛОНКИ id PRIMARY KEY, что бы РАБОТАЕЛ АВТОИНКРЕМЕНТ!

'''
