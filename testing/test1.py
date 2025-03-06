from bs4 import BeautifulSoup
import smtplib
import lxml
import requests
import time , datetime
import threading
from tkinter import messagebox , ttk
import tkinter as tk
import sys
import mysql.connector as sqltor



#API FOR GETTING PRICE AND NAME OF THE PRODUCT

def get_link_data(url):
    
    headers = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36",
    "Accept-language":'en',}
    r = requests.get(url, headers=headers)
    soup= BeautifulSoup(r.text , "lxml")
    
    global prod_name
    prod_name = soup.select_one('#productTitle').getText().strip()[0:55]
    avail = soup.select_one('#availability').getText().strip().replace('\n','').split ('.')
   
    Check_avail(avail)
    global price
    try:
        price = soup.select_one("#priceblock_ourprice").getText()
    except:
        price = soup.select_one("#priceblock_dealprice").getText()
    
    price = float(price[1:].replace(',','').replace('₹',''))
    compare_price(price)    

       
    return None

def dbstor():
    
    con = sqltor.connect(host="localhost",user=f"{dbuser}",password=f"{dbpass}")
    cur = con.cursor()
    cur = con.cursor(buffered=True) 
    
    cur.execute("create database if not exists AZ_PRICE_TRACKER")
    cur.execute("use AZ_PRICE_TRACKER")
    cur.execute("CREATE TABLE if not exists Az_list(Name VARCHAR(255) PRIMARY KEY, Price VARCHAR(40),Email VARCHAR(40), Limitprice VARCHAR(40), Date DATETIME)")
    
    
    cur.execute('INSERT into Az_list values(%s,%s,%s,%s,now())' , (prod_name, price ,entry2.get(), entry3.get()))
    con.commit()
    
    
def send_email():
    server = smtplib.SMTP('smtp.gmail.com', 587 )
    server.ehlo()
    server.starttls()
    server.ehlo()
    
    server.login('azpricetrackerbot@gmail.com',"zjewhxbcebsgniny")
    
    subject = "Hey the price fell down!"
    body = f"Check The amazon link {entry1.get()} "

    msg=f"Subject: {subject}\n\n{body}"
    
    server.sendmail(
        "azpricetrackerbot@gmail.com",
        f"{entry2.get()}",
        msg)
    
    
    
    messagebox.showinfo('Info','Hey the price has been decreased check your Email')    
   

 


#FOR TKINTER APP
def run_app():
    t = threading.Thread(target=run)
    t.setDaemon(True)
    t.start()
    
 
def run():
    
    link=entry1.get()
    get_link_data(link)



def Check_avail(avail):
    if ('Currently unavailable' in tuple(avail)):
        messagebox.showinfo('Availability' , 'The Item is Currently unavailable')
        

def compare_price(rate):

    if rate <= float(entry3.get()):
        dbstor() 
        send_email()
       
    else:
        messagebox.showinfo('Info',f'Price Limit Specified is less than the current price\n Current price of the prdouct is {price}')
         
    return None              








def az_tracker():
    global datawin , dbuser , dbpass
    datawin = tk.Toplevel(main)
    datawin.title("Amazon Price Tracker")
    datawin.iconbitmap(r'aztrackericon.ico')
    datawin.geometry(("700x600"))
    #datawin.resizable(False,False)
    s = ttk.Style(datawin)
    s.theme_use("clam")
    
    # frame = tk.Frame(datawin , bg ='#423233' )
    # frame.place( relwidth=1 , relheight=1 )

    tree = ttk.Treeview(datawin, show="headings", height='10')
    
    # CREATING OUR COLUMNS
    tree['columns'] = ("Sno.","NAME", "PRICE", "EMAIL","LIMPRICE","Date")
    tree.column("#0", width=120 , minwidth=25)
    tree.column("Sno.", anchor='center', width = 80 , minwidth=25)
    tree.column("NAME", anchor='center' , width= 120, minwidth=50)
    tree.column("PRICE" ,anchor='center' , width= 120, minwidth=50)
    tree.column("EMAIL", anchor ='center', width= 120 , minwidth=50)
    tree.column("LIMPRICE", anchor='center' , width=120, minwidth=30 )
    tree.column("Date", anchor='center' , width=120, minwidth=30 )
    
    #creating Headings
    #tree.heading('#0', text="label" , anchor ='w')
    tree.heading("Sno." , text="S_No.", anchor='center')
    tree.heading('NAME', text="Name" , anchor ='center')
    tree.heading('PRICE', text="Product Price" , anchor='center')
    tree.heading('EMAIL', text ='Email' , anchor='center')
    tree.heading('LIMPRICE', text="Limit price" , anchor ='center')
    tree.heading("Date", text="Date" , anchor ='center')

    # connecting to database
    
    con = sqltor.connect(host="localhost",user=f'{dbuser}',password=f'{dbpass}')
    cur = con.cursor()
    cur.execute("create database if not exists AZ_PRICE_TRACKER")
    cur.execute("use AZ_PRICE_TRACKER")
    cur.execute("CREATE TABLE if not exists Az_list(Name VARCHAR(255) PRIMARY KEY, Price VARCHAR(40),Email VARCHAR(40), Limitprice VARCHAR(40) , Date DATETIME)")
    cur.execute("use AZ_PRICE_TRACKER")
    cur.execute("SELECT * from Az_list")
    rows = cur.fetchall()
    con.close()
    # ADD DATA
    a=1
    for i in rows:
        tree.insert('',a,values = (a,i[0],i[1],i[2],i[3],i[4]))
        a=a+1    
    tree.pack(side = 'bottom' , anchor='s' )

    def refresh():
        datawin.destroy()
        az_tracker()
        
        

    def clearTextInput():
        entry1.delete("0","end")
        entry2.delete("0","end")
        entry3.delete("0","end")
    
        
    global entry1,entry2,entry3

       

    frame = tk.Frame(datawin , bg ='#747474' )
    frame.place(relx=0.5 ,rely=0, relwidth=1 , relheight=0.55, anchor='n')

    background_img= tk.PhotoImage(file='C:\\Users\\subbi\\OneDrive\\Desktop\\project cs xii\\bgimage1.png')
    background_label=tk.Label(frame, image=background_img,bg='#747470')
    background_label.place(relwidth=1,relheight=0.5,y=-0)

    label1= tk.Label(frame , text="Product-Url:",fg='white', bg='black', font=('Arial',10,'bold'))
    label1.place(relheight=0.1, rely=0.5, relx=0.05,relwidth=0.15 )

    entry1 = tk.Entry(frame, bd=3)
    entry1.place(relx=0.20,relwidth=0.75, relheight=0.1,rely = 0.5)


    label2= tk.Label(frame , text="Email-id:",fg='white', bg='black', font=('Arial',10,'bold'))
    label2.place(relheight=0.1, rely=0.61, relx=0.05,relwidth=0.15 )

    entry2 = tk.Entry(frame, bd=3)
    entry2.place(relx=0.20,relwidth=0.75, relheight=0.1,rely = 0.61)


    label3= tk.Label(frame , text="Limit(in ₹) :",fg='white', bg='black', font=('Arial',10,'bold'))
    label3.place(relheight=0.1, rely=0.72, relx=0.05,relwidth=0.15 )

    entry3 = tk.Entry(frame, bd=3)
    entry3.place(relx=0.2,relwidth=0.75, relheight=0.1,rely = 0.72)



    button1=tk.Button(frame , text='Submit', command=run_app , bg='#ff9a00', font=('Arial',12,'bold'))
    button1.place(anchor='s', relx=0.10, relwidth=0.15, relheight=0.1, rely=0.95)



    button2=tk.Button(frame , text='Clear', bg='#ff9a00', command = clearTextInput ,font=('Arial',12,'bold'))
    button2.place(anchor='s', relx=0.36 , relwidth=0.15, relheight=0.1, rely=0.95)

    button3=tk.Button(frame , text='Refresh', bg='#ff9a00', font=('Arial',12,'bold') , command = lambda: refresh())
    button3.place(anchor='s', relx=0.62 , relwidth=0.15, relheight=0.1, rely=0.95)


    button4=tk.Button(frame , text='Remove' ,bg='#ff9a00', font=('Arial',12,'bold') )
    button4.place(anchor='s', relx=0.89 , relwidth=0.15, relheight=0.1, rely=0.95)

    datawin.mainloop()


def mainwin():
    global main
    
    def concheck():
        global dbpass , dbuser  
        con = sqltor.connect(host="localhost",user=f"{entry_user.get()}",password=f"{entry_pass.get()}")
        con.close()
        dbuser=entry_user.get()
        dbpass=entry_pass.get()
        messagebox.showinfo('Login', "You are logged In")
        az_tracker()

        #except:
            #messagebox.showerror('error', "Invalid Credentials")

    main = tk.Tk()
    main.geometry('400x400')
    main.title("WELCOME")
    main.resizable(False,False)
    label = tk.Label(text='DATABASE LOGIN', font=('Calibiri',20,'bold','underline'))
    label.pack()

    
    entry_user=tk.Entry(main, text='root', fg='black', bg='yellow' )
    entry_user.place(rely=0.2 , relx=0.45)
    entry_user.insert(0,"root")

    label_user= tk.Label(main , text="User",fg='white', bg='black', font=('Arial',10,'bold'))
    label_user.place(rely=0.2 , relx=0.2 , relwidth=0.2)

    entry_pass=tk.Entry(main, fg='black', bg='yellow',show="*")
    entry_pass.place(rely=0.30 , relx=0.45)
    
    label_pass= tk.Label(main , text="Password",fg='white', bg='black', font=('Arial',10,'bold'))
    label_pass.place(rely=0.30 , relx=0.2 , relwidth =0.2)
    
    button1=tk.Button(text='Login', fg='black', bg='yellow', command= lambda: concheck())
    button1.place(relx=0.3, rely=0.42 , relwidth=0.45)

    
    
    

    main.mainloop()
mainwin()
