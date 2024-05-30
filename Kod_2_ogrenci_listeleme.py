import tkinter as tk
from tkinter import ttk
import pyodbc

def fetch_data():
    try:
        # Veri tabanı bağlantı parametrelerini ayarla
        server = 'bozkurt\\SQLEXPRESS'
        database = 'YBS'

        # Bağlantı dizesini oluştur
        connection_string = f""" DRIVER={{SQL Server}}; SERVER={server}; DATABASE={database}; Trusted_Connection=yes; """

        # Bağlantıyı kur
        connection = pyodbc.connect(connection_string)
        cursor = connection.cursor()

        # Stored procedure'ü çağır ve sonuçları al
        cursor.execute("{CALL sp_Ogrenci_Getir}")
        rows = cursor.fetchall()

        # Tüm sütun adlarını bir listeye al
        columns = [column[0] for column in cursor.description]

        # Her satır için değerleri bir listeye al
        data = []
        for row in rows:
            values = []
            for i, column in enumerate(columns):  # Use enumerate to get both index (i) and column name
                values.append(row[i])  # Access element using index (i)
            data.append(values)

        # Bağlantıyı kapat
        connection.close()

        return data, columns
    except pyodbc.Error as err:
        print("Bağlantı hatası: ", err)
        return [], []

def populate_treeview(tree, data, columns):
    # Sütunları ekle
    tree["columns"] = columns
    for column in columns:
        tree.column(column, width=100, minwidth=100)
        tree.heading(column, text=column)

    # Satırları ekle
    for row in data:
        tree.insert("", "end", values=row)

# Tkinter arayüzünü oluştur
root = tk.Tk()
root.title("Veri Tabanı Görüntüleme")

frame = tk.Frame(root)
frame.pack(pady=20)

tree = ttk.Treeview(frame)
tree.pack()

# Verileri getir ve Treeview'i doldur
data, columns = fetch_data()
populate_treeview(tree, data, columns)

# Tkinter mainloop
root.mainloop()
