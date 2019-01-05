#python3/SQLite3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 5 01:29:31 2019
@author: dimavdp
"""
from tkinter import *
from DBbackend import database_func
database = database_func("library.db")

#   Класс создания и описания переменных окна и элементов в нем.
class Window(object):

    def __init__(self, window):

        self.window = window
        self.window.wm_title("libraryDB")

        #   Label - это виджет, предназначенный для отображения какой-либо надписи
        #   без возможности редактирования пользователем.
        #   Имеет те же свойства, что и перечисленные свойства кнопки.
        title_label = Label(window, text = "Title")
        title_label.grid(row=0,column=0)
        author_label = Label(window, text = "Author")
        author_label.grid(row = 0, column = 2)
        remain_label = Label(window, text = "Remain")
        remain_label.grid(row = 1, column = 0)

        #   Entry - это виджет, позволяющий пользователю ввести одну строку текста. 
        self.title_text = StringVar()
        self.title_entry = Entry(window, textvariable = self.title_text)
        self.title_entry.grid(row = 0, column = 1)
        self.author_text = StringVar()
        self.author_entry = Entry(window, textvariable = self.author_text)
        self.author_entry.grid(row = 0, column = 3)
        self.remain_text = StringVar()
        self.remain_entry = Entry(window, textvariable = self.remain_text)
        self.remain_entry.grid(row = 1, column = 1)

        #   Listbox - это виджет, который представляет собой список,
        #   из элементов которого пользователь может выбирать один или несколько пунктов. 
        self.library_listbox = Listbox(window, height = 6, width = 35)
        self.library_listbox.grid(row = 2, column = 0, rowspan = 6, columnspan = 2)
        self.library_listbox.bind('<<ListboxSelect>>', self.get_selected_row)

        #   Scrollbar даёт возможность пользователю "прокрутить" другой виджет (например текстовое поле). 
        scrollbar = Scrollbar(window)
        scrollbar.grid(row = 2, column = 2, rowspan = 6)
        self.library_listbox.configure(yscrollcommand = scrollbar.set)
        scrollbar.configure(command = self.library_listbox.yview)
        
        #   Cоздание кнопок
        #   Кнопка View all
        view_command_button = Button(window, text="View all", width=12,command=self.view_command)
        view_command_button.grid(row = 2, column = 3)
        #   Кнопка Search Entry
        search_command_button = Button(window, text = "Search entry", width = 12, command = self.search_command)
        search_command_button.grid(row = 3, column = 3)
        #   Кнопка Add Entry 
        add_command_button = Button(window, text = "Add entry", width = 12, command = self.add_command)
        add_command_button.grid(row = 4, column = 3)
        #   Кнопка Update selected
        update_command_button = Button(window, text = "Update selected", width = 12, command = self.update_command)
        update_command_button.grid(row = 5, column = 3)
        #   Кнопка Delete selected
        delete_command_button = Button(window, text = "Delete selected", width = 12, command = self.delete_command)
        delete_command_button.grid(row = 6, column = 3)
        #   Кнопка Close
        close_button = Button(window, text = "Close", width = 12, command = window.destroy)
        close_button.grid(row = 7, column = 3)

    #   Метод обработки данных в строках базы данных
    def get_selected_row(self, event):

        #   Данные строк хранятся в списках
        if len(self.library_listbox.curselection()) > 0:
            index = self.library_listbox.curselection()[0]
            self.selected_tuple = self.library_listbox.get(index)
            
            #   Взаимодействие с данными базы данных идет через изменение списков строк
            self.title_entry.delete(0, END)
            self.title_entry.insert(END, self.selected_tuple[1])
            self.author_entry.delete(0, END)
            self.author_entry.insert(END, self.selected_tuple[2])
            self.remain_entry.delete(0, END)
            self.remain_entry.insert(END, self.selected_tuple[3])

    #   Метод просмотра всех данных в базе данных
    def view_command(self):
        self.library_listbox.delete(0, END)
        for row in database.view():
            self.library_listbox.insert(END, row)

    #   Метод поиска необходимой строки
    def search_command(self):
        self.library_listbox.delete(0, END)
        for row in database.search(self.title_text.get(), self.author_text.get(), self.remain_text.get()):
            self.library_listbox.insert(END, row)
    
    #   Метод добавления данных в базу данных
    def add_command(self):
        database.insert(self.title_text.get(), self.author_text.get(), self.remain_text.get())
        self.library_listbox.delete(0,END)
        self.library_listbox.insert(END, (self.title_text.get(), self.author_text.get(), self.remain_text.get()))

    #   Метод удаления данных из базы данных
    def delete_command(self):
        database.delete(self.selected_tuple[0])

    #   Метод обновления строки 
    def update_command(self):
        database.update(self.selected_tuple[0], self.title_text.get(), self.author_text.get(), self.remain_text.get())

App = Tk()
Window(App)
App.mainloop()


