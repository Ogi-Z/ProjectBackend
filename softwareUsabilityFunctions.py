import DbConnection as Db
import string
from flask import Flask, request, jsonify
import secrets

# SoftwareUsability tablosuna veri ekleme fonksiyonu
def add_softwareUsability(user_id, SoftwareUsabilitySoftware, SoftwareUsabilityTopicName, SoftwareUsabilityText):
    conn = Db.connect_to_database()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO SoftwareUsability (userid, softwareusabilitysoftware, softwareusabilitytopicname, softwareusabilitytext) VALUES (%s, %s, %s, %s)", (user_id, SoftwareUsabilitySoftware, SoftwareUsabilityTopicName, SoftwareUsabilityText))
    conn.commit()
    conn.close()

# SoftwareUsability tablosuna veri ekleme fonksiyonu
def add_softwareUsability_with_image(user_id, SoftwareUsabilitySoftware, SoftwareUsabilityTopicName, SoftwareUsabilityText, image_data):
    conn = Db.connect_to_database()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO SoftwareUsability (userid, softwareusabilitysoftware, softwareusabilitytopicname, softwareusabilitytext, SoftwareUsabilityImage) VALUES (%s, %s, %s, %s, %s)", (user_id, SoftwareUsabilitySoftware, SoftwareUsabilityTopicName, SoftwareUsabilityText,image_data))
    conn.commit()
    conn.close()

# User tablosundan belirli bir SoftwareUsabilityID'ye göre veri silme fonksiyonu
def delete_softwareUsability(SoftwareUsabilityID):
    conn = Db.connect_to_database()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM SoftwareUsability WHERE SoftwareUsabilityID=%s", (SoftwareUsabilityID,))
    conn.commit()
    conn.close()

# Belirli bir SoftwareUsabilityID'ye göre User tablosundan veri sorgulama fonksiyonu
def query_softwareUsability(SoftwareUsabilityID):
    conn = Db.connect_to_database()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM SoftwareUsability WHERE SoftwareUsabilityID=%s", (SoftwareUsabilityID,))
    softwareUsability_data = cursor.fetchone()
    conn.close()
    return softwareUsability_data

# Tüm SoftwareUsabilityleri getiren fonksiyon
def get_all_softwareUsabilityUnApproved():
    conn = Db.connect_to_database()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM SoftwareUsability WHERE Approved = False")
    users = cursor.fetchall()
    conn.close()
    return users
# Tüm SoftwareUsabilityleri getiren fonksiyon
def get_all_softwareUsability():
    conn = Db.connect_to_database()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM SoftwareUsability WHERE Approved = True")
    users = cursor.fetchall()
    conn.close()
    return users

# SoftwareUsability onaylama fonksiyonu
def approve_softwareusability(softwareusability_id):
    conn = Db.connect_to_database()
    cursor = conn.cursor()
    cursor.execute("UPDATE softwareusability SET Approved = True WHERE softwareusabilityid=%s", (softwareusability_id,))
    conn.commit()
    conn.close()

# SoftwareUsability Add Comment
def add_softwareusability_comment(userid, softwareusability_id, comment_text):
    conn = Db.connect_to_database()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO softwareusabilitycomments (userid, softwareusabilityid, commenttext) VALUES (%s,%s, %s)", (userid, softwareusability_id, comment_text))
    conn.commit()
    conn.close()

# SoftwareUsability Get Comments
def get_softwareusability_comments(softwareusability_id):
    conn = Db.connect_to_database()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM softwareusabilitycomments WHERE softwareusabilityid=%s", (softwareusability_id,))
    comments = cursor.fetchall()
    conn.close()
    return comments

# SoftwareUsability Get Softwares
def get_softwareusability_softwares():
    conn = Db.connect_to_database()
    cursor = conn.cursor()
    cursor.execute("SELECT SoftwareUsabilitySoftware FROM softwareusability")
    softwareusabilities = cursor.fetchall()
    conn.close()
    return softwareusabilities

# SoftwareUsability için beğenme fonksiyonu
def like_softwareusability(softwareusability_id):
    conn = Db.connect_to_database()
    cursor = conn.cursor()
    cursor.execute("UPDATE softwareusability SET Likes = Likes + 1 WHERE softwareusabilityid=%s", (softwareusability_id,))
    conn.commit()
    conn.close()

# SoftwareUsability için beğenmeme fonksiyonu
def dislike_softwareusability(softwareusability_id):
    conn = Db.connect_to_database()
    cursor = conn.cursor()
    cursor.execute("UPDATE softwareusability SET Dislikes = Dislikes + 1 WHERE softwareusabilityid=%s", (softwareusability_id,))
    conn.commit()
    conn.close()
