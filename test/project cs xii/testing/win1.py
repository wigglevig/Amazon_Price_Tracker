import tkinter as tk
from tkinter import ttk
datawin = tk.Tk()
datawin.title("Amazon Price Tracker")
datawin.iconbitmap(r'aztrackericon.ico')
app_height = 600
app_width  = 600
screen_width = datawin.winfo_screenwidth()
screen_height = datawin.winfo_screenheight()
x = (screen_width / 2) - (app_width/2)
y = (screen_height / 2) - (app_height/2)

datawin.geometry(f'{app_width}x{app_height}+{int(x)}+{int(y)-10}')
#datawin.resizable(False,False)
s = ttk.Style(datawin)
s.theme_use("clam")

tree = ttk.Treeview(datawin, show="headings", height='10')
tree['columns'] = ("Sno.","NAME", "PRICE", "EMAIL","LIMPRICE","Date","ASIN","Link")
tree.column("#0", width=120 , minwidth=25)
tree.column("Sno.", anchor='center', width = 38 , minwidth=25)
tree.column("NAME", anchor='w' , width= 120, minwidth=50)
tree.column("PRICE" ,anchor='center' , width= 100, minwidth=50)
tree.column("EMAIL", anchor ='center', width= 122 , minwidth=50)
tree.column("LIMPRICE", anchor='center' , width=80, minwidth=30 )
tree.column("Date", anchor='center' , width=150, minwidth=30 )
tree.column("ASIN", anchor='center' , width=100, minwidth=30 )
tree.column("Link", anchor='center' , width=220, minwidth=30 )
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
#tree.pack(side = 'left' , anchor='s' )

# For SCROLLBAR
xscrollbar = ttk.Scrollbar(datawin, orient='horizontal', command = tree.xview)
xscrollbar.pack(side='bottom', fill='x')

yscrollbar = ttk.Scrollbar(datawin, orient='vertical', command = tree.yview)
yscrollbar.place(anchor='e', relx=1, rely=0.77 , relheight=0.4)

tree.configure(xscrollcommand=xscrollbar.set)
tree.configure(yscrollcommand=yscrollbar.set)


datawin.mainloop()