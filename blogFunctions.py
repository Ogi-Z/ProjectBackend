import DbConnection as Db
import string
from flask import Flask, request, jsonify
import secrets
import MailSender as ms

# Blog tablosuna veri ekleme fonksiyonu
def add_blog(user_id, blog_category,BlogTitle, blog_text):
    conn = Db.connect_to_database()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Blog (userid, blogcategory,BlogTitle, blogtext) VALUES (%s, %s,%s, %s)", (user_id, blog_category, BlogTitle ,blog_text))
    conn.commit()
    conn.close()

# Blog tablosuna fotoğraflı veri ekleme fonksiyonu
def add_blog_with_image(user_id, blog_category,BlogTitle , blog_text,image_data):
    conn = Db.connect_to_database()
    cursor = conn.cursor()
    query = """
        INSERT INTO Blog (UserID, BlogCategory,BlogTitle, BlogText, BlogImage)
        VALUES (%s, %s, %s, %s);
        """
    cursor.execute(query, (user_id, blog_category, BlogTitle, blog_text, image_data))
    conn.commit()
    conn.close()

# Belirli bir BlogID'ye göre Blog tablosundan veri silme fonksiyonu
def delete_blog(blog_id):
    conn = Db.connect_to_database()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Blog WHERE BlogID=%s", (blog_id,))
    conn.commit()
    conn.close()

# Belirli bir BlogID'ye göre Blog tablosundan veri sorgulama fonksiyonu
def query_blog(blog_id):
    conn = Db.connect_to_database()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Blog WHERE BlogID=%s", (blog_id,))
    blog_data = cursor.fetchone()
    conn.close()
    return blog_data

# Tüm blogları getiren fonksiyon
def get_all_blogs():
    conn = Db.connect_to_database()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Blog Where Approved = True")
    users = cursor.fetchall()
    conn.close()
    return users
# Tüm unapprowed blogları getiren fonksiyon
def get_all_unapprovedblogs():
    conn = Db.connect_to_database()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Blog Where Approved = False")
    users = cursor.fetchall()
    conn.close()
    return users

def verify_owner(verificationkey):
    # Veritabanında kullanıcıyı bul ve doğrulama anahtarını kontrol et
    conn = Db.connect_to_database()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Blog WHERE Approved = %s", (verificationkey,))
    user = cursor.fetchone()
    conn.close()
    if user:
        print("Software Owner verified successfully")
        return True
    else:
        return False
    
# Blog approve etme fonksiyonu
def approve_blog(blog_id):
    conn = Db.connect_to_database()
    cursor = conn.cursor()
    cursor.execute("UPDATE Blog SET Approved = True WHERE BlogID=%s", (blog_id,))
    conn.commit()
    conn.close()