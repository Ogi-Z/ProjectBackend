import DbConnection as Db

# User tablosuna veri ekleme fonksiyonu
def add_user(user_id, username, usersurname, useremail, userpassword, usercity, role_id):
    conn = Db.connect_to_database()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO User (UserID, UserName, UserSurname, UserEmail, UserPassword, UserCity, RoleID) VALUES (?, ?, ?, ?, ?, ?, ?)", (user_id, username, usersurname, useremail, userpassword, usercity, role_id))
    conn.commit()
    conn.close()

# User tablosundan belirli bir UserID'ye göre veri silme fonksiyonu
def delete_user(user_id):
    conn = Db.connect_to_database()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM User WHERE UserID=?", (user_id,))
    conn.commit()
    conn.close()

# Belirli bir UserID'ye göre User tablosundan veri sorgulama fonksiyonu
def query_user(user_id):
    conn = Db.connect_to_database()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM User WHERE UserID=?", (user_id,))
    user_data = cursor.fetchone()
    conn.close()
    return user_data

