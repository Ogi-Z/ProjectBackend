import DbConnection as Db



# SoftwareUsability tablosuna veri ekleme fonksiyonu
def add_softwareUsability(user_id, SoftwareUsabilityID, SoftwareUsabilitySoftware, SoftwareUsabilityTopicName, SoftwareUsabilityText):
    conn = Db.connect_to_database()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Blog (UserID, SoftwareUsabilityID, SoftwareUsabilitySoftware, SoftwareUsabilityTopicName, SoftwareUsabilityText) VALUES (?, ?, ?, ?, ?, ?, ?)", (user_id, SoftwareUsabilityID, SoftwareUsabilitySoftware, SoftwareUsabilityTopicName, SoftwareUsabilityText))
    conn.commit()
    conn.close()

# User tablosundan belirli bir BlogID'ye göre veri silme fonksiyonu
def delete_softwareUsability():
    conn = Db.connect_to_database()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Blog WHERE SoftwareUsabilityID=?", (SoftwareUsabilityID))
    conn.commit()
    conn.close()

# Belirli bir BlogID'ye göre User tablosundan veri sorgulama fonksiyonu
def query_softwareUsability():
    conn = Db.connect_to_database()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM SoftwareUsability")
    softwareUsability_data = cursor.fetchone()
    conn.close()
    return softwareUsability_data
