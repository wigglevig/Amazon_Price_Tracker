from bs4 import BeautifulSoup
import smtplib
import requests
import threading
from tkinter import messagebox , ttk
import tkinter as tk
import mysql.connector as sqltor



#API FOR GETTING PRICE AND NAME OF THE PRODUCT

def get_link_data(url):
    
    headers = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36",
    "Accept-language":'en',}
    r = requests.get(url, headers=headers)
    soup= BeautifulSoup(r.text , "lxml")
    
    global prod_name , asin
    prod_name = soup.select_one('#productTitle').getText().strip()[0:55]

    avail = soup.select_one('#availability').getText().strip().replace('\n','').split ('.')

    try:
        asin = url.split('/dp/')[1].split('?')[0]
    except:
        asin = url.split('/dp/')[1].split('/')[0]
    Check_avail(avail)
    global price
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
    compare_price(price)    

       
    return None

   
def send_email():
    server = smtplib.SMTP('smtp.gmail.com', 587 )
    server.ehlo()
    server.starttls()
    server.ehlo()
    
    server.login('azpricetrackerbot@gmail.com',"zjewhxbcebsgniny")
    
    subject = "Hi,The price fell down!"
    body = f"Check The amazon link {entry1.get()} "

    msg=f"Subject: {subject}\n\n{body}"
    
    server.sendmail(
        "azpricetrackerbot@gmail.com",
        f"{entry2.get()}",
        msg)
    
    
    
    messagebox.showinfo('Info','Hey the price has been decreased check your Email')    
   

def dbstor():
    
    con = sqltor.connect(host="localhost",user=f"{dbuser}",password=f"{dbpass}")
    cur = con.cursor()
    cur = con.cursor(buffered=True) 
    
    #cur.execute("create database if not exists AZ_PRICE_TRACKER")
    cur.execute("use AZ_PRICE_TRACKER")
    #cur.execute("CREATE TABLE if not exists Az_list(Name VARCHAR(255) PRIMARY KEY, Price VARCHAR(40),Email VARCHAR(40), Limitprice VARCHAR(40), Date DATETIME ,asin VARCHAR(15), Link VARCHAR(65535))")
    link = f'https://www.amazon.in/dp/{asin}'

    cur.execute('INSERT into Az_list values(%s,%s,%s,%s,now(),%s,%s)' , (prod_name, price ,entry2.get(), entry3.get(), asin, link))
    con.commit()
    messagebox.showinfo("Info","Item stored in database successfully.\n Thank You")
    con.close()
    # except:
    #     messagebox.showerror("Error", "Duplicate entry")

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
        

def compare_price(price):

    if price <= float(entry3.get()):
        dbstor() 
        #send_email()
       
    else:
        messagebox.showinfo('Info',f'Price Limit Specified is less than the current price\n Current price of the prdouct is {price}')
         
    return None              



def az_tracker():
    global datawin , dbuser , dbpass
    datawin = tk.Tk()
    datawin.title("Amazon Price Tracker")
    datawin.iconbitmap(r'aztrackericon.ico')
    app_height = 600
    app_width  = 600
    screen_width = datawin.winfo_screenwidth()
    screen_height = datawin.winfo_screenheight()
    x = (screen_width / 2) - (app_width/2)
    y = (screen_height / 2) - (app_height/2)

    datawin.geometry(f'{app_width}x{app_height}+{int(x)}+{int(y)-20}')
    #datawin.resizable(False,False)
    s = ttk.Style(datawin)
    s.theme_use("clam")
    
    
    # _FOR TREEVIEW__FOR TREEVIEW___FOR TREEVIEW__FOR TREEVIEW__FOR TREEVIEW___FOR TREEVIEW__FOR TREEVIEW__FOR TREEVIEW__FOR TREEVIEW__FOR TREEVIEW__
    
    
    tree = ttk.Treeview(datawin, show="headings", height='10')
    
    # CREATING OUR COLUMNS
    tree['columns'] = ("Sno.","NAME", "PRICE", "EMAIL","LIMPRICE","Date","ASIN","Link")
    tree.column("#0", width=120 , minwidth=25)
    tree.column("Sno.", anchor='center', width = 38 , minwidth=25)
    tree.column("NAME", anchor='w' , width= 120, minwidth=50)
    tree.column("PRICE" ,anchor='center' , width= 100, minwidth=50)
    tree.column("EMAIL", anchor ='center', width= 122 , minwidth=50)
    tree.column("LIMPRICE", anchor='center' , width=80, minwidth=30 )
    tree.column("Date", anchor='center' , width=150, minwidth=30 )
    tree.column("ASIN", anchor='center' , width=100, minwidth=30 )
    tree.column("Link", anchor='w' , width=260, minwidth=30 )
    #creating Headings
    #tree.heading('#0', text="label" , anchor ='w')
    tree.heading("Sno." , text="S_No.", anchor='center')
    tree.heading('NAME', text="Name" , anchor ='center')
    tree.heading('PRICE', text="Product Price" , anchor='center')
    tree.heading('EMAIL', text ='Email' , anchor='center')
    tree.heading('LIMPRICE', text="Limit price" , anchor ='center')
    tree.heading("Date", text="Date" , anchor ='center')
    tree.heading("ASIN", text="ASIN" , anchor ='center')
    tree.heading("Link", text="Prod_Link" , anchor ='center')


    # For SCROLLBAR
    xscrollbar = ttk.Scrollbar(datawin, orient='horizontal', command = tree.xview)
    xscrollbar.pack(side='bottom', fill='x')

    yscrollbar = ttk.Scrollbar(datawin, orient='vertical', command = tree.yview)
    yscrollbar.place(anchor='e', relx=1, rely=0.806, height=203)
    
    tree.configure(xscrollcommand=xscrollbar.set)
    tree.configure(yscrollcommand=yscrollbar.set)
    # Creating DATABASE 
    
    con = sqltor.connect(host="localhost",user=f'{dbuser}',password=f'{dbpass}')
    cur = con.cursor(buffered=True)
    cur.execute("create database if not exists AZ_PRICE_TRACKER")
    cur.execute("USE AZ_PRICE_TRACKER")
    cur.execute("CREATE TABLE if not exists Az_list(Name VARCHAR(255) PRIMARY KEY, Price VARCHAR(40),Email VARCHAR(40), Limitprice VARCHAR(40) , Date DATETIME ,ASIN VARCHAR(30) , LINK TEXT)")
    cur.execute("SELECT * from Az_list Order by date")
    rows = cur.fetchall()
    con.close()

    # ADDING DATA TO TREEVIEW FROM DATABASE 
    a=1
    for i in rows:
        tree.insert('',a,values = (a,i[0],i[1],i[2],i[3],i[4],i[5],i[6]))
        a=a+1
            
    tree.pack(side = 'left' , anchor='s' )

    def refresh():
        datawin.destroy()
        az_tracker()    

    def select():
        entry1.configure(state='normal')
        entry1.delete("0","end")
        entry2.delete("0","end")
        entry3.delete("0","end")

        selected = tree.focus()
        values = tree.item(selected ,'values')

        
        entry2.insert(0 ,values[3])
        entry3.insert(0 ,values[4])
        entry1.insert(0, values[7])     
        entry1.configure(state='readonly')

    def update_record():
        selected = tree.focus()
        values = tree.item(selected ,'values')
        #print(type(entry3.get()) , type(entry2.get()))
        if entry3.get()!='' and entry2.get()!='':
            con = sqltor.connect(host="localhost",user=f"{dbuser}",password=f"{dbpass}")
            cur = con.cursor()
            cur.execute("USE AZ_PRICE_TRACKER")
            cur.execute("UPDATE az_list SET Limitprice=%s , Email=%s where ASIN = %s", (entry3.get() , entry2.get() , values[6] ))
            con.commit()
            con.close()
            messagebox.showinfo("Update","Record Updated successfully")
            tree.item(selected, values=(values[0],values[1],values[2],entry2.get(),entry3.get(),values[5],values[6],values[7]))
        else:
            messagebox.showerror("No Entry", "No entry Found")


    def remove_record():
        selected = tree.focus()
        values = tree.item(selected ,'values')
        con = sqltor.connect(host="localhost",user=f"{dbuser}",password=f"{dbpass}")
        cur = con.cursor()
        cur.execute("USE AZ_PRICE_TRACKER") 
        cur.execute(f"Delete from az_list where ASIN='{values[6]}'")
        con.commit()
        con.close()
        messagebox.showinfo("Update","Record Deleted successfully")
        datawin.destroy()
        az_tracker()








    def clearTextInput():
        entry1.delete("0","end")
        entry2.delete("0","end")
        entry3.delete("0","end")
    
        
    global entry1,entry2,entry3

       

    frame = tk.Frame(datawin , bg ='#747474' )
    frame.place(relx=0.5 ,rely=0, relwidth=1 , relheight=0.55, anchor='n')

    background_img= tk.PhotoImage(file='bgimage1.png')
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



    button1=tk.Button(frame , text='Add', command=run_app , bg='#ff9a00', font=('Arial',12,'bold'))
    button1.place(anchor='s', relx=0.10, relwidth=0.10, relheight=0.1, rely=0.95)



    button2=tk.Button(frame , text='Clear', bg='#ff9a00', command = clearTextInput ,font=('Arial',12,'bold'))
    button2.place(anchor='s', relx=0.25 , relwidth=0.10, relheight=0.1, rely=0.95)

    button3=tk.Button(frame , text='Refresh', bg='#ff9a00', font=('Arial',12,'bold') , command =refresh)
    button3.place(anchor='s', relx=0.40 , relwidth=0.12, relheight=0.1, rely=0.95)


    button4=tk.Button(frame , text='Select' ,bg='#ff9a00', font=('Arial',12,'bold'), command = select)
    button4.place(anchor='s', relx=0.55 , relwidth=0.10, relheight=0.1, rely=0.95)

    button5=tk.Button(frame , text='Update' ,bg='#ff9a00', font=('Arial',12,'bold') , command = update_record)
    button5.place(anchor='s', relx=0.70 , relwidth=0.12, relheight=0.1, rely=0.95)

    button6=tk.Button(frame , text='Remove' ,bg='#ff9a00', font=('Arial',12,'bold') , command= remove_record)
    button6.place(anchor='s', relx=0.87 , relwidth=0.15, relheight=0.1, rely=0.95)


    datawin.mainloop()


def mainwin():
    global main
    
    def concheck(*args):
        global dbpass , dbuser  
        
        con = sqltor.connect(host="localhost",user=f"{entry_user.get()}",password=f"{entry_pass.get()}")
        con.close()
        dbuser=entry_user.get()
        dbpass=entry_pass.get()
        messagebox.showinfo('Login', "You are logged In")
        main.destroy()
        az_tracker()

        # except:
        #     messagebox.showerror('error', "Invalid Credentials")

    main = tk.Tk()
    main.iconbitmap(r'dbicon.ico')
    app_height = 200
    app_width  = 300
    screen_width = main.winfo_screenwidth()
    screen_height = main.winfo_screenheight()
    x = (screen_width / 2) - (app_width/2)
    y = (screen_height / 2) - (app_height/2)

    main.geometry(f'{app_width}x{app_height}+{int(x)}+{int(y)}')
    #main.geometry('300x200')
    main.title("DATABASE LOGIN")
    main['bg']='#330606'
    main.resizable(False,False)
    label = tk.Label(text='WELCOME', font=('Calibiri',20,'bold','underline'), bg='pink')
    label.pack()

    
    entry_user=tk.Entry(main, text='root', fg='black', bg='yellow' )
    entry_user.place(rely=0.2 , relx=0.42)
    entry_user.insert(0,"root")

    label_user= tk.Label(main , text="User",fg='white', bg='black', font=('Arial',10,'bold'))
    label_user.place(rely=0.2 , relx=0.2 , relwidth=0.2)

    entry_pass=tk.Entry(main, fg='black', bg='yellow',show="*")
    entry_pass.place(rely=0.30 , relx=0.42)
    entry_pass.focus_set()
    label_pass= tk.Label(main , text="Password",fg='white', bg='black', font=('Arial',10,'bold'))
    label_pass.place(rely=0.30 , relx=0.2 , relwidth =0.2)
    
    button1=tk.Button(text='Login', fg='black', bg='pink', command= lambda: concheck())
    button1.place(relx=0.4, rely=0.42 , relwidth=0.35)
    
    main.bind('<Return>',concheck)
    main.mainloop()


mainwin()
