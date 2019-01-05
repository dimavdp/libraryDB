#python3/SQLite3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan  4 23:48:13 2019
@author: dimavdp
"""
#   Импортируем SQLite 3
import sqlite3

class database_func:

    #   Создаем метод-конструктор инициализации
    #   Он не должен позволять создавать объект класса, без обязательных полей.
    #   В нем создается новая БД.

    def __init__ (self, db):

        #   Переменная conn (от connection) - объект соединения

        #   Такие переменные представляют соединение с базой данных,
        #   служат интерфейсом для операций отмены и подтверждения,
        #   предоставляют досту к реализации пакета и создают объекты курсоров.
        self.conn = sqlite3.connect(db)
        
        #   Переменная cur (от cursor) - объект курсора

        #   Такие переменные представляют одну команду SQL,
        #   посылаемую в виде строки, и могут использоваться
        #   для доступа к результатам, возвращаемым командой SQL.
        self.cur = self.conn.cursor()

        #   В классе работы с функциями SQL в базе данных все методы будут использоваться по схеме:
        # 
        #                self.cur.execute("конструкция, основанная на синтаксисе функций SQL, с передаваемыми из Python значениями")
        #
        #   где:
        #   self - аргумент класса, через который можно обращаться к атрибутам класса
        #   сur  - объект курсора
        #   execute - Python аналог EXEC в SQL
                    
        #   С помощью запроса SQL создается новая таблица library
        self.cur.execute("CREATE TABLE IF NOT EXISTS library(id INTEGER PRIMARY KEY, title VARCHAR(50) ,author text, remain INTEGER)")
        self.conn.commit()


    #   Метод, основывающийся на INSERT-запросе в SQL
    def insert (self, title, author, remain):
        
        #   Команда insert в языке SQL добавляет в таблицу единственную запись. 
        #   После вызова метода execute в атрибуте rowcount курсора возвращается количество записей,
        #   созданных или затронутых последней вы- полненной инструкцией. 
        self.cur.execute("INSERT into library VALUES (NULL,?,?,?)",(title, author, remain))
        
        #   чтобы сохранить изменения в базе данных, необходимо всегда вызывать метод commit объекта соединения.
        #   В противном случае, когда соединение будет закрыто, изменения будут потеряны. 
        #   Пока не будет вызван метод commit, ни одна из добавленных записей не будет видна из других соединений с базой данных.
        self.conn.commit()
        

    #   Метод, позволяющий вывести все данные таблицы
    def view (self):

        #   Здесь с помощью объекта курсора выполняется инструкция SQL select, которая отбирает все записи,
        #   и вызывается метод fetchall курсора, что бы извлечь их. Записи возвращаются сценарию в виде последовательности последовательностей.
        #   В данном модуле это список кортежей – внешний список представляет таблицу результатов,
        #   вложенные кортежи представляют записи, а содержимое вложенных кортежей – столбцы данных.
        self.cur.execute("SELECT * FROM library")
        rows = self.cur.fetchall()
        return rows

    #   Метод поиска, основан на SQL-функциях SELECT/WHERE
    def search (self, title = "", author = "", remain = ""):
        self.cur.execute("SELECT * FROM library where title = ? OR author = ? OR remain = ?",(title, author, remain))
        rows = self.cur.fetchall()
        return rows

    #   Метод удаления по ID книги
    def delete(self,id):
        self.cur.execute("DELETE FROM library where id = ?",(id,))
        self.conn.commit()

    #   Метод изменения/обновления данных с помощью функции SQL UPDATE/SET 
    def update(self, id, author, title, remain):
        self.cur.execute("UPDATE library SET title = ?, author = ?, remain = ? WHERE id=?",(title, author, remain, id))
        self.conn.commit()

    def __del__(self):
        self.conn.close()