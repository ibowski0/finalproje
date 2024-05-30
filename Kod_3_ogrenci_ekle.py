import tkinter as tk
from tkinter import ttk
import pyodbc
from tkinter import messagebox

server = 'bozkurt\\SQLEXPRESS'
database = 'YBS'

# Bağlantı dizesini oluştur
connection_string = f""" DRIVER={{SQL Server}}; SERVER={server}; DATABASE={database}; Trusted_Connection=yes; """

def fetch_bolumler():
    try:
        # Bağlantıyı kur
        connection = pyodbc.connect(connection_string)
        cursor = connection.cursor()

        # Bolumler tablosundan bolum_isim sütunundaki verileri çek
        cursor.execute("SELECT bolum_isim FROM Bolumler")
        bolumler = [row[0] for row in cursor.fetchall()]

        # Bağlantıyı kapat
        connection.close()

        return bolumler
    except pyodbc.Error as err:
        print("Bağlantı hatası: ", err)
        return []

def fetch_siniflar():
    try:
        # Bağlantıyı kur
        connection = pyodbc.connect(connection_string)
        cursor = connection.cursor()

        # Siniflar tablosundan sinif_isim sütunundaki verileri çek
        cursor.execute("SELECT sinif_isim FROM Siniflar")
        siniflar = [row[0] for row in cursor.fetchall()]

        # Bağlantıyı kapat
        connection.close()

        return siniflar
    except pyodbc.Error as err:
        print("Bağlantı hatası: ", err)
        return []

def fetch_akademik_yillar():
    try:
        # Bağlantıyı kur
        connection = pyodbc.connect(connection_string)
        cursor = connection.cursor()

        # Akademik_yil tablosundan akademik_yil_isim sütunundaki verileri çek
        cursor.execute("SELECT akademik_yil_isim FROM Akademik_yil")
        akademik_yillar = [row[0] for row in cursor.fetchall()]

        # Bağlantıyı kapat
        connection.close()

        return akademik_yillar
    except pyodbc.Error as err:
        print("Bağlantı hatası: ", err)
        return []

def add_student():
    # Formdaki girdi değerlerini al
    ogrenci_no = ogrenci_no_entry.get()
    ogrenci_isim = ogrenci_isim_entry.get()
    ogrenci_soyisim = ogrenci_soyisim_entry.get()
    bolum_id = bolum_combobox.current()  + 1 # Seçilen bölümün indeksini al
    sinif_id = sinif_combobox.current()  # Seçilen sınıfın indeksini al
    akademik_yil_id = akademik_yil_combobox.current() + 1 # Seçilen akademik yılın indeksini al


    try:
        connection = pyodbc.connect(connection_string)
        cursor = connection.cursor()

        # Stored procedure'ü çağır
        cursor.execute("{CALL sp_Ogrenci_Ekle (?, ?, ?, ?, ?, ?)}",
                       (ogrenci_no, ogrenci_isim, ogrenci_soyisim, bolum_id, sinif_id, akademik_yil_id))

        # Değişiklikleri uygula ve bağlantıyı kapat
        connection.commit()
        connection.close()

        # Başarı mesajı göster
        
        messagebox.showinfo("Başarılı", "Öğrenci başarıyla eklendi.")
    except pyodbc.Error as err:
        print("Bağlantı hatası: ", err)
        messagebox.showerror("Hata", "Öğrenci eklenirken bir hata oluştu.")

# Tkinter arayüzünü oluştur
root = tk.Tk()
root.title("Öğrenci Veri Girişi")

frame = tk.Frame(root)
frame.pack(pady=20)

# Öğrenci No
ogrenci_no_label = tk.Label(frame, text="Öğrenci No:")
ogrenci_no_label.grid(row=0, column=0, padx=10, pady=5)
ogrenci_no_entry = tk.Entry(frame)
ogrenci_no_entry.grid(row=0, column=1, padx=10, pady=5)

# Öğrenci İsim
ogrenci_isim_label = tk.Label(frame, text="Öğrenci İsim:")
ogrenci_isim_label.grid(row=1, column=0, padx=10, pady=5)
ogrenci_isim_entry = tk.Entry(frame)
ogrenci_isim_entry.grid(row=1, column=1, padx=10, pady=5)

# Öğrenci Soyisim
ogrenci_soyisim_label = tk.Label(frame, text="Öğrenci Soyisim:")
ogrenci_soyisim_label.grid(row=2, column=0, padx=10, pady=5)
ogrenci_soyisim_entry = tk.Entry(frame)
ogrenci_soyisim_entry.grid(row=2, column=1, padx=10, pady=5)

# Bölüm
bolum_label = tk.Label(frame, text="Bölüm:")
bolum_label.grid(row=3, column=0, padx=10, pady=5)
bolum_combobox = ttk.Combobox(frame, width=27)
bolum_combobox.grid(row=3, column=1, padx=10, pady=5)
bolumler = fetch_bolumler()
bolum_combobox['values'] = bolumler
#bolum_combobox.current(0)  # İlk değeri seçili olarak ayarla

# Sınıf
sinif_label = tk.Label(frame, text="Sınıf:")
sinif_label.grid(row=4, column=0, padx=10, pady=5)
sinif_combobox = ttk.Combobox(frame, width=27)
sinif_combobox.grid(row=4, column=1, padx=10, pady=5)
sinifler = fetch_siniflar()
sinif_combobox['values'] = sinifler
#sinif_combobox.current(0)  # İlk değeri seçili olarak ayarla

# Akademik Yıl
akademik_yil_label = tk.Label(frame, text="Akademik Yıl:")
akademik_yil_label.grid(row=5, column=0, padx=10, pady=5)
akademik_yil_combobox = ttk.Combobox(frame, width=27)
akademik_yil_combobox.grid(row=5, column=1, padx=10, pady=5)
akademik_yillar = fetch_akademik_yillar()
akademik_yil_combobox['values'] = akademik_yillar
#akademik_yil_combobox.current(0)  # İlk değeri seçili olarak ayarla

# Ekle Butonu
ekle_btn = tk.Button(frame, text="Ekle", command=add_student)
ekle_btn.grid(row=6, column=0, columnspan=2, pady=10)

# Tkinter mainloop
root.mainloop()
