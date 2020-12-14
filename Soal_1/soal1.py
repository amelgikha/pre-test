import datetime

nama = input("Masukkan Nama : ")
email = input("Masukkan Email : ")
bday = input("Masukkan tanggal lahir (DD-MM-YYYY) : ").split('-')

tahun = abs(int(bday[2]) - datetime.date.today().year)
bulan = abs(int(bday[1]) - datetime.date.today().month)

print(f"Nama Anda : {nama}")
print(f"Email Anda : {email}")
print(f"Usia Anda : {tahun}tahun {bulan}bulan")