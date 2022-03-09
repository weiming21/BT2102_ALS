from datetime import date
from tkinter import *
from tkinter import ttk
from Books import Books
from Template import *

class Reservations(Template):
    def __init__(self, root=None,app=None):
        self.root = root
        self.app = app
        self.frame = Frame(self.root, bg = 'floral white')
        self.frame.pack(fill=BOTH, expand=True)
        global con
        global cur
        con, cur = self.connect_database()
    
        headingLabel = Label(self.frame, text="Select one of the options below:", bg='light blue', fg='black', font=('Courier', 20, 'bold'))
        headingLabel.place(relx=0.1,rely=0.1,relwidth=0.8,relheight=0.1)

        dummy_label = Label(self.frame)
        dummy_label.place(relx=0.1,rely=0.3,relwidth=0.28,relheight=0.5)
        self.images = self.load_image(dummy_label)
        image_label= Label(self.frame, image = self.images[2], compound="center")
        image_label.place(relx=0.1,rely=0.3,relwidth=0.28,relheight=0.5)

        reserve_btn = Button(self.frame, text="Reserve", highlightbackground='mint cream', fg = "black", font=('Courier', 15, 'bold'), command=lambda: self.switch_frame(self.reserve_page()))
        reserve_btn.place(relx=0.4, rely=0.35, relwidth=0.2, relheight=0.2)
        Label(self.frame, text = "Book Reservation", font="Verdana 15").place(relx=0.6, rely=0.4, relwidth=0.3, relheight=0.1)
        cancel_btn = Button(self.frame, text="Cancel", highlightbackground='mint cream', fg = "black", font=('Courier', 15, 'bold'), command=lambda: self.switch_frame(self.cancel_page()))
        cancel_btn.place(relx=0.4, rely=0.55, relwidth=0.2, relheight=0.2)
        Label(self.frame, text = "Reservation Cancellation", font="Verdana 15").place(relx=0.6, rely=0.6, relwidth=0.3, relheight=0.1)

        menu_btn = Button(self.frame, text="Back To Main Menu", highlightbackground='blue', fg = "black", font=('Courier', 15, 'bold'), command=lambda: self.go_to_main())
        menu_btn.place(relx=0.1, rely=0.9, relwidth=0.8, relheight=0.06)
       
    def reserve_page(self):
        frame = Frame(self.root, bg = 'floral white')

        headingLabel = Label(frame, text="To Reserve a Book, Please Enter Information Below:", bg='light blue', fg='black', font=('Courier', 15, 'bold'))
        headingLabel.place(relx=0.1,rely=0.11,relwidth=0.8,relheight=0.1)

        Label(frame, text = "Accession Number", bg='light blue', fg='black', font=('Courier', 15, 'bold')).place(relx=0.1,rely=0.3,relwidth=0.2,relheight=0.1)
        BookID_field = ttk.Entry(frame, width= 30)
        BookID_field.place(relx=0.3,rely=0.3,relwidth=0.6,relheight=0.1)

        Label(frame, text = "Membership ID", bg='light blue', fg='black', font=('Courier', 15, 'bold')).place(relx=0.1,rely=0.41,relwidth=0.2,relheight=0.1)
        ID_field = ttk.Entry(frame, width= 30)
        ID_field.place(relx=0.3,rely=0.41,relwidth=0.6,relheight=0.1)

        Label(frame, text = "Reserve Date (DD/MM/YYYY)", bg='light blue', fg='black', font=('Courier', 15, 'bold')).place(relx=0.1,rely=0.52,relwidth=0.2,relheight=0.1)
        date_field = ttk.Entry(frame, width= 30)
        date_field.place(relx=0.3,rely=0.52,relwidth=0.6,relheight=0.1)

        fields = [BookID_field, ID_field, date_field]

        delete_btn = Button(frame, text = "Reserve Book", highlightbackground='blue', fg = "black", font=('Courier', 15, 'bold'), command=lambda: self.reserve(fields))
        delete_btn.place(relx=0.15, rely=0.85, relwidth=0.3, relheight=0.1)

        menu_btn = Button(frame, text="Back To Reservations Menu", highlightbackground='blue', fg = "black", font=('Courier', 15, 'bold'), command=lambda: self.reset())
        menu_btn.place(relx=0.55, rely=0.85, relwidth=0.3, relheight=0.1)
        return frame

    def cancel_page(self):
        frame = Frame(self.root, bg = 'floral white')

        headingLabel = Label(frame, text="To Cancel a Book, Please Enter Information Below:", bg='light blue', fg='black', font=('Courier', 15, 'bold'))
        headingLabel.place(relx=0.1,rely=0.11,relwidth=0.8,relheight=0.1)

        Label(frame, text = "Accession Number", bg='light blue', fg='black', font=('Courier', 15, 'bold')).place(relx=0.1,rely=0.3,relwidth=0.2,relheight=0.1)
        BookID_field = ttk.Entry(frame, width= 30)
        BookID_field.place(relx=0.3,rely=0.3,relwidth=0.6,relheight=0.1)

        Label(frame, text = "Membership ID", bg='light blue', fg='black', font=('Courier', 15, 'bold')).place(relx=0.1,rely=0.41,relwidth=0.2,relheight=0.1)
        ID_field = ttk.Entry(frame, width= 30)
        ID_field.place(relx=0.3,rely=0.41,relwidth=0.6,relheight=0.1)

        Label(frame, text = "Cancel Date (DD/MM/YYYY)", bg='light blue', fg='black', font=('Courier', 15, 'bold')).place(relx=0.1,rely=0.52,relwidth=0.2,relheight=0.1)
        date_field = ttk.Entry(frame, width= 30)
        date_field.place(relx=0.3,rely=0.52,relwidth=0.6,relheight=0.1)

        fields = [BookID_field, ID_field, date_field]

        delete_btn = Button(frame, text = "Cancel Reservation", highlightbackground='blue', fg = "black", font=('Courier', 15, 'bold'), command=lambda: self.cancel(fields))
        delete_btn.place(relx=0.15, rely=0.85, relwidth=0.3, relheight=0.1)

        menu_btn = Button(frame, text="Back To Cancellation Menu", highlightbackground='blue', fg = "black", font=('Courier', 15, 'bold'), command=lambda: self.reset())
        menu_btn.place(relx=0.55, rely=0.85, relwidth=0.3, relheight=0.1)
        return frame

    def reserve(self, fields):
        
        def execute(book_id, member_id, date):
            try:
                cur.execute("INSERT INTO ReservedBooks VALUES(%s, %s, STR_TO_DATE(%s, %s))", (book_id, member_id, date, "%d/%m/%Y"))
                con.commit()
                cur.execute("UPDATE Books SET isReserved = TRUE WHERE accessionNo = %s", book_id)
                con.commit()
            except:
                self.createPopUp("red", "Error", "Invalid date format", "Reserve")

        BookID_field, ID_field, date_field = fields
        if not BookID_field.get() or not ID_field.get() or not date_field.get():
            self.createPopUp("red", "Error", "Please enter \nrequired information", "Reserve")
            return
        cur.execute("SELECT COUNT(*) FROM ReservedBooks WHERE reservedUserID = %s", ID_field.get())
        no_of_res = cur.fetchone()[0]
        cur.execute("SELECT isReserved FROM Books WHERE accessionNo = %s", BookID_field.get())
        book_status = cur.fetchone()
        cur.execute("SELECT fineAmt FROM Members WHERE membershipID = %s", ID_field.get())
        fine = cur.fetchone()

        if not fine or not book_status:
            self.createPopUp("red", "Error", "Member or book does not exist", "Reserve")
        else:
            if no_of_res >= 2:
                self.createPopUp("red", "Error", "Member currently has 2 books \non reservation", "Reserve")
            elif book_status[0]:
                self.createPopUp("red", "Error", "Book has been reserved", "Loan")
            elif fine[0]:
                self.createPopUp("red", "Error", f"Member has outstanding \nfine of ${fine[0]}", "Reserve")
            else:
                cur.execute("SELECT accessionNo, title FROM Books WHERE accessionNo = %s", BookID_field.get())
                results = list(cur.fetchone())
                cur.execute("SELECT membershipID, name FROM Members WHERE membershipID = %s", ID_field.get())
                results.extend(list(cur.fetchone()))
                results.append(date_field.get())
                labels = ["Accession Number", "Book Title", "Membership ID", "Member Name", "Reserve Date"]
                self.createPopUp2("Confirm Reservation Details\n To Be Correct", dict(zip(labels, results)), "Reservation", lambda: execute(BookID_field.get(), ID_field.get(), date_field.get()))

    def cancel(self, fields):
        
        BookID_field, ID_field, date_field = fields
        book_id, member_id, date = BookID_field.get(), ID_field.get(), date_field.get()
        if not book_id or not member_id or not date:
            self.createPopUp("red", "Error", "Please enter \nrequired information", "Cancellation")
            return
        cur.execute("\
            SELECT b.accessionNo, b.title, m.membershipID, m.name \
                FROM ReservedBooks r JOIN Books b ON r.reservedBookID = b.accessionNo \
                    JOIN Members m ON r.reservedUserID = m.membershipID \
                        WHERE reservedBookID = %s AND reservedUserID = %s", (book_id, member_id))
        results = cur.fetchone()
        
        if not results:
            self.createPopUp("red", "Error", "Member has no such reservation", "Cancellation")
        else:
            results += (date,)
            labels = ("Accession Number", "Book Title", "Membership ID", "Member Name", "Cancel Date")
            self.createPopUp2("Confirm Cancellation Details\n To Be Correct", dict(zip(labels, results)), "Cancellation", lambda: execute(book_id, id))
        
        def execute(book_id, id):
            cur.execute("DELETE FROM ReservedBooks WHERE reservedBookID = %s AND reservedUserID = %s", (book_id, member_id))
            con.commit()
            cur.execute("UPDATE Books SET isReserved = FALSE WHERE accessionNo = %s", book_id)
            con.commit()