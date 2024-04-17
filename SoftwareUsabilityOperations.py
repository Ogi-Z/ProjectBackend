import DbConnection as Db



# SoftwareUsability tablosuna veri ekleme fonksiyonu
def add_softwareUsability(user_id, SoftwareUsabilityID, SoftwareUsabilitySoftware, SoftwareUsabilityTopicName, SoftwareUsabilityText):
    conn = Db.connect_to_database()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Blog (UserID, BlogID, BlogCategory, BlogText) VALUES (?, ?, ?, ?, ?, ?, ?)", (user_id, SoftwareUsabilityID, SoftwareUsabilitySoftware, SoftwareUsabilityTopicName, SoftwareUsabilityText))
    conn.commit()
    conn.close()

# User tablosundan belirli bir BlogID'ye göre veri silme fonksiyonu
def delete_softwareUsability(blog_id):
    conn = Db.connect_to_database()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Blog WHERE BlogID=?", (blog_id,))
    conn.commit()
    conn.close()

# Belirli bir BlogID'ye göre User tablosundan veri sorgulama fonksiyonu
def query_softwareUsability(blog_id):
    conn = Db.connect_to_database()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Blog WHERE UserID=?", (blog_id,))
    softwareUsability_data = cursor.fetchone()
    conn.close()
    return softwareUsability_data
