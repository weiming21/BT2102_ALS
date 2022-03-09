from tkinter import *
from tkinter import ttk
from Template import *


class Fines(Template):
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
        image_label= Label(self.frame, image = self.images[1], compound="center")
        image_label.place(relx=0.1,rely=0.3,relwidth=0.28,relheight=0.5)

        payment_btn = Button(self.frame, text="Payment", highlightbackground='mint cream', fg = "black", font=('Courier', 15, 'bold'), command=lambda: self.switch_frame(self.payment_page()))
        payment_btn.place(relx=0.4, rely=0.45, relwidth=0.2, relheight=0.2)
        Label(self.frame, text = "Fine Payment", font="Verdana 15").place(relx=0.6, rely=0.5, relwidth=0.3, relheight=0.1)

        menu_btn = Button(self.frame, text="Back To Main Menu", highlightbackground='blue', fg = "black", font=('Courier', 15, 'bold'), command=lambda: self.go_to_main())
        menu_btn.place(relx=0.1, rely=0.9, relwidth=0.8, relheight=0.06)

    def payment_page(self):
        frame = Frame(self.root, bg = 'floral white')

        headingLabel = Label(frame, text="To Pay a Fine, Please Enter Information Below:", bg='light blue', fg='black', font=('Courier', 15, 'bold'))
        headingLabel.place(relx=0.1,rely=0.11,relwidth=0.8,relheight=0.1)

        Label(frame, text = "Membership ID", bg='light blue', fg='black', font=('Courier', 15, 'bold')).place(relx=0.1,rely=0.3,relwidth=0.2,relheight=0.1)
        ID_field = ttk.Entry(frame, width= 30)
        ID_field.place(relx=0.3,rely=0.3,relwidth=0.6,relheight=0.1)

        Label(frame, text = "Payment Date (DD/MM/YYYY)", bg='light blue', fg='black', font=('Courier', 15, 'bold')).place(relx=0.1,rely=0.41,relwidth=0.2,relheight=0.1)
        date_field = ttk.Entry(frame, width= 30)
        date_field.place(relx=0.3,rely=0.41,relwidth=0.6,relheight=0.1)

        Label(frame, text = "Payment Amount", bg='light blue', fg='black', font=('Courier', 15, 'bold')).place(relx=0.1,rely=0.52,relwidth=0.2,relheight=0.1)
        amount_field = ttk.Entry(frame, width= 30)
        amount_field.place(relx=0.3,rely=0.52,relwidth=0.6,relheight=0.1)

        fields = [ID_field, date_field, amount_field]

        delete_btn = Button(frame, text = "Pay Fine", highlightbackground='blue', fg = "black", font=('Courier', 15, 'bold'), command=lambda: self.pay(fields))
        delete_btn.place(relx=0.15, rely=0.85, relwidth=0.3, relheight=0.1)

        menu_btn = Button(frame, text="Back To Fines Menu", highlightbackground='blue', fg = "black", font=('Courier', 15, 'bold'), command=lambda: self.reset())
        menu_btn.place(relx=0.55, rely=0.85, relwidth=0.3, relheight=0.1)
        return frame

    def pay(self, fields):
        ID_field, date_field, amount_field = fields
        if not ID_field.get() or not date_field.get() or not amount_field.get():
            self.createPopUp("red", "Error", "Please enter \nrequired information", "Payment")
        else:
            cur.execute("SELECT fineAmt from Members WHERE membershipID = %s", ID_field.get())
            fine_amt = cur.fetchone()
            if not fine_amt:
                self.createPopUp("red", "Error", "Member does not exist", "Payment")
                return
            results = [ID_field.get(), date_field.get(), fine_amt[0]]
            labels = ["Member ID", "Payment Date", "Payment($) Due (Only exact fee accepted)"]
            self.createPopUp2("Please Confirm Details\n To Be Correct", dict(zip(labels, results)), "Payment", lambda: execute(ID_field.get(), date_field.get(), amount_field.get(), fine_amt[0]))

        def execute(member_id, date, payment_amt, fine_amt):
            if not fine_amt:
                self.createPopUp("red", "Error", "Member has no fine", "Payment")
            elif int(payment_amt) != fine_amt:
                self.createPopUp("red", "Error", "Incorrect fine payment amount", "Payment")
            else:
                try:
                    cur.execute("UPDATE Members SET fineAmt = 0, paymentDate = STR_TO_DATE(%s, %s) WHERE membershipID = %s", (date, "%d/%m/%Y", member_id))
                    con.commit()
                except:
                    self.createPopUp("red", "Error", "Invalid date format", "Payment")
        