import pyodbc
import pandas as pd
import mysql.connector
import sqlite3


db = mysql.connector.connect(host='localhost',
                             user='wojtek',
                             passwd='123456',
                             database='laliga')

cursor = db.cursor()
""""for league in leagues:
    query = f'create database {league}; create table teams(id int auto_increment primary key, team_name varchar(50) not null)'
    cursor.execute(query, (nazmulti=True)
    db.commit()
    for team in findTeams(league)[0]:
        query = 'insert into teams(team_name) values(%s)'
        cursor.execute(query, multi=True)
        db.commit()"""

db.commit()
nazwa = 'Huawei'
data_powstania = '1985-12-10'
kraj = 'Chiny'

# cursor.execute('insert into producenci(nazwa,data_powstania,kraj) values(%s,%s,%s)', (nazwa, data_powstania, kraj))
# cursor.execute('DELETE FROM producenci WHERE id_producenta = 7;')
# cursor.execute('ALTER TABLE producenci AUTO_INCREMENT = 1')

# data = pd.read_sql_query(query, db)
# print(data)

db.close()
