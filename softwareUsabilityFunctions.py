import DbConnection as Db
import string
from flask import Flask, request, jsonify
import secrets

# SoftwareUsability tablosuna veri ekleme fonksiyonu
def add_softwareUsability(user_id, SoftwareUsabilityID, SoftwareUsabilitySoftware, SoftwareUsabilityTopicName, SoftwareUsabilityText):
    conn = Db.connect_to_database()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO SoftwareUsability (UserID, SoftwareUsabilityID, SoftwareUsabilitySoftware, SoftwareUsabilityTopicName, SoftwareUsabilityText) VALUES (?, ?, ?, ?, ?)", (user_id, SoftwareUsabilityID, SoftwareUsabilitySoftware, SoftwareUsabilityTopicName, SoftwareUsabilityText))
    conn.commit()
    conn.close()

# User tablosundan belirli bir SoftwareUsabilityID'ye göre veri silme fonksiyonu
def delete_softwareUsability(SoftwareUsabilityID):
    conn = Db.connect_to_database()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Blog WHERE SoftwareUsabilityID=?", (SoftwareUsabilityID,))
    conn.commit()
    conn.close()

# Belirli bir SoftwareUsabilityID'ye göre User tablosundan veri sorgulama fonksiyonu
def query_softwareUsability(SoftwareUsabilityID):
    conn = Db.connect_to_database()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM SoftwareUsability WHERE SoftwareUsabilityID=?", (SoftwareUsabilityID,))
    softwareUsability_data = cursor.fetchone()
    conn.close()
    return softwareUsability_data

# Tüm SoftwareUsabilityleri getiren fonksiyon
def get_all_softwareUsability():
    conn = Db.connect_to_database()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM SoftwareUsability")
    users = cursor.fetchall()
    conn.close()
    return users
