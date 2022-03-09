import os
from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
import pymysql
class Template():

    def __init__(self, root=None):
        self.root = root
        self.root.title("ALS")
        self.root.minsize(width=700,height=700)
        width, height = root.winfo_screenwidth(), root.winfo_screenheight()
        self.root.geometry(f"{width}x{height}")

    def start_page(self):
        self.__init__(self.root)
    
    def reset(self):
        self.frame.destroy()
        self.__init__(self.root, self.app)

    def go_to_main(self):
        self.frame.destroy()
        self.app.start_page()

    def switch_class(self, new_class):
        self.frame.destroy()
        self.frame = new_class(self.root, self)

    def switch_frame(self, frame):
        self.frame.destroy()
        self.frame = frame
        self.frame.pack(fill=BOTH, expand=True)

    def load_image(self, widget):
        path = os.getcwd() + "/images/"
        widget.update()
        images = []
        for file in os.listdir(path):
            if file.endswith("jpg"):
                image = Image.open(os.path.join(path, file))
                image = image.resize((widget.winfo_width(), widget.winfo_height()), Image.ANTIALIAS)
                image = ImageTk.PhotoImage(image)
                images.append(image)
        return images

    def create_frame(self, action):
        pass
    
    def createPopUp(self, color, message, description, name):
        pop = Toplevel(self.root)
        height, width = self.root.winfo_height(), self.root.winfo_width()
        pop.geometry(f"500x450+{int((width - 500)/2)}+{int((height - 450)/2)}")
        pop.config(bg = color)
        Label(pop, text = message, bg=color, font=('Courier', 40, 'bold')).pack()
        Label(pop, text = description, bg=color, font=('Courier', 25)).pack(anchor="center")
        Button(pop, text = f"Back to\n{name} Function", highlightbackground='mint cream', command = lambda: pop.destroy()).place(relx=0.3, rely=0.6, relwidth=0.4, relheight=0.3)

    def createPopUp2(self, message, dict, name, function):
        def func(function):
            function()
            pop.destroy()
        pop = Toplevel(self.root)
        height, width = self.root.winfo_height(), self.root.winfo_width()
        pop.geometry(f"500x450+{int((width - 500)/2)}+{int((height - 450)/2)}")
        pop.config(bg = "green")
        Label(pop, text = message, bg="green", font=('Courier', 35, 'bold')).pack()
        i = 0
        for k, v in dict.items():
            Label(pop, text = f"{k} : {v}", bg="green", font="Verdana 15 underline").place(relx = 0.15, rely = 0.25 + i)
            i+=0.05
        Button(pop, text = f"Confirm {name}", highlightbackground='mint cream', command = lambda: func(function)).place(relx=0.15, rely=0.6, relwidth=0.3, relheight=0.3)
        Button(pop, text = f"Back to\n{name} Function", highlightbackground='mint cream', command = lambda: pop.destroy()).place(relx=0.55, rely=0.6, relwidth=0.3, relheight=0.3)

    def report_type(self, height, headings, widths):
        pop = Toplevel(self.root)
        columns = ()
        for i in range(len(widths)):
            columns += (i+1,)
        trv = ttk.Treeview(pop, columns=columns, show="headings", height=f"{height}")
        trv.pack()
        for i in range(len(widths)):
            trv.heading(i+1, text = headings[i])
            trv.column(i+1, width = widths[i])
        return trv

    def switch_popups(self,popup1,popup2):
        popup1.destroy()
        popup2()

    def connect_database(self):
        pw = "BT2102group26"
        db = "ALS"
        con = pymysql.connect(host="localhost",user="root",password=pw,database=db) 
        cur = con.cursor()
        return (con, cur)