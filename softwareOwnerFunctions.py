import DbConnection as Db
import string
from flask import Flask, request, jsonify
import secrets
import MailSender as ms

def add_softwareOwner(username, usersurname, useremail, userpassword, usercity, role_id, verification_key):
    conn = Db.connect_to_database()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO softwareowner (OwnerName, OwnerSurname, OwnerEmail, OwnerPassword, OwnerCity, RoleID, VerificationKey) VALUES (%s, %s, %s, %s, %s, %s, %s)", (username, usersurname, useremail, userpassword, usercity, role_id, verification_key))
    conn.commit()
    conn.close()

# User tablosundan belirli bir UserID'ye göre veri silme fonksiyonu
def delete_user(user_id):
    conn = Db.connect_to_database()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM softwareowner WHERE OwnerID=%s", (user_id,))
    conn.commit()
    conn.close()

# Belirli bir UserID'ye göre User tablosundan veri sorgulama fonksiyonu
def query_user(user_id):
    conn = Db.connect_to_database()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM softwareowner WHERE OwnerID=%s", (user_id,))
    user_data = cursor.fetchone()
    conn.close()
    return user_data

# Tüm kullanıcıları getiren fonksiyon
def get_all_users():
    conn = Db.connect_to_database()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM softwareowner")
    users = cursor.fetchall()
    conn.close()
    return users

def login_owner(email, password):
    # Kullanıcıyı veritabanında bul
    conn = Db.connect_to_database()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM softwareowner WHERE Email = %s AND Password = %s", (email, password))
    user = cursor.fetchone()
    
    if user:
        # Kullanıcı doğrulanmış mı kontrol et
        if user['SELECT * FROM Users Where IsVerified = True']:
            # Kullanıcı giriş yapabilir
            conn.close()
            return True
        else:
            # Kullanıcı doğrulanmamış
            conn.close()
            return False
    else:
        # Kullanıcı bulunamadı
        return False
def verify_owner(verificationkey):
    # Veritabanında kullanıcıyı bul ve doğrulama anahtarını kontrol et
    conn = Db.connect_to_database()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE verificationKey = %s", (verificationkey,))
    user = cursor.fetchone()
    conn.close()
    if user:
        print("User verified successfully")
        return True
    else:
        return False