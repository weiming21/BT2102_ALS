from ast import excepthandler
from tkinter import *
from tkinter import ttk
from Template import *
import datetime

class Loans(Template):
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
        image_label= Label(self.frame, image = self.images[0], compound="center")
        image_label.place(relx=0.1,rely=0.3,relwidth=0.28,relheight=0.5)

        borrow_btn = Button(self.frame, text="Borrow", highlightbackground='mint cream', fg = "black", font=('Courier', 15, 'bold'), command=lambda: self.switch_frame(self.borrow_page()))
        borrow_btn.place(relx=0.4, rely=0.35, relwidth=0.2, relheight=0.2)
        Label(self.frame, text = "Book Borrowing", font="Verdana 15").place(relx=0.6, rely=0.40, relwidth=0.3, relheight=0.1)
        return_btn = Button(self.frame, text="Return", highlightbackground='mint cream', fg = "black", font=('Courier', 15, 'bold'), command=lambda: self.switch_frame(self.return_page()))
        return_btn.place(relx=0.4, rely=0.55, relwidth=0.2, relheight=0.2)
        Label(self.frame, text = "Book Returning", font="Verdana 15").place(relx=0.6, rely=0.60, relwidth=0.3, relheight=0.1)

        menu_btn = Button(self.frame, text="Back To Main Menu", highlightbackground='blue', fg = "black", font=('Courier', 15, 'bold'), command=lambda: self.go_to_main())
        menu_btn.place(relx=0.1, rely=0.9, relwidth=0.8, relheight=0.06)

    def borrow_page(self):
        frame = Frame(self.root, bg = 'floral white')

        headingLabel = Label(frame, text="  To Borrow a Book, Please Enter Information Below:", bg='light blue', fg='black', font=('Courier', 15, 'bold'))
        headingLabel.place(relx=0.1,rely=0.11,relwidth=0.8,relheight=0.1)

        Label(frame, text = "Accession Number", bg='light blue', fg='black', font=('Courier', 15, 'bold')).place(relx=0.1,rely=0.4,relwidth=0.2,relheight=0.1)
        BookID_field = ttk.Entry(frame, width= 30)
        BookID_field.place(relx=0.3,rely=0.4,relwidth=0.6,relheight=0.1)

        Label(frame, text = "Membership ID", bg='light blue', fg='black', font=('Courier', 15, 'bold')).place(relx=0.1,rely=0.51,relwidth=0.2,relheight=0.1)
        ID_field = ttk.Entry(frame, width= 30)
        ID_field.place(relx=0.3,rely=0.51,relwidth=0.6,relheight=0.1)

        fields = [BookID_field, ID_field]

        delete_btn = Button(frame, text = "Borrow Book", highlightbackground='blue', fg = "black", font=('Courier', 15, 'bold'), command=lambda: self.borrow(fields))
        delete_btn.place(relx=0.15, rely=0.85, relwidth=0.3, relheight=0.1)

        menu_btn = Button(frame, text="Back To Loans Menu", highlightbackground='blue', fg = "black", font=('Courier', 15, 'bold'), command=lambda: self.reset())
        menu_btn.place(relx=0.55, rely=0.85, relwidth=0.3, relheight=0.1)
        return frame

    def return_page(self):
        frame = Frame(self.root, bg = 'floral white')

        headingLabel = Label(frame, text="  To Return a Book, Please Enter Information Below:", bg='light blue', fg='black', font=('Courier', 15, 'bold'))
        headingLabel.place(relx=0.1,rely=0.11,relwidth=0.8,relheight=0.1)

        Label(frame, text = "Accession Number", bg='light blue', fg='black', font=('Courier', 15, 'bold')).place(relx=0.1,rely=0.4,relwidth=0.2,relheight=0.1)
        BookID_field = ttk.Entry(frame, width= 30)
        BookID_field.place(relx=0.3,rely=0.4,relwidth=0.6,relheight=0.1)

        Label(frame, text = "Return Date (DD/MM/YYYY)", bg='light blue', fg='black', font=('Courier', 15, 'bold')).place(relx=0.1,rely=0.51,relwidth=0.2,relheight=0.1)
        date_field = ttk.Entry(frame, width= 30)
        date_field.place(relx=0.3,rely=0.51,relwidth=0.6,relheight=0.1)

        fields = [BookID_field, date_field]

        delete_btn = Button(frame, text = "Return Book", highlightbackground='blue', fg = "black", font=('Courier', 15, 'bold'), command=lambda: self.return_book(fields))
        delete_btn.place(relx=0.15, rely=0.85, relwidth=0.3, relheight=0.1)

        menu_btn = Button(frame, text="Back To Loans Menu", highlightbackground='blue', fg = "black", font=('Courier', 15, 'bold'), command=lambda: self.reset())
        menu_btn.place(relx=0.55, rely=0.85, relwidth=0.3, relheight=0.1)
        return frame
        
    def borrow(self, fields):
        def success(book_id, id, func):
            cur.execute("SELECT membershipID, name FROM Members WHERE membershipID = %s", id)
            member_info = cur.fetchone()
            cur.execute("SELECT accessionNo, title FROM Books WHERE accessionNo = %s", book_id)
            book_info = cur.fetchone()
            today_date = datetime.date.today().strftime("%d/%m/%y")
            due_date = (datetime.date.today() + datetime.timedelta(days=14)).strftime("%d/%m/%y")
            results = list(book_info)
            results.append(today_date)
            results.extend(member_info)
            results.append(due_date)
            labels = ["Accession Number", "Book Title", "Borrow Date", "Membership ID", "Member Name", "Due Date"]
            self.createPopUp2("Please Comfirm Details\n To Be Correct", dict(zip(labels, results)), "Loan", lambda: func(book_id, id))

        def execute(book_id, id):
            try:
                cur.execute("INSERT INTO BorrowedBooks VALUES(%s, %s, CURDATE(), DATE_ADD(CURDATE(), INTERVAL 14 DAY), DEFAULT)", (book_id, id))
                con.commit()
                cur.execute("UPDATE Books SET isBorrowed = TRUE WHERE accessionNo = %s", book_id)
                con.commit()
            except:
                self.createPopUp("Red", "Error","You cannot borrow the\nsame book again today.\nStop wasting the resources!", "Loans")

        def execute_reserved(book_id, id):
            execute(book_id, id)
            cur.execute("DELETE FROM ReservedBooks WHERE reservedBookID = %s", book_id)
            con.commit()
            cur.execute("UPDATE Books SET isReserved = FALSE WHERE accessionNo = %s", book_id)
            con.commit()

        BookID_field, ID_field = fields
        if not ID_field.get() or not BookID_field.get():
            self.createPopUp("red", "Error", "Please enter \nrequired information", "Loan")
        else:
            cur.execute("SELECT isBorrowed FROM Books WHERE accessionNo = %s", BookID_field.get())
            is_borrowed = cur.fetchone()
            cur.execute("SELECT COUNT(*) FROM BorrowedBooks WHERE borrowedUserID = %s AND returnedDate IS NULL", ID_field.get())
            no_of_books = cur.fetchone()
            cur.execute("SELECT fineAmt FROM Members WHERE membershipID = %s", ID_field.get())
            has_fine = cur.fetchone()
            cur.execute("SELECT reservedUserID FROM ReservedBooks WHERE reservedBookID = %s", BookID_field.get())
            reserved_member = cur.fetchone()

            if not is_borrowed or not has_fine:
                self.createPopUp("red", "Error", "Member or book does not exist", "Delete")
            elif is_borrowed[0]:
                cur.execute("SELECT dueDate FROM BorrowedBooks WHERE borrowedBookID = %s AND returnedDate IS NULL", BookID_field.get())
                due_date = cur.fetchone()
                self.createPopUp("red", "Error", f"Book currently on loan until \n{due_date[0]}", "Delete")
            elif no_of_books[0] >= 2:
                self.createPopUp("red", "Error", f"Member loan quota exceeded", "Delete")
            elif has_fine[0]:
                self.createPopUp("red", "Error", f"Member has outstanding fines", "Delete")
            else:
                if not reserved_member:
                    success(BookID_field.get(), ID_field.get(), execute)
                elif reserved_member[0] == ID_field.get():
                    success(BookID_field.get(), ID_field.get(), execute_reserved)
                else:
                    self.createPopUp("red", "Error", f"Book has been reserved", "Delete")
    
    def return_book(self, fields):

        def execute(book_id, date, member_id, fine):
            cur.execute("UPDATE BorrowedBooks SET returnedDate = STR_TO_DATE(%s, %s) \
                WHERE borrowedBookID = %s and returnedDate is NULL", (date, "%d/%m/%Y", book_id))
            con.commit()
            cur.execute("UPDATE Books SET isBorrowed = FALSE WHERE accessionNo = %s", book_id)
            con.commit()
            if fine:
                cur.execute("UPDATE Members SET fineAmt = fineAmt + %s WHERE membershipID = %s", (fine, member_id))
                con.commit()
                self.createPopUp("red", "Error", "Book returned successfully\nbut has fines", "Return")
            else:
                self.createPopUp("green", "Success", "Book returned successfully", "Return")

        BookID_field, date_field = fields
        if not BookID_field.get() or not date_field.get():
            self.createPopUp("red", "Error", "Please enter \nrequired information", "Return")
        else:
            cur.execute("SELECT b.accessionNo, b.title, m.name, m.membershipID \
                FROM BorrowedBooks b1 JOIN Books b ON b1.borrowedBookID = b.accessionNo \
                    JOIN Members m ON b1.borrowedUserID = m.membershipID \
                        WHERE b1.borrowedBookID = %s AND b1.returnedDate IS NULL", BookID_field.get())
            results = cur.fetchone()
            if not results:
                self.createPopUp("red", "Error", "Borrowed book not found", "Loan")
            else:
                results = list(results)
                cur.execute("\
                    SELECT TIMESTAMPDIFF(DAY, dueDate, STR_TO_DATE(%s, %s)) FROM BorrowedBooks \
                    WHERE borrowedBookID = %s AND returnedDate IS NULL\
                    ",(date_field.get(), "%d/%m/%Y", BookID_field.get()))
                fine = cur.fetchone()[0]
                if not fine:
                    self.createPopUp("red", "Error", "Invalid Date Format", "Return")
                else:
                    fine = 0 if fine <= 0 else fine
                    results.append(fine)
                    results.insert(len(results) - 1, date_field.get())
                    labels = ["Accession Number", "Book Title", "Membership ID", "Membership Name", "Return Date", "Fine($)"]
                    self.createPopUp2("Please Comfirm Details\n To Be Correct", dict(zip(labels, results)), "Return", lambda: execute(BookID_field.get(), date_field.get(), results[3], fine))