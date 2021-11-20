import gspread
import time
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint
import sqlite3
scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

creds = ServiceAccountCredentials.from_json_keyfile_name(
    "C:\example\AI\AI.json")
client = gspread.authorize(creds)
sheet = client.open("AI").sheet1
data = sheet.get_all_records()
print(data)
pprint(data)


def sheets():
    conn = sqlite3.connect('C:\example\AI\AI_secA.db')
    c = conn.cursor()
    val = c.execute("SELECT * from AIsecA")
    cont = val.fetchall
    row = 2
    c.execute("PRAGMA table_info(AIsecA)")
    head = c.fetchall()
    header = []

    for i in head:
        header.append(i[1])
        print(header)
    sheet.resize(rows=1)
    sheet.resize(rows=100)
    sheet.delete_row(1)
    sheet.insert_row(header, 1)
    for tuple in c.execute('SELECT * FROM AIsecA'):
        sheet.insert_row(tuple, row)
        row = row+1
        print("\n")
        print(tuple)
        time.sleep(1.5)
