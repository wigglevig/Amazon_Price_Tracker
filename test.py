import mysql.connector as sqltor
from bs4 import BeautifulSoup
import requests
import csv

def get_link_data(url):
    
    headers = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36",
    "Accept-language":'en',}
    r = requests.get(url, headers=headers)
    soup= BeautifulSoup(r.text , "lxml")
    
    global prod_name , price
    prod_name = soup.select_one('#productTitle').getText().strip()

    avail = soup.select_one('#availability').getText().strip().replace('\n','').split ('.')

    try:
        asin = url.split('/dp/')[1].split('?')[0]
    except:
        asin = url.split('/dp/')[1].split('/')[0]
    #global price
    try:
        price = soup.select_one("#priceblock_ourprice").getText()
    except:
        pass
    
    try:
        price = soup.select_one("#priceblock_dealprice").getText()
    except:
        pass
    try:
        price = soup.find("span", attrs ={'class':"a-size-base a-color-price a-color-price"}).string.strip()
    except:
        pass
    price = float(price[1:].replace(',','').replace('₹',''))


       
    return None

con=sqltor.connect(host='localhost' , user='root', password='vignesh' , database='az_price_tracker')
cur=con.cursor()
cur.execute("select * from az_list")
rows= cur.fetchall()
con.close()
with open('log.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Product_Name", "Current_Price", "Price_Status"])

for i in rows:
    a = i[5]
    print(a)
    if float(a) <= float(i[3]):
        status = "price decreased"
    else:
        status= "price increased"
    with open('abc.csv', 'a') as file:
        witer = csv.writer(file)
        content = [f"{prod_name} , {price} , {status}"]
        file.writerow(content)
    with open('abc.csv', 'r') as file:
        print(file.read())