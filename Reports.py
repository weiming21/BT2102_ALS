from tkinter import *
from tkinter import ttk
from Template import *

class Reports(Template):
    def __init__(self, root=None,app=None):
        self.root = root
        self.app = app
        self.frame = Frame(self.root, bg = 'floral white')
        self.frame.pack(fill=BOTH, expand=True)
        global con
        global cur
        con, cur = self.connect_database()

        headingLabel = Label(self.frame, text="Select one of the options below:", bg='light blue', fg='black', font=('Courier', 15, 'bold'))
        headingLabel.place(relx=0.1,rely=0.11,relwidth=0.8,relheight=0.1)

        dummy_label = Label(self.frame)
        dummy_label.place(relx=0.1,rely=0.3,relwidth=0.28,relheight=0.5)
        self.images = self.load_image(dummy_label)
        image_label= Label(self.frame, image = self.images[3], compound="center")
        image_label.place(relx=0.1,rely=0.3,relwidth=0.28,relheight=0.5)

        Button(self.frame, text = "Book Search", bg='light blue', fg='black', font=('Courier', 15, 'bold'), command = lambda: self.switch_frame(self.frame_one()))\
            .place(relx=0.4,rely=0.27,relwidth=0.2,relheight=0.1)
        Label(self.frame, text = "Search from a\ncollection of books", font="Verdana 15").place(relx=0.6, rely=0.29, relwidth=0.3, relheight=0.06)
        Button(self.frame, text = "Books on Loan", bg='light blue', fg='black', font=('Courier', 15, 'bold'), command = lambda: self.loan_report())\
            .place(relx=0.4,rely=0.38,relwidth=0.2,relheight=0.1)
        Label(self.frame, text = "Display all books\ncurrently on loan", font="Verdana 15").place(relx=0.6, rely=0.4, relwidth=0.3, relheight=0.06)
        Button(self.frame, text = "Book \nReservation", bg='light blue', fg='black', font=('Courier', 15, 'bold'), command = lambda: self.reservation_report())\
            .place(relx=0.4,rely=0.49,relwidth=0.2,relheight=0.1)
        Label(self.frame, text = "Display all books\ncurrently reserved", font="Verdana 15").place(relx=0.6, rely=0.51, relwidth=0.3, relheight=0.06)
        Button(self.frame, text = "Outstanding\nFines", bg='light blue', fg='black', font=('Courier', 15, 'bold'), command = lambda: self.fine_report())\
            .place(relx=0.4,rely=0.60,relwidth=0.2,relheight=0.1)
        Label(self.frame, text = "Display all members\nwith outstanding fines", font="Verdana 15").place(relx=0.6, rely=0.62, relwidth=0.3, relheight=0.06)
        Button(self.frame, text = "Books on Loan\nto Member", bg='light blue', fg='black', font=('Courier', 15, 'bold'), command = lambda: self.switch_frame(self.frame_two()))\
            .place(relx=0.4,rely=0.71,relwidth=0.2,relheight=0.1)
        Label(self.frame, text = "Display all books\na member borrowed", font="Verdana 15").place(relx=0.6, rely=0.73, relwidth=0.3, relheight=0.06)

        menu_btn = Button(self.frame, text="Back To Main Menu", highlightbackground='blue', fg = "black", font=('Courier', 15, 'bold'), command=lambda: self.go_to_main())
        menu_btn.place(relx=0.1, rely=0.9, relwidth=0.8, relheight=0.06)

    def frame_one(self):
        frame = Frame(self.root, bg = 'floral white')

        headingLabel = Label(frame, text="Search based on ONLY ONE of the categories below:", bg='light blue', fg='black', font=('Courier', 15, 'bold'))
        headingLabel.place(relx=0.1,rely=0.11,relwidth=0.8,relheight=0.1)
      
        title_field, author_field, ISBN_field, publisher_field, year_field = ttk.Entry(frame), ttk.Entry(frame), ttk.Entry(frame), ttk.Entry(frame), ttk.Entry(frame)
        labels = ["Title", "Authors", "ISBN", "Publisher", "Publication Year"]
        widgets = [title_field, author_field, ISBN_field, publisher_field, year_field]

        for i in range(len(labels)):
            Label(frame, text = f"{labels[i]}", bg='light blue', fg='black', font=('Courier', 15, 'bold')).place(relx=0.1,rely=0.26 + 0.09*i,relwidth=0.2,relheight=0.08)
            widgets[i].place(relx=0.3,rely=0.26 + 0.09*i,relwidth=0.6,relheight=0.08)
        
        fields = [title_field, author_field, ISBN_field, publisher_field, year_field]

        create_btn = Button(frame, text = "Search Book", highlightbackground='blue', fg = "black", font=('Courier', 15, 'bold'), command=lambda: self.search(fields))
        create_btn.place(relx=0.15, rely=0.85, relwidth=0.3, relheight=0.1)

        menu_btn = Button(frame, text="Back To Reports Menu", highlightbackground='blue', fg = "black", font=('Courier', 15, 'bold'), command=lambda: self.reset())
        menu_btn.place(relx=0.55, rely=0.85, relwidth=0.3, relheight=0.1)
        return frame

    def frame_two(self):
        frame = Frame(self.root, bg = 'floral white')

        headingLabel = Label(frame, text="Books On Loan To Member", bg='light blue', fg='black', font=('Courier', 15, 'bold'))
        headingLabel.place(relx=0.1,rely=0.11,relwidth=0.8,relheight=0.1)

        Label(frame, text = "Membership ID", bg='light blue', fg='black', font=('Courier', 15, 'bold')).place(relx=0.1,rely=0.45,relwidth=0.2,relheight=0.1)
        ID_field = ttk.Entry(frame, width= 30)
        ID_field.place(relx=0.3,rely=0.45,relwidth=0.6,relheight=0.1)

        delete_btn = Button(frame, text = "Search Member", highlightbackground='blue', fg = "black", font=('Courier', 15, 'bold'), command=lambda: self.specific_loan(ID_field))
        delete_btn.place(relx=0.15, rely=0.85, relwidth=0.3, relheight=0.1)

        menu_btn = Button(frame, text="Back To Reports Menu", highlightbackground='blue', fg = "black", font=('Courier', 15, 'bold'), command=lambda: self.reset())
        menu_btn.place(relx=0.55, rely=0.85, relwidth=0.3, relheight=0.1)
        return frame


    def report_type_one(self):
        headings = ("Accession Number", "Title", "Authors", "ISBN", "Publisher", "Year")
        widths = (100, 200, 300, 150, 100, 100)
        return self.report_type(30, headings, widths)

    def report_type_two(self):
        headings = ("Accession Number", "Title", "Membership ID", "Name")
        widths = (100, 200, 300, 150)
        return self.report_type(30, headings, widths)

    def report_type_three(self):
        headings = ("Membership ID", "Name", "Faculty", "Phone Number", "Email Address")
        widths = (100, 200, 200, 200, 200)
        return self.report_type(30, headings, widths)

    def update(self, trv_type, rows):
        for i in rows:
            trv_type.insert("", 'end', values=i)

    def loan_report(self):
        cur.execute("\
            SELECT b.accessionNo, title, GROUP_CONCAT(a.name SEPARATOR ', ') AS Authors, ISBN, publisher, publicationYr \
                FROM Books b JOIN BorrowedBooks b2 ON b.accessionNo = b2.borrowedBookID \
                    JOIN Authors a ON b.accessionNo = a.accessionNo \
                        WHERE b2.returnedDate IS NULL \
                        GROUP BY accessionNo"
        )
        results = cur.fetchall()
        self.update(self.report_type_one(), results)
        con.commit()


    def reservation_report(self):
        cur.execute("\
            SELECT b.accessionNo, title, m.membershipID, m.name \
                FROM Books b JOIN ReservedBooks r ON b.accessionNo = r.reservedBookID \
                    JOIN Members m ON m.membershipID = r.reservedUserID"     
        )
        results = cur.fetchall()
        self.update(self.report_type_two(), results)
        con.commit()

    def fine_report(self):
        cur.execute("\
            SELECT membershipID, name, faculty, phoneNo, email \
                FROM Members \
                    WHERE fineAmt > 0"
        )
        results = cur.fetchall()
        self.update(self.report_type_three(), results)
        con.commit()
        
    def specific_loan(self, ID_field):
        cur.execute("\
            SELECT b.accessionNo, title, GROUP_CONCAT(a.name SEPARATOR ', ') AS Authors, ISBN, publisher, publicationYr \
                FROM BorrowedBooks b2 JOIN Books b ON b.accessionNo = b2.borrowedBookID \
                    JOIN Authors a ON b.accessionNo = a.accessionNo \
                        WHERE b2.borrowedUserID = %s AND b.isBorrowed = TRUE\
                            GROUP BY b.accessionNo", ID_field.get()
        )
        results = cur.fetchall()
        self.update(self.report_type_one(), results)
        con.commit()

    def search(self, fields):
        title_field, author_field, ISBN_field, publisher_field, year_field = fields
        title, authors, isbn, publisher, year = title_field.get(), author_field.get(), ISBN_field.get(), publisher_field.get(), year_field.get()
        
        if len(title.split(" ")) > 1 or len(authors.split(" ")) > 1 or len(publisher.split(" ")) > 1:
            self.createPopUp("red", "Error", "Please only search for one word", "Search")
            return

        query_1 = "\
            SELECT b.accessionNo, title, GROUP_CONCAT(a.name SEPARATOR ', ') AS Authors, ISBN, publisher, publicationYr \
                FROM Books b JOIN Authors a ON b.accessionNo = a.accessionNo "

        query_2 = " GROUP BY b.accessionNo"

        if isbn:
            cur.execute(query_1 + "WHERE isbn = %s" + query_2, isbn)
            result = cur.fetchall()
            con.commit()
        elif year:
            cur.execute(query_1 + "WHERE publicationYr = %s" + query_2, year)
            result = cur.fetchall()
            con.commit()
        elif title:
            title = '([[:blank:][:punct:]]|^)' + title + '([[:blank:][:punct:]]|$)'
            cur.execute(query_1 + "WHERE title REGEXP %s" + query_2, title)
            result = cur.fetchall()
            con.commit()
        elif authors:
            authors = '([[:blank:][:punct:]]|^)' + authors + '([[:blank:][:punct:]]|$)'
            cur.execute(query_1 + "WHERE b.accessionNo IN (SELECT b.accessionNo \
                FROM Books b JOIN Authors a ON b.accessionNo = a.accessionNo \
                    WHERE a.name REGEXP %s)" + query_2, authors)
            result = cur.fetchall()
            
        elif publisher:
            publisher = '([[:blank:][:punct:]]|^)' + publisher + '([[:blank:][:punct:]]|$)'
            cur.execute(query_1 + "WHERE publisher REGEXP %s" + query_2, publisher)
            result = cur.fetchall()
        
        self.update(self.report_type_one(), result)
        con.commit()