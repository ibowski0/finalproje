import pyodbc

#DESKTOP-ETBJ7UV\SQLEXPRESS

# Veri tabanı bağlantı parametrelerini ayarla
server = 'bozkurt\\SQLEXPRESS'
database = 'YBS'

# Bağlantı dizesini oluştur
connection_string = f"""
DRIVER={{SQL Server}};
SERVER={server};
DATABASE={database};
Trusted_Connection=yes;
"""

# Bağlantıyı kur
try:
    connection = pyodbc.connect(connection_string)
    print("Bağlantı başarılı!")
except pyodbc.Error as err:
    print("Bağlantı hatası: ", err)

# Bağlantıyı kapat
connection.close()
