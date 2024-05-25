import DbConnection as Db
import string
from flask import Flask, request, jsonify
import secrets
import MailSender as ms

# Software Owner ekleme fonksiyonu
def add_softwareOwner(username, usersurname, useremail, userpassword, ownersSoftware ,usercity, role_id, verification_key):
    conn = Db.connect_to_database()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO softwareowner (OwnerName, OwnerSurname, OwnerEmail, OwnerPassword, OwnersSoftware, OwnerCity, RoleID, VerificationKey) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (username, usersurname, useremail, userpassword, ownersSoftware,usercity, role_id, verification_key))
    conn.commit()
    conn.close()

# SoftwareOwner tablosundan belirli bir SoftwareOwnerID'ye göre veri silme fonksiyonu
def delete_user(user_id):
    conn = Db.connect_to_database()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM softwareowner WHERE OwnerID=%s", (user_id,))
    conn.commit()
    conn.close()

# Belirli bir SoftwareOwnerID'ye göre Softwareowner tablosundan veri sorgulama fonksiyonu
def query_owner(user_id):
    conn = Db.connect_to_database()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM softwareowner WHERE OwnerID=%s", (user_id,))
    user_data = cursor.fetchone()
    conn.close()
    return user_data

# Tüm softwareOwnerları getiren fonksiyon
def get_all_owners():
    conn = Db.connect_to_database()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM softwareowner")
    users = cursor.fetchall()
    conn.close()
    return users

# SoftwareOwner login fonksiyonu
def login_owner(email, password):
    # Kullanıcıyı veritabanında bul
    conn = Db.connect_to_database()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM softwareowner WHERE Email = %s AND Password = %s", (email, password))
    user = cursor.fetchone()
    
    if user:
        # Kullanıcı doğrulanmış mı kontrol et
        if user['SELECT * FROM softwareowner Where IsVerified = True']:
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


# SoftwareOwner verify etme fonksiyonu
def verify_owner(verificationkey):
    # Veritabanında kullanıcıyı bul ve doğrulama anahtarını kontrol et
    conn = Db.connect_to_database()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM softwareowner WHERE verificationKey = %s", (verificationkey,))
    user = cursor.fetchone()
    conn.close()
    if user:
        print("Software Owner verified successfully")
        return True
    else:
        return False
    
# Unverified SoftwareOwners getiren fonksiyon
def get_all_unverified_owners():
    conn = Db.connect_to_database()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM softwareowner WHERE IsVerified = False")
    users = cursor.fetchall()
    conn.close()
    return users

# SoftwareOwner Software görüntüleme fonksiyonu
def view_software(OwnersSoftware):
    conn = Db.connect_to_database()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM SoftwareUsability WHERE SoftwareUsabilitySoftware  = %s", (OwnersSoftware,))
    software = cursor.fetchone()
    conn.close()
    return software