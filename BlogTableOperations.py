import DbConnection as Db



# Blog tablosuna veri ekleme fonksiyonu
def add_blog(user_id, blog_id, blog_category, blog_text):
    conn = Db.connect_to_database()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Blog (UserID, BlogID, BlogCategory, BlogText) VALUES (?, ?, ?, ?, ?, ?, ?)", (user_id, blog_id, blog_category, blog_text))
    conn.commit()
    conn.close()

# User tablosundan belirli bir BlogID'ye göre veri silme fonksiyonu
def delete_blog(blog_id):
    conn = Db.connect_to_database()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Blog WHERE BlogID=?", (blog_id,))
    conn.commit()
    conn.close()

# Belirli bir BlogID'ye göre User tablosundan veri sorgulama fonksiyonu
def query_blog(blog_id):
    conn = Db.connect_to_database()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Blog WHERE BlogID=?", (blog_id,))
    blog_data = cursor.fetchone()
    conn.close()
    return blog_data
