from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from Membership import *
from Books import *
from Reports import *
from Fines import *
from Loans import *
from Reservations import *
from Template import *

class ALS(Template):
    def __init__(self, root=None):
        super().__init__(root)

        self.frame = Frame(self.root, bg = 'floral white')
        self.frame.pack(fill=BOTH, expand=True)
        headingLabel = Label(self.frame, text="ALS", bg = 'light blue', fg='black', font=('Courier', 50, 'bold'))
        headingLabel.place(relx=0.2,rely=0.1,relwidth=0.6,relheight=0.16)
        
        dummy_btn = Button(self.frame)
        dummy_btn.place(relx=0.1, rely=0.3, relwidth=0.2, relheight=0.3)
        self.images = self.load_image(dummy_btn)
        btn0 = Button(self.frame, text="Membership", image = self.images[5], compound= "center",
            highlightbackground='mint cream', fg = "black", font=('Courier', 20, 'bold'), command= lambda: self.switch_class(Membership))
        btn0.place(relx=0.1, rely=0.3, relwidth=0.2, relheight=0.3)
        btn1 = Button(self.frame, text="Books", image = self.images[4], compound= "center",
            highlightbackground='mint cream', fg = "black", font=('Courier', 20, 'bold'), command=lambda: self.switch_class(Books))
        btn1.place(relx=0.4, rely=0.3, relwidth=0.2, relheight=0.3)
        btn2 = Button(self.frame, text="Loans", image = self.images[0], compound= "center",
            highlightbackground='mint cream', fg = "black", font=('Courier', 20, 'bold'), command=lambda: self.switch_class(Loans))
        btn2.place(relx=0.7, rely=0.3, relwidth=0.2, relheight=0.3)
        btn3 = Button(self.frame, text="Reservations", image = self.images[2],compound= "center",
            highlightbackground='mint cream', fg = "black", font=('Courier', 20, 'bold'), command=lambda: self.switch_class(Reservations))
        btn3.place(relx=0.1, rely=0.65, relwidth=0.2, relheight=0.3)
        btn4 = Button(self.frame, text="Fines", image = self.images[1], compound = "center",
            highlightbackground='mint cream', fg = "black", font=('Courier', 20, 'bold'), command=lambda: self.switch_class(Fines))
        btn4.place(relx=0.4, rely=0.65, relwidth=0.2, relheight=0.3)
        btn5 = Button(self.frame , text="Reports", image = self.images[3], compound = "center",
            highlightbackground='mint cream', fg = "black", font=('Courier', 20, 'bold'), command=lambda: self.switch_class(Reports))
        btn5.place(relx=0.7, rely=0.65, relwidth=0.2, relheight=0.3)

if __name__ == '__main__':
    root = Tk()
    app = ALS(root)
    root.mainloop()