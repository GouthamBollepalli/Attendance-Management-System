from tkinter import filedialog
from numpy import record
import pandas as pd
import sqlite3
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from gs import sheets

class Root(Tk):
    def __init__(self):
        super(Root, self).__init__()
        self.title("Attendance management system.")
        self.minsize(640, 400)
        print("Check")
    #giving width and height of GUI and the title
        self.labelFrame = ttk.LabelFrame(
            self, text="Open a file to update the attendance.")
        self.labelFrame.grid(column=0, row=1, padx=320, pady=20)
        self.filename = ""
        self.button()
        self.date()
        self.button1()
        self.Course()
    
    def button(self):
        self.button = ttk.Button(
            self.labelFrame, text="Browse A File", command=self.fileDialog)
        self.button.grid(column=1, row=1)

    def fileDialog(self):
        self.filename = filedialog.askopenfile()
        print(self.filename.name)
        self.label = ttk.Label(self.labelFrame, text="")
        self.label.grid(column=1, row=1)
        self.label.configure(text=self.filename)

    def Course(self):
        self.course = ("Operating systems", "Artificial Inteligence")
        self.labelFrame2 = ttk.LabelFrame(self, text = "course")
        self.labelFrame2.grid(column=0, row=3)
        self.cb1 = ttk.Combobox(self.labelFrame2, values = self.course)
        self.cb1.grid(column=1, row=4)
        

    def date(self):
        self.s_date = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15,
                       16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31)
        self.s_month = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12)
        self.s_year = (2020, 2021, 2022, 2023, 2024,
                       2025, 2026, 2027, 2028, 2029, 2030)

        self.labelFrame3 = ttk.LabelFrame(self, text="Date")
        self.labelFrame3.grid(column=0, row=5)
        self.cb2 = ttk.Combobox(self.labelFrame3, values=self.s_date)
        self.cb2.grid(column=1, row=6)

        self.labelFrame3 = ttk.LabelFrame(self, text="Month")
        self.labelFrame3.grid(column=0, row=7)
        self.cb3 = ttk.Combobox(self.labelFrame3, values=self.s_date)
        self.cb3.grid(column=1, row=8)

        self.labelFrame3 = ttk.LabelFrame(self, text="Year")
        self.labelFrame3.grid(column=0, row=8)
        self.cb4 = ttk.Combobox(self.labelFrame3, values=self.s_year)
        self.cb4.grid(column=1, row=10)

    def button1(self):
        print("button1")
        self.labelFrame4 = ttk.LabelFrame(self, text="Update attendance")
        self.labelFrame4.grid(column=0, row=11)
        self.button_submit = ttk.Button(
            self.labelFrame4, text="Update attendance", command=self.check)
        self.button_submit.grid(column=1, row=12)
    #function check is used to take attendance date atuomatically by using command=self.check so that the file date and file location will be taken automatically
    def check(self):
        self.loc = self.filename.name
        self.course = self.cb1.get()
        self.sd = self.cb2.get()
        self.sm = self.cb3.get()
        self.sy = self.cb4.get()
        print(self.loc)

        date = "d" + self.sd + self.sm + self.sy

        df = pd.read_excel(self.loc)
        df["Reg. No"] = df["Reg. No"].str.upper()
        list1 = []
        list1 = (df.iloc[0:, 3])

        print(list1)
        # list5 = number of students attended the class
        list5 = []
        for i in list1:
            list5.append(str(i).strip())
        print("\n list5 \n")
        print(list5)

        # connecting to the database
        conn = sqlite3.connect(':memory:')
        conn = sqlite3.connect('C:\example\Code\Students.db')
        c = conn.cursor()

        #date = input("date:")
        #date = dat
        c.execute("alter table code add column '%s' 'integer' DEFAULT '1'" % date)
        for row in c.execute("PRAGMA table_info('code')").fetchall():
            print(row)

        list2 = []
        c.execute(" SELECT Enroll from code ")
        list2 = c.fetchall()
        list3 = [i[0] for i in list2]
        # list4 = total number of students in database
        list4 = []
        for i in list3:
            list4.append(i.strip())
        print("\n\n Enroll No")
        print(list4)
        print(type(list1[1]))
        print(type(list4[1]))
        abs = []
        for i in list4:
            if i not in list5:
                abs.append(i)
        print("\nabsenties list: \n")
        print(abs)
        
        val = 0
        Eroll = '19STUCHH010134'
        att = 0
        cond = 0
        per = 0.0
        for i in abs:
            print(type(i))
            Eroll = str(i)
            sql_update_query = """Update code set %s = ? where Enroll = ?""" % date
            data = (val, Eroll)
            c.execute(sql_update_query, data)

        # for loop for number of classes conducted
        for i in list4:
            Eroll = str(i)
            sql_select_query = """SELECT Conducted FROM code WHERE Enroll = ?"""
            data = (Eroll)
            print(data)
            c.execute(sql_select_query, (Eroll,))
            record = c.fetchall()
            for j in record:
                cond = j[0]
                cond = cond+1
                sql_update_query = """UPDATE code SET Conducted = ? WHERE Enroll = ?"""
                data = (cond, Eroll)
                c.execute(sql_update_query, data)

            # for loop for number of classes attended
        for i in list5:
            Eroll = str(i)
            sql_select_query = """SELECT Attended FROM code WHERE Enroll = ?"""
            data = (Eroll)
            print(data)
            c.execute(sql_select_query, (Eroll,))
            record = c.fetchall()
            for j in record:
                att = j[0]
                att = att+1
                sql_Update_query = """UPDATE code SET Attended = ? WHERE Enroll = ?"""
                data = (att, Eroll)
                c.execute(sql_Update_query, data)

        # for loop for caluculating the percentage
        for i in list4:
            Eroll = str(i)
            sql_select_query = """SELECT Conducted, Attended FROM code WHERE Enroll = ?"""
            data = (Eroll)
            c.execute(sql_select_query, (Eroll,))
            record = c.fetchall()
            for j in record:
                cond = j[0]
                att = j[1]
                if (cond != 0):
                    per = (att/cond)*100
                    sql_update_query = """UPDATE code SET Percentage = ? WHERE Enroll = ?"""
                    data = (per, Eroll)
                    c.execute(sql_update_query, data)
        conn.commit()
        c.close()
        print(sql_update_query)
        print("command runned sucessfully...")
        exec = sheets()


if __name__ == "__main__":
    print("in side main")
    root = Root()
    root.mainloop()
