import tkinter as tk
from tkinter import ttk
import pyodbc
from tkinter import messagebox

# Veri tabanı bağlantı parametrelerini ayarla
server = 'bozkurt\\SQLEXPRESS'
database = 'YBS'

# Bağlantı dizesini oluştur
connection_string = f""" DRIVER={{SQL Server}}; SERVER={server}; DATABASE={database}; Trusted_Connection=yes; """

# Öğrencileri listeleme işlevi
def fetch_data():
    try:
        connection = pyodbc.connect(connection_string)
        cursor = connection.cursor()
        cursor.execute("{CALL sp_Ogrenci_Getir}")
        rows = cursor.fetchall()
        columns = [column[0] for column in cursor.description]
        data = [list(row) for row in rows]
        connection.close()
        return data, columns
    except pyodbc.Error as err:
        print("Bağlantı hatası: ", err)
        return [], []

def populate_treeview(tree, data, columns):
    tree.delete(*tree.get_children())
    tree["columns"] = columns
    for column in columns:
        tree.column(column, width=100, minwidth=100)
        tree.heading(column, text=column)
    for row in data:
        tree.insert("", "end", values=row)

def refresh_treeview():
    data, columns = fetch_data()
    populate_treeview(tree, data, columns)

def delete_student():
    selected_item = tree.selection()[0]
    values = tree.item(selected_item, 'values')
    student_id = values[0]

    try:
        connection = pyodbc.connect(connection_string)
        cursor = connection.cursor()
        cursor.execute("DELETE FROM Ogrenciler WHERE ogrenci_no = ?", student_id)
        connection.commit()
        connection.close()
        tree.delete(selected_item)
        messagebox.showinfo("Başarılı", "Öğrenci başarıyla silindi.")
    except pyodbc.Error as err:
        print("Bağlantı hatası: ", err)
        messagebox.showerror("Hata", "Öğrenci silinirken bir hata oluştu.")

def fetch_bolumler():
    try:
        connection = pyodbc.connect(connection_string)
        cursor = connection.cursor()
        cursor.execute("SELECT bolum_isim FROM Bolumler")
        bolumler = [row[0] for row in cursor.fetchall()]
        connection.close()
        return bolumler
    except pyodbc.Error as err:
        print("Bağlantı hatası: ", err)
        return []

def fetch_siniflar():
    try:
        connection = pyodbc.connect(connection_string)
        cursor = connection.cursor()
        cursor.execute("SELECT sinif_isim FROM Siniflar")
        siniflar = [row[0] for row in cursor.fetchall()]
        connection.close()
        return siniflar
    except pyodbc.Error as err:
        print("Bağlantı hatası: ", err)
        return []

def fetch_akademik_yillar():
    try:
        connection = pyodbc.connect(connection_string)
        cursor = connection.cursor()
        cursor.execute("SELECT akademik_yil_isim FROM Akademik_yil")
        akademik_yillar = [row[0] for row in cursor.fetchall()]
        connection.close()
        return akademik_yillar
    except pyodbc.Error as err:
        print("Bağlantı hatası: ", err)
        return []

def add_student():
    try:
        ogrenci_no = int(ogrenci_no_entry.get())
    except ValueError:
        messagebox.showerror("Hata", "Öğrenci No geçerli bir tamsayı olmalıdır.")
        return

    ogrenci_isim = ogrenci_isim_entry.get()
    ogrenci_soyisim = ogrenci_soyisim_entry.get()
    bolum_id = bolum_combobox.current() + 1
    sinif_id = sinif_combobox.current()
    akademik_yil_id = akademik_yil_combobox.current() + 1

    try:
        connection = pyodbc.connect(connection_string)
        cursor = connection.cursor()
        cursor.execute("{CALL sp_Ogrenci_Ekle (?, ?, ?, ?, ?, ?)}",
                       (ogrenci_no, ogrenci_isim, ogrenci_soyisim, bolum_id, sinif_id, akademik_yil_id))
        connection.commit()
        connection.close()
        messagebox.showinfo("Başarılı", "Öğrenci başarıyla eklendi.")
    except pyodbc.Error as err:
        print("Bağlantı hatası: ", err)
        messagebox.showerror("Hata", "Öğrenci eklenirken bir hata oluştu.")

# Tkinter arayüzünü oluştur
root = tk.Tk()
root.title("Öğrenci Yönetim Sistemi")

notebook = ttk.Notebook(root)
notebook.pack(pady=10, expand=True)

# Öğrenci Listeleme Sekmesi
listele_frame = ttk.Frame(notebook, width=800, height=400)
listele_frame.pack(fill='both', expand=True)

tree = ttk.Treeview(listele_frame)
tree.pack(fill='both', expand=True)

delete_button = tk.Button(listele_frame, text="Sil", command=delete_student)
delete_button.pack(pady=10)

refresh_button = tk.Button(listele_frame, text="Listele", command=refresh_treeview)
refresh_button.pack(pady=10)

data, columns = fetch_data()
populate_treeview(tree, data, columns)

# Öğrenci Ekleme Sekmesi
ekle_frame = ttk.Frame(notebook, width=800, height=400)
ekle_frame.pack(fill='both', expand=True)

ogrenci_no_label = tk.Label(ekle_frame, text="Öğrenci No:")
ogrenci_no_label.grid(row=0, column=0, padx=10, pady=5)
ogrenci_no_entry = tk.Entry(ekle_frame)
ogrenci_no_entry.grid(row=0, column=1, padx=10, pady=5)

ogrenci_isim_label = tk.Label(ekle_frame, text="Öğrenci İsim:")
ogrenci_isim_label.grid(row=1, column=0, padx=10, pady=5)
ogrenci_isim_entry = tk.Entry(ekle_frame)
ogrenci_isim_entry.grid(row=1, column=1, padx=10, pady=5)

ogrenci_soyisim_label = tk.Label(ekle_frame, text="Öğrenci Soyisim:")
ogrenci_soyisim_label.grid(row=2, column=0, padx=10, pady=5)
ogrenci_soyisim_entry = tk.Entry(ekle_frame)
ogrenci_soyisim_entry.grid(row=2, column=1, padx=10, pady=5)

bolum_label = tk.Label(ekle_frame, text="Bölüm:")
bolum_label.grid(row=3, column=0, padx=10, pady=5)
bolum_combobox = ttk.Combobox(ekle_frame, width=27)
bolum_combobox.grid(row=3, column=1, padx=10, pady=5)
bolum_combobox['values'] = fetch_bolumler()

sinif_label = tk.Label(ekle_frame, text="Sınıf:")
sinif_label.grid(row=4, column=0, padx=10, pady=5)
sinif_combobox = ttk.Combobox(ekle_frame, width=27)
sinif_combobox.grid(row=4, column=1, padx=10, pady=5)
sinif_combobox['values'] = fetch_siniflar()

akademik_yil_label = tk.Label(ekle_frame, text="Akademik Yıl:")
akademik_yil_label.grid(row=5, column=0, padx=10, pady=5)
akademik_yil_combobox = ttk.Combobox(ekle_frame, width=27)
akademik_yil_combobox.grid(row=5, column=1, padx=10, pady=5)
akademik_yil_combobox['values'] = fetch_akademik_yillar()

ekle_button = tk.Button(ekle_frame, text="Ekle", command=add_student)
ekle_button.grid(row=6, column=0, columnspan=2, pady=10)

# Sekmeleri ekle
notebook.add(listele_frame, text='Öğrenci Listele ve Sil')
notebook.add(ekle_frame, text='Öğrenci Ekle')

# Tkinter mainloop
root.mainloop()
