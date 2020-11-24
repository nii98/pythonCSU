# -*- coding: utf-8 -*-
"""
Created on Tue Nov 24 08:59:20 2020

@author: nii98_5tv8l5u
"""

import adodbapi
import sqlite3 as sql
from sqlite3 import Error
import pandas as pd
import numpy as np
import os 
import sys
import os.path

print ('Ready')

#добавление нового товара
def add_item(new_data, DataFrame ): # обработка исключений
     



    DataFrame.loc[len(DataFrame)] = new_data
     
     
# удаление товара
def delete_item(df,index):
     df = df.drop(index=index)
     df = df.reset_index(drop=True)
     return df      
     
# добавление товаров оптом из файла
    
def add_item_from_file(file, DataFrame): # обработка исключений
    my_sheet = 'Лист1'
    
    df3 = pd.read_excel(file, sheet_name = my_sheet)   
    DataFrame= pd.concat([DataFrame,df3], axis=0)
    #DataFrame.loc[len(DataFrame)] = df3
    #data_base= sql_connection()
    #sql_insert(data_base,df3)
    return DataFrame 

def enter_item(): 
    item = {}
    print('Введите NAME')
    item['name'] = input()
    print('Введите ID товара')
    item['id'] = input()
    print('Введите MANUFACTURER товара')
    item['manufacturer'] = input()
    print('Введите PRICE товара')
    item['price'] = input()
    print('Введите SIZE товара')
    item['size'] = input()

    return item 

def sql_connection():

    try:
        
        data_base = sql.connect('warehause.db')
        print("Connection is established: Database is created ")
                   
        return data_base 
    
    except Error:

        print(Error)    
     
     
def sql_table(data_base): #создает таблицу
    
  try:
        cursorObj = data_base.cursor()
        cursorObj.execute("CREATE TABLE warehause ( name text, id integer, manufacturer text, price integer,size integer )")
        print("Таблица создана" )
        data_base.commit()
  except Error:
        print("Таблица УЖЕ создана " )      
     
     
def sql_insert(data_base, data): #добавить данные

    cursorObj = data_base.cursor()
    cursorObj.execute('INSERT INTO warehause (name,id,manufacturer,price,size ) VALUES( ?, ?, ?, ?, ?)', data)
    data_base.commit()
    print("Данные добавленны")     
     
     
def show_stat(df):
    print("Статистика:")
    df_stat=df.groupby(['name','size','manufacturer','price',])['id'].count()
    
    #print(df.groupby(['name','size','manufacturer','price'])['id'].count())
    print(df_stat)
    
def show_comand():
    
    
     print('Выберите номер нужной команды\n')
     print('1. Добавить новую позицию')
     print('2. Удалить позицию')
     print('3. Отобразить статистику')
     print('4. Добавить позиции из файла')
     print('5. Отобразить товары')
     #print('ERORR')      
     #print('ТАКОЙ КОМАНДЫ НЕ СУЩЕСТВУЕТ.')
          
     

      
#TEST##################3     

#data = ['rebeok', 8901 , 'balu', 2000, 31] 
#index = 0
#file='testdata.xlsx' ## Файл для загрузки данных из файла
#add_item(data,df)
#df=delete_item(df,index)
#df=add_item_from_file(file,df)
#df=df.reset_index()
#show_stat(df)

####################
df = pd.DataFrame(columns=['name','id','manufacturer','price','size']) 
db=sql_connection()


df.to_sql('tab', db, if_exists='replace', index=False) # синхронизцация с базой данных
db.commit()


def main(df,db):
    while 1:
        show_comand()
        cmd = input("Введите команду: ")
        if cmd =="1":
            new_data=enter_item()
            add_item(new_data,df)
            df.to_sql('tab', db, if_exists='replace', index=False) # синхронизцация с базой данных
            db.commit()
        if cmd == "2":
           index = input("Введите Индекс для удаления: ")
           df = delete_item(df,index)
           df.to_sql('tab', db, if_exists='replace', index=False) # синхронизцация с базой данных
           db.commit()
           
        if cmd =="3":
            show_stat(df)
        if cmd =="4":
            file=input("Введите имя файла: ")
            df=add_item_from_file(file,df)
            df.to_sql('tab', db, if_exists='replace', index=False) # синхронизцация с базой данных
            db.commit()
        
        if cmd =="5":
            print(pd.read_sql('select * from tab', db))
        
      

main(df,db)

 