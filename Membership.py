from multiprocessing import dummy
from tkinter import *
from tkinter import ttk
from Template import *
from ALS import *
import pymysql


class Membership(Template):

    def __init__(self, root = None, app = None):
        super().__init__(root)
        self.app = app
        global con
        global cur
        con, cur = self.connect_database()

        self.frame = Frame(self.root, bg = 'floral white')
        self.frame.pack(fill=BOTH, expand=True)
    
        headingLabel = Label(self.frame, text="Select one of the options below:", bg='light blue', fg='black', font=('Courier', 20, 'bold'))
        headingLabel.place(relx=0.1,rely=0.1,relwidth=0.8,relheight=0.1)

        dummy_label = Label(self.frame)
        dummy_label.place(relx=0.1,rely=0.3,relwidth=0.28,relheight=0.5)
        self.images = self.load_image(dummy_label)
        image_label= Label(self.frame, image = self.images[5], compound="center")
        image_label.place(relx=0.1,rely=0.3,relwidth=0.28,relheight=0.5)

        create_btn = Button(self.frame, text="Create", highlightbackground='mint cream', fg = "black", font=('Courier', 15, 'bold'), command=lambda: self.switch_frame(self.create_frame()))
        create_btn.place(relx=0.4, rely=0.23, relwidth=0.2, relheight=0.2)
        Label(self.frame, text = "Membership Creation", font="Verdana 15").place(relx=0.6, rely=0.28, relwidth=0.3, relheight=0.1)
        delete_btn = Button(self.frame, text="Delete", highlightbackground='mint cream', fg = "black", font=('Courier', 15, 'bold'), command=lambda: self.switch_frame(self.delete_frame()))
        delete_btn.place(relx=0.4, rely=0.45, relwidth=0.2, relheight=0.2)
        Label(self.frame, text = "Membership Deletion", font="Verdana 15").place(relx=0.6, rely=0.50, relwidth=0.3, relheight=0.1)
        update_btn = Button(self.frame, text="Update", highlightbackground='mint cream', fg = "black", font=('Courier', 15, 'bold'), command=lambda: self.switch_frame(self.update_frame()))
        update_btn.place(relx=0.4, rely=0.67, relwidth=0.2, relheight=0.2)
        Label(self.frame, text = "Membership Update", font="Verdana 15").place(relx=0.6, rely=0.72, relwidth=0.3, relheight=0.1)

        menu_btn = Button(self.frame, text="Back To Main Menu", highlightbackground='blue', fg = "black", font=('Courier', 15, 'bold'), command=lambda: self.go_to_main())
        menu_btn.place(relx=0.1, rely=0.9, relwidth=0.8, relheight=0.06)

    def submit(self, fields):
        ID_field, name_field, faculty_field, phone_field, email_field = fields
        if not (ID_field.get() and name_field.get() and faculty_field.get() and phone_field.get() and email_field.get()):
            self.createPopUp("red", "Error", "Member already exist; Missing\n or Incomplete fields", "Create")
        else:
            cur.execute("SELECT * FROM Members WHERE membershipID = %s", ID_field.get())
            result = cur.fetchone()        
            if not result:
                cur.execute("INSERT INTO Members VALUES(%s, %s, %s, %s, %s, DEFAULT, DEFAULT)",
                    (ID_field.get(), name_field.get(), faculty_field.get(), phone_field.get(), email_field.get()))
                con.commit()
                self.createPopUp("green", "Success!", "ALS Membership \nCreated", "Create")
            else:
                self.createPopUp("red", "Error", "Member already exist; Missing\n or Incomplete fields", "Create")    

    def delete(self, ID_field):

        def execute(id):
            cur.execute("DELETE FROM Members WHERE membershipID = %s", id)
            con.commit()

        id = ID_field.get()
        if not id:
            self.createPopUp("red", "Error", "Please enter \nmembership ID", "Delete")
        else:
            cur.execute("SELECT * FROM Members WHERE membershipID = %s", id)
            fields = cur.fetchone()
            con.commit()
            if not fields:
                self.createPopUp("red", "Error", "Member does not exist", "Delete")
            else:
                cur.execute("SELECT membershipID, name, faculty, phoneNo, email FROM Members \
                    WHERE membershipID NOT IN(SELECT borrowedUserID FROM BorrowedBooks WHERE returnedDate IS NULL)\
                        AND membershipID NOT IN(SELECT reservedUserID FROM ReservedBooks) \
                            AND membershipID = %s AND fineAmt = 0", id)
                result = cur.fetchone()
                con.commit()
                if not result:
                    self.createPopUp("red", "Error", "Member has loans, \nreservations or \noutstanding fines", "Delete")
                else:
                    labels = ("Member ID", "Name", "Faculty", "Phone Number", "Email Address")
                    self.createPopUp2("Please Comfirm Details\n To Be Correct", dict(zip(labels, result)), "Delete", lambda: execute(id))

    def update(self, id, fields):

        def execute(values):
            id, name, faculty, phone, email = values
            cur.execute("UPDATE Members SET name = %s, faculty = %s, phoneNo = %s, email = %s WHERE membershipID = %s", (name, faculty, phone, email, id))
            con.commit()

        name_field, faculty_field, phone_field, email_field = fields
        cur.execute("SELECT * FROM Members WHERE membershipID = %s", id)
        result = cur.fetchone()
        con.commit()
        if not result:
            self.createPopUp("red", "Error", "Member does not exist", "Delete")
        elif not (name_field.get() and faculty_field.get() and phone_field.get() and email_field.get()):
            self.createPopUp("red", "Error", "Missing\n or Incomplete fields", "Update")
        else:
            labels = ("Member ID", "Name", "Faculty", "Phone Number", "Email Address")
            values = (id, name_field.get(), faculty_field.get(), phone_field.get(), email_field.get())
            self.createPopUp2("Please Comfirm Details\n To Be Correct", dict(zip(labels, values)), "Update", lambda: execute(values))
   
    def create_frame(self):
        frame = Frame(self.root, bg = 'floral white')

        headingLabel = Label(frame, text="To Create Member, Please Enter Requested Information Below:", bg='light blue', fg='black', font=('Courier', 15, 'bold'))
        headingLabel.place(relx=0.1,rely=0.11,relwidth=0.8,relheight=0.1)

        Label(frame, text = "Membership ID", bg='light blue', fg='black', font=('Courier', 15, 'bold')).place(relx=0.1,rely=0.26,relwidth=0.2,relheight=0.1)
        ID_field = ttk.Entry(frame, width= 30)
        ID_field.place(relx=0.3,rely=0.26,relwidth=0.6,relheight=0.1)

        Label(frame, text = "Name", bg='light blue', fg='black', font=('Courier', 15, 'bold')).place(relx=0.1,rely=0.37,relwidth=0.2,relheight=0.1)
        name_field = ttk.Entry(frame, width= 30)
        name_field.place(relx=0.3,rely=0.37,relwidth=0.6,relheight=0.1)

        Label(frame, text = "Faculty", bg='light blue', fg='black', font=('Courier', 15, 'bold')).place(relx=0.1,rely=0.48,relwidth=0.2,relheight=0.1)
        faculty_field = ttk.Entry(frame, width= 30)
        faculty_field.place(relx=0.3,rely=0.48,relwidth=0.6,relheight=0.1)

        Label(frame, text = "Phone Number", bg='light blue', fg='black', font=('Courier', 15, 'bold')).place(relx=0.1,rely=0.59,relwidth=0.2,relheight=0.1)
        phone_field = ttk.Entry(frame, width= 30)
        phone_field.place(relx=0.3,rely=0.59,relwidth=0.6,relheight=0.1)

        Label(frame, text = "Email Address", bg='light blue', fg='black', font=('Courier', 15, 'bold')).place(relx=0.1,rely=0.7,relwidth=0.2,relheight=0.1)
        email_field = ttk.Entry(frame, width= 30)
        email_field.place(relx=0.3,rely=0.7,relwidth=0.6,relheight=0.1)

        fields = [ID_field, name_field, faculty_field, phone_field, email_field]

        create_btn = Button(frame, text = "Create Member", highlightbackground='blue', fg = "black", font=('Courier', 15, 'bold'), command=lambda: self.submit(fields))
        create_btn.place(relx=0.15, rely=0.85, relwidth=0.3, relheight=0.1)

        menu_btn = Button(frame, text="Back To Membership Menu", highlightbackground='blue', fg = "black", font=('Courier', 15, 'bold'), command=lambda: self.reset())
        menu_btn.place(relx=0.55, rely=0.85, relwidth=0.3, relheight=0.1)
        return frame

    def delete_frame(self):
        frame = Frame(self.root, bg = 'floral white')

        headingLabel = Label(frame, text="To Delete Member, Please Enter Membership ID:", bg='light blue', fg='black', font=('Courier', 15, 'bold'))
        headingLabel.place(relx=0.1,rely=0.11,relwidth=0.8,relheight=0.1)

        Label(frame, text = "Membership ID", bg='light blue', fg='black', font=('Courier', 15, 'bold')).place(relx=0.1,rely=0.45,relwidth=0.2,relheight=0.1)
        ID_field = ttk.Entry(frame, width= 30)
        ID_field.place(relx=0.3,rely=0.45,relwidth=0.6,relheight=0.1)

        delete_btn = Button(frame, text = "Delete Member", highlightbackground='blue', fg = "black", font=('Courier', 15, 'bold'), command=lambda: self.delete(ID_field))
        delete_btn.place(relx=0.15, rely=0.85, relwidth=0.3, relheight=0.1)

        menu_btn = Button(frame, text="Back To Membership Menu", highlightbackground='blue', fg = "black", font=('Courier', 15, 'bold'), command=lambda: self.reset())
        menu_btn.place(relx=0.55, rely=0.85, relwidth=0.3, relheight=0.1)
        return frame

    def update_frame(self):
        frame = Frame(self.root, bg = 'floral white')

        headingLabel = Label(frame, text="To Update Member, Please Enter Membership ID:", bg='light blue', fg='black', font=('Courier', 15, 'bold'))
        headingLabel.place(relx=0.1,rely=0.11,relwidth=0.8,relheight=0.1)

        Label(frame, text = "Membership ID", bg='light blue', fg='black', font=('Courier', 15, 'bold')).place(relx=0.1,rely=0.45,relwidth=0.2,relheight=0.1)
        ID_field = ttk.Entry(frame, width= 30)
        ID_field.place(relx=0.3,rely=0.45,relwidth=0.6,relheight=0.1)

        delete_btn = Button(frame, text = "Update Member", highlightbackground='blue', fg = "black", font=('Courier', 15, 'bold'), 
            command=lambda: self.switch_frame(self.update_second_frame(ID_field.get())))
        delete_btn.place(relx=0.15, rely=0.85, relwidth=0.3, relheight=0.1)

        menu_btn = Button(frame, text="Back To Membership Menu", highlightbackground='blue', fg = "black", font=('Courier', 15, 'bold'), command=lambda: self.reset())
        menu_btn.place(relx=0.55, rely=0.85, relwidth=0.3, relheight=0.1)
        return frame

    def update_second_frame(self, id):
        frame = Frame(self.root, bg = 'floral white')

        headingLabel = Label(frame, text="To Create Member, Please Enter Requested Information Below:", bg='light blue', fg='black', font=('Courier', 15, 'bold'))
        headingLabel.place(relx=0.1,rely=0.11,relwidth=0.8,relheight=0.1)

        Label(frame, text = "Membership ID", bg='light blue', fg='black', font=('Courier', 15, 'bold')).place(relx=0.1,rely=0.26,relwidth=0.2,relheight=0.1)
        ID_field = Label(frame, text = f"{id}", width= 30)
        ID_field.place(relx=0.3,rely=0.26,relwidth=0.6,relheight=0.1)

        Label(frame, text = "Name", bg='light blue', fg='black', font=('Courier', 15, 'bold')).place(relx=0.1,rely=0.37,relwidth=0.2,relheight=0.1)
        name_field = ttk.Entry(frame, width= 30)
        name_field.place(relx=0.3,rely=0.37,relwidth=0.6,relheight=0.1)

        Label(frame, text = "Faculty", bg='light blue', fg='black', font=('Courier', 15, 'bold')).place(relx=0.1,rely=0.48,relwidth=0.2,relheight=0.1)
        faculty_field = ttk.Entry(frame, width= 30)
        faculty_field.place(relx=0.3,rely=0.48,relwidth=0.6,relheight=0.1)

        Label(frame, text = "Phone Number", bg='light blue', fg='black', font=('Courier', 15, 'bold')).place(relx=0.1,rely=0.59,relwidth=0.2,relheight=0.1)
        phone_field = ttk.Entry(frame, width= 30)
        phone_field.place(relx=0.3,rely=0.59,relwidth=0.6,relheight=0.1)

        Label(frame, text = "Email Address", bg='light blue', fg='black', font=('Courier', 15, 'bold')).place(relx=0.1,rely=0.7,relwidth=0.2,relheight=0.1)
        email_field = ttk.Entry(frame, width= 30)
        email_field.place(relx=0.3,rely=0.7,relwidth=0.6,relheight=0.1)

        fields = [name_field, faculty_field, phone_field, email_field]

        create_btn = Button(frame, text = "Update Member", highlightbackground='blue', fg = "black", font=('Courier', 15, 'bold'), command=lambda: self.update(id, fields))
        create_btn.place(relx=0.15, rely=0.85, relwidth=0.3, relheight=0.1)

        menu_btn = Button(frame, text="Back To Update Menu", highlightbackground='blue', fg = "black", font=('Courier', 15, 'bold'), command=lambda: self.switch_frame(self.update_frame()))
        menu_btn.place(relx=0.55, rely=0.85, relwidth=0.3, relheight=0.1)
        return frame

