from tkinter import *
from tkinter import ttk
from Template import *
import pymysql

class Books(Template):

    #connecting to database (can be abstracted into a function)
    # pw = "BT2102group26"
    # db = "ALS"
    # global con
    # global cur
    # con = pymysql.connect(host="localhost",user="root",password=pw,database=db) 
    # cur = con.cursor()

    def __init__(self, root=None,app=None):
        self.root = root
        self.app = app
        self.frame = Frame(self.root, bg = 'floral white')
        self.frame.pack(fill=BOTH, expand=True)
        global con
        global cur
        con, cur = self.connect_database()

        dummy_label = Label(self.frame)
        dummy_label.place(relx=0.1,rely=0.3,relwidth=0.28,relheight=0.5)
        self.images = self.load_image(dummy_label)
        image_label= Label(self.frame, image = self.images[4], compound="center")
        image_label.place(relx=0.1,rely=0.3,relwidth=0.28,relheight=0.5)
    
        headingLabel = Label(self.frame, text="Select one of the options below:", bg='light blue', fg='black', font=('Courier', 20, 'bold'))
        headingLabel.place(relx=0.1,rely=0.1,relwidth=0.8,relheight=0.1)

        create_btn = Button(self.frame, text="Acquire", highlightbackground='mint cream', fg = "black", font=('Courier', 15, 'bold'), command=lambda: self.switch_frame(self.acquire_page()))
        create_btn.place(relx=0.4, rely=0.35, relwidth=0.2, relheight=0.2)
        Label(self.frame, text = "Book Acquisition", font="Verdana 15").place(relx=0.6, rely=0.40, relwidth=0.3, relheight=0.1)
        delete_btn = Button(self.frame, text="Withdraw", highlightbackground='mint cream', fg = "black", font=('Courier', 15, 'bold'), command=lambda: self.switch_frame(self.withdraw_page()))
        delete_btn.place(relx=0.4, rely=0.55, relwidth=0.2, relheight=0.2)
        Label(self.frame, text = "Book Withdrawal", font="Verdana 15").place(relx=0.6, rely=0.60, relwidth=0.3, relheight=0.1)

        menu_btn = Button(self.frame, text="Back To Main Menu", highlightbackground='blue', fg = "black", font=('Courier', 15, 'bold'), command=lambda: self.go_to_main())
        menu_btn.place(relx=0.1, rely=0.9, relwidth=0.8, relheight=0.06)

    def acquire_page(self):
        frame = Frame(self.root, bg = 'floral white')

        headingLabel = Label(frame, text="For New Book Acquisition, Please Enter Required Information Below:", bg='light blue', fg='black', font=('Courier', 15, 'bold'))
        headingLabel.place(relx=0.1,rely=0.11,relwidth=0.8,relheight=0.1)
      
        BookID_field, title_field, author_field, ISBN_field, publisher_field, year_field = ttk.Entry(frame), ttk.Entry(frame), ttk.Entry(frame), ttk.Entry(frame), ttk.Entry(frame), ttk.Entry(frame)
        labels = ["Accession Number", "Title", "Authors", "ISBN", "Publisher", "Publication Year"]
        widgets = [BookID_field, title_field, author_field, ISBN_field, publisher_field, year_field]

        for i in range(len(labels)):
            Label(frame, text = f"{labels[i]}", bg='light blue', fg='black', font=('Courier', 15, 'bold')).place(relx=0.1,rely=0.26 + 0.09*i,relwidth=0.2,relheight=0.08)
            widgets[i].place(relx=0.3,rely=0.26 + 0.09*i,relwidth=0.6,relheight=0.08)

        fields = [BookID_field, title_field, author_field, ISBN_field, publisher_field, year_field]

        create_btn = Button(frame, text = "Add New Book", highlightbackground='blue', fg = "black", font=('Courier', 15, 'bold'), command=lambda: self.acquire(fields))
        create_btn.place(relx=0.15, rely=0.85, relwidth=0.3, relheight=0.1)

        menu_btn = Button(frame, text="Back To Books Menu", highlightbackground='blue', fg = "black", font=('Courier', 15, 'bold'), command=lambda: self.reset())
        menu_btn.place(relx=0.55, rely=0.85, relwidth=0.3, relheight=0.1)
        return frame

    def withdraw_page(self):
        frame = Frame(self.root, bg = 'floral white')

        headingLabel = Label(frame, text=" To Remove Outdated Books From System, Please Enter Required Information Below:", bg='light blue', fg='black', font=('Courier', 15, 'bold'))
        headingLabel.place(relx=0.1,rely=0.11,relwidth=0.8,relheight=0.1)

        Label(frame, text = "Accession Number", bg='light blue', fg='black', font=('Courier', 15, 'bold')).place(relx=0.1,rely=0.45,relwidth=0.2,relheight=0.1)
        ID_field = ttk.Entry(frame, width= 30)
        ID_field.place(relx=0.3,rely=0.45,relwidth=0.6,relheight=0.1)

        delete_btn = Button(frame, text = "Withdraw Book", highlightbackground='blue', fg = "black", font=('Courier', 15, 'bold'), command=lambda: self.withdraw(ID_field))
        delete_btn.place(relx=0.15, rely=0.85, relwidth=0.3, relheight=0.1)

        menu_btn = Button(frame, text="Back To Books Menu", highlightbackground='blue', fg = "black", font=('Courier', 15, 'bold'), command=lambda: self.reset())
        menu_btn.place(relx=0.55, rely=0.85, relwidth=0.3, relheight=0.1)
        return frame

    def acquire(self, fields):
        BookID, title, authors, isbn, publisher, year = fields
        author_list = list(authors.get().split(","))
        if not (BookID.get() and title.get() and authors.get() and isbn.get() and publisher.get() and year.get()):
            self.createPopUp("red", "Error", "Missing\n or Incomplete fields", "Acquisition")
        else:
            cur.execute("SELECT * FROM Books WHERE accessionNo = %s", BookID.get())
            result = cur.fetchone()        
            if not result:
                cur.execute("INSERT INTO Books VALUES(%s, %s, %s, %s, %s, DEFAULT, DEFAULT)",
                    (BookID.get(), isbn.get(), title.get(), publisher.get(), year.get()))
                con.commit()
                for author in author_list:
                    cur.execute("INSERT INTO Authors VALUES(%s, %s)", (BookID.get(), author))
                    con.commit()
                self.createPopUp("green", "Success!", "New Book added in Library", "Acquisition")
            else:
                self.createPopUp("red", "Error", "Book already exists", "Acquisition")   

    def withdraw(self, ID_field):

        def execute(id):
            cur.execute("DELETE FROM Books WHERE accessionNo = %s", id)
            con.commit()

        id = ID_field.get()
        if not id:
            self.createPopUp("red", "Error", "Please enter \nAccession Number", "Delete")
        else:
            cur.execute("SELECT * FROM Books WHERE accessionNo = %s", id)
            book_exists = cur.fetchone()
            con.commit()
            cur.execute("SELECT isBorrowed, isReserved FROM Books WHERE accessionNo = %s", id)
            is_borrowed, is_reserved = cur.fetchone()
            con.commit()

            if not book_exists:
                self.createPopUp("red", "Error", "Book does not exist", "Withdrawal")
            elif is_borrowed:
                self.createPopUp("red", "Error", "Book is currently on Loan", "Withdrawal")
            elif is_reserved:
                self.createPopUp("red", "Error", "Book is currently reserved", "Withdrawal")
            else:
                cur.execute("SELECT b.accessionNo, title, GROUP_CONCAT(a.name SEPARATOR ', ') AS Authors, ISBN, publisher, publicationYr \
                    FROM Books b JOIN Authors a ON b.accessionNo = a.accessionNo WHERE b.accessionNo = %s GROUP BY accessionNo", id)
                result = cur.fetchone()
                con.commit()
                labels = ("Accession Number", "Title", "Authors", "ISBN", "Publisher", "Year")
                self.createPopUp2("Please Comfirm Details\n To Be Correct", dict(zip(labels, result)), "Withdrawal", lambda: execute(id))