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

def delete_student():
    selected_item = tree.selection()[0]  # Seçili öğeyi al
    values = tree.item(selected_item, 'values')
    student_id = values[0]  # Öğrencinin ID'si (varsayılan olarak ilk sütunda)

    try:
        # Veri tabanı bağlantı parametrelerini ayarla
        server = ''
        database = 'YBS'

        # Bağlantı dizesini oluştur
        connection_string = f""" DRIVER={{SQL Server}}; SERVER={server}; DATABASE={database}; Trusted_Connection=yes; """

        # Bağlantıyı kur
        connection = pyodbc.connect(connection_string)
        cursor = connection.cursor()

        # Öğrenciyi silen SQL sorgusunu çalıştır
        cursor.execute("DELETE FROM Ogrenciler WHERE ogrenci_id = ?", student_id)
        connection.commit()

        # Bağlantıyı kapat
        connection.close()

        # Treeview'den öğeyi sil
        tree.delete(selected_item)

    except pyodbc.Error as err:
        print("Bağlantı hatası: ", err)

# Tkinter arayüzünü oluştur
root = tk.Tk()
root.title("Veri Tabanı Görüntüleme")

frame = tk.Frame(root)
frame.pack(pady=20)

tree = ttk.Treeview(frame)
tree.pack()

# Sil butonunu oluştur ve ekle
delete_button = tk.Button(root, text="Sil", command=delete_student)
delete_button.pack(pady=10)

# Verileri getir ve Treeview'i doldur
data, columns = fetch_data()
populate_treeview(tree, data, columns)

# Tkinter mainloop
root.mainloop()
