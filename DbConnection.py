import psycopg2

# Veritabanı bağlantısını yapar
def connect_to_database():
    try:
        # Veritabanı bağlantısını yap
        connection = psycopg2.connect(
            dbname="tempDB",
            user="postgres",
            password="123",
            host="localhost",
            port="5432"
        )
        print("Veritabanına başarıyla bağlandı.")
        return connection
    except psycopg2.Error as e:
        print("Veritabanına bağlanırken bir hata oluştu:", e)
        return None
