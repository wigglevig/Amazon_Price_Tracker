import mysql.connector as sqltor
from tkinter import messagebox
import pandas as pd
con = sqltor.connect(host="localhost",user="root",password="vignesh")
cur = con.cursor()
cur = con.cursor(buffered=True) 

cur.execute("create database if not exists AZ_PRICE_TRACKER")
cur.execute("use AZ_PRICE_TRACKER")
cur.execute("CREATE TABLE if not exists Az_list(Name VARCHAR(255) PRIMARY KEY, Price VARCHAR(40), Limitprice VARCHAR(40) )")

try:
    #cur.execute('INSERT into Az_list values(%s,%s,%s)' , (prod_name, price , entry3.get()))
    con.commit()
    cur.execute('SELECT * FROM az_list')
    results = cur.fetchall()
    print(results)
    
except:
    messagebox.showerror('error',"Duplicate Entry in database")