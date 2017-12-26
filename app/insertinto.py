import sys
import sqlite3
import json

def insertintotable():

        conn = sqlite3.connect('EBL.db')
        curs = conn.cursor()       
        nm = '2036-12-30'
        addr = '230'
        city = '776'
        curs.execute("INSERT INTO banks (date, value, luck) VALUES (?,?,?)",(nm, addr, city) )
       
        conn.commit()
    # This enables column access by name: row['column_name']
        


