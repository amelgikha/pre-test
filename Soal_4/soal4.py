import xlsxwriter
import datetime
import pandas as pd

workbook = xlsxwriter.Workbook("Rezky_Amelia.xlsx")
sheet = workbook.add_worksheet("Soal_Pretest")

nama_kolom = ['nama','email','usia']
for kolom,data in enumerate(nama_kolom):
    sheet.write(0, kolom, data)

workbook.close()

nama = input("Masukkan Nama : ")
email = input("Masukkan Email : ")
bday = input("Masukkan tanggal lahir (DD-MM-YYYY) : ").split('-')
usia = abs(int(bday[2]) - datetime.date.today().year)

xl = pd.read_excel("Rezky_Amelia.xlsx", index_col=0, header=0)
df = pd.DataFrame({'nama': [nama],
                    'email': [email],
                    'usia': [usia]}).set_index('nama')

xl = xl.append(df)
xl.to_excel("Rezky_Amelia.xlsx", sheet_name="Soal_Pretest") 