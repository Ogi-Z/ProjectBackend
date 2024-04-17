import sqlite3
# Veritabanı dosyasının adı
db_file = "tempDB"

# Veritabanına bağlanma fonksiyonu
def connect_to_database():
    conn = sqlite3.connect(db_file)
    return conn
