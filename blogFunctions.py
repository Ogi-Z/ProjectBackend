import DbConnection as Db
import string
from flask import Flask, request, jsonify
import secrets
import MailSender as ms

# Blog tablosuna veri ekleme fonksiyonu
def add_blog(user_id, blog_id, blog_category, blog_text):
    conn = Db.connect_to_database()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Blog (UserID, BlogID, BlogCategory, BlogText) VALUES (?, ?, ?, ?)", (user_id, blog_id, blog_category, blog_text))
    conn.commit()
    conn.close()

# Belirli bir BlogID'ye göre Blog tablosundan veri silme fonksiyonu
def delete_blog(blog_id):
    conn = Db.connect_to_database()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Blog WHERE BlogID=?", (blog_id,))
    conn.commit()
    conn.close()

# Belirli bir BlogID'ye göre Blog tablosundan veri sorgulama fonksiyonu
def query_blog(blog_id):
    conn = Db.connect_to_database()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Blog WHERE BlogID=?", (blog_id,))
    blog_data = cursor.fetchone()
    conn.close()
    return blog_data

# Tüm blogları getiren fonksiyon
def get_all_blogs():
    conn = Db.connect_to_database()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Blog")
    users = cursor.fetchall()
    conn.close()
    return users
