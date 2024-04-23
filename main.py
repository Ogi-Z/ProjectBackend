import DbConnection as Db
from flask import Flask, request, jsonify
from flask_mail import Mail, Message
import string
import secrets

app = Flask(__name__)
app.config['MAIL_SERVER'] = 'smtp.yandex.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'tmpproject'  
app.config['MAIL_PASSWORD'] = '123321asD.'  

mail = Mail(app)


# Doğrulama anahtarı oluşturma fonksiyonu
def generate_verification_key(length=16):
    """Generate a random verification key."""
    characters = string.ascii_letters + string.digits
    verification_key = ''.join(secrets.choice(characters) for _ in range(length))
    return verification_key


    


# E-posta gönderme fonksiyonu
def send_email_with_verification_key(recipient_email, verification_key):
    try:
        # E-posta gönderme işlemi
        msg = Message("Account Verification", recipients=[recipient_email])
        msg.body = f"Please click the following link to verify your account: http://127.0.0.1:5000/verify/{verification_key}"
        # E-posta içeriğine doğrulama anahtarını eklemek için HTML şablonu kullanılabilir.
        msg.html = f"""
            <html>
                <body>
                    <p>Please click the following link to verify your account:</p>
                    <a href="http://127.0.0.1:5000/verify/{verification_key}">Verify Account</a>
                </body>
            </html>
        """
        mail.send(msg)
        print("Email sent successfully")  # Hata ayıklama çıktısı ekle
    except Exception as e:
        print(f"Error sending email: {e}")  # Hata ayıklama çıktısı ekle

# User tablosuna veri ekleme fonksiyonu
def add_user(username, usersurname, useremail, userpassword, usercity, role_id, verification_key):
    conn = Db.connect_to_database()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (UserName, UserSurname, UserEmail, UserPassword, UserCity, RoleID, VerificationKey) VALUES (%s, %s, %s, %s, %s, %s, %s)", (username, usersurname, useremail, userpassword, usercity, role_id, verification_key))
    conn.commit()
    conn.close()

# User tablosundan belirli bir UserID'ye göre veri silme fonksiyonu
def delete_user(user_id):
    conn = Db.connect_to_database()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Users WHERE UserID=%s", (user_id,))
    conn.commit()
    conn.close()

# Belirli bir UserID'ye göre User tablosundan veri sorgulama fonksiyonu
def query_user(user_id):
    conn = Db.connect_to_database()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Users WHERE UserID=%s", (user_id,))
    user_data = cursor.fetchone()
    conn.close()
    return user_data

# Tüm kullanıcıları getiren fonksiyon
def get_all_users():
    conn = Db.connect_to_database()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Users")
    users = cursor.fetchall()
    conn.close()
    return users

# SoftwareUsability tablosuna veri ekleme fonksiyonu
def add_softwareUsability(user_id, SoftwareUsabilityID, SoftwareUsabilitySoftware, SoftwareUsabilityTopicName, SoftwareUsabilityText):
    conn = Db.connect_to_database()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Blog (UserID, SoftwareUsabilityID, SoftwareUsabilitySoftware, SoftwareUsabilityTopicName, SoftwareUsabilityText) VALUES (?, ?, ?, ?, ?, ?, ?)", (user_id, SoftwareUsabilityID, SoftwareUsabilitySoftware, SoftwareUsabilityTopicName, SoftwareUsabilityText))
    conn.commit()
    conn.close()

# User tablosundan belirli bir BlogID'ye göre veri silme fonksiyonu
def delete_softwareUsability(SoftwareUsabilityID):
    conn = Db.connect_to_database()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Blog WHERE SoftwareUsabilityID=?", (SoftwareUsabilityID,))
    conn.commit()
    conn.close()

# Belirli bir BlogID'ye göre User tablosundan veri sorgulama fonksiyonu
def query_softwareUsability(SoftwareUsabilityID):
    conn = Db.connect_to_database()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM SoftwareUsability WHERE SoftwareUsabilityID=?", (SoftwareUsabilityID,))
    softwareUsability_data = cursor.fetchone()
    conn.close()
    return softwareUsability_data

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
def login_user(email, password):
    # Kullanıcıyı veritabanında bul
    cursor.execute("SELECT * FROM Users WHERE Email = %s AND Password = %s", (email, password))
    user = cursor.fetchone()
    if user:
        # Kullanıcı doğrulanmış mı kontrol et
        if user['IsVerified']:
            # Kullanıcı giriş yapabilir
            return True
        else:
            # Kullanıcı doğrulanmamış
            return False
    else:
        # Kullanıcı bulunamadı
        return False
def verify_user(email, verification_key):
    # Veritabanında kullanıcıyı bul ve doğrulama anahtarını kontrol et
    cursor.execute("SELECT * FROM Users WHERE Email = %s AND VerificationKey = %s", (email, verification_key))
    user = cursor.fetchone()
    if user:
        # Kullanıcıyı doğrula
        cursor.execute("UPDATE Users SET IsVerified = TRUE WHERE Email = %s", (email,))
        conn.commit()
        return True
    else:
        return False

@app.route('/login', methods=['POST'])
def login():
    # İstek verilerini al
    request_data = request.json
    useremail = request_data.get('useremail')
    userpassword = request_data.get('userpassword')

    # Veritabanından kullanıcıyı sorgula
    conn = Db.connect_to_database()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE useremail = %s", (useremail,))
    user = cursor.fetchone()
    conn.close()

    if user:
        # Kullanıcı bulundu, şifreyi kontrol et
        if user[4] == userpassword:  # userpassword indeksi veritabanındaki şifre sütununa bağlı olabilir
            # Şifre doğru, kullanıcı doğrulama durumunu kontrol et
            if user[7]:  # isverified indeksi veritabanındaki isverified sütununa bağlı olabilir
                # Kullanıcı doğrulanmış, giriş başarılı
                return jsonify({'success': True}), 200
            else:
                # Kullanıcı doğrulanmamış, giriş başarısız
                return jsonify({'success': False, 'message': 'User is not verified'}), 401
        else:
            # Şifre yanlış, giriş başarısız
            return jsonify({'success': False, 'message': 'Invalid password'}), 401
    else:
        # Kullanıcı bulunamadı, giriş başarısız
        return jsonify({'success': False, 'message': 'User not found'}), 404

@app.route('/send_email')
def send_email():
    try:
        # E-posta gönderme işlemi
        msg = Message("Subject of the Email", recipients=["recipient@example.com"])
        msg.body = "This is the plain text body of the email"
        msg.html = "<p>This is the HTML body of the email</p>"
        mail.send(msg)
        return "Email sent successfully"
    except Exception as e:
        return str(e)

@app.route('/add_user', methods=['POST'])
def add_user_endpoint():
    request_data = request.json
    # Kullanıcı bilgilerini al
    username = request_data.get('username')
    usersurname = request_data.get('usersurname')
    useremail = request_data.get('useremail')
    userpassword = request_data.get('userpassword')
    usercity = request_data.get('usercity')
    role_id = request_data.get('role_id')
    conn = Db.connect_to_database()
    verification_key = generate_verification_key()
    print (verification_key)
    add_user(username, usersurname, useremail, userpassword, usercity, role_id, verification_key)

    send_email_with_verification_key(useremail, verification_key)

    return f"Verification key sent to {useremail}: {verification_key}"

  

# Tüm kullanıcıları getiren endpoint
@app.route('/users', methods=['GET'])
def get_all_users_endpoint():
    users = get_all_users()
    if users:
        return jsonify(users), 200
    else:
        return jsonify({"message": "No users found"}), 404


# Belirli bir UserID'ye göre User tablosundan veri sorgulama endpoint'i
@app.route('/query_user/<int:user_id>', methods=['GET'])
def query_user_endpoint(user_id):
    user_data = query_user(user_id)
    if user_data:
        return jsonify(user_data), 200
    else:
        return jsonify({"message": "User not found"}), 404

# Belirli bir UserID'ye göre User tablosundan veri silme endpoint'i
@app.route('/delete_user/<int:user_id>', methods=['DELETE'])
def delete_user_endpoint(user_id):
    delete_user(user_id)
    return jsonify({"message": "User deleted successfully"}), 200

# SoftwareUsability tablosuna veri ekleme endpoint'i
@app.route('/add_softwareUsability', methods=['POST'])
def add_softwareUsability_endpoint():
    request_data = request.json
    user_id = request_data.get('user_id')
    SoftwareUsabilityID = request_data.get('SoftwareUsabilityID')
    SoftwareUsabilitySoftware = request_data.get('SoftwareUsabilitySoftware')
    SoftwareUsabilityTopicName = request_data.get('SoftwareUsabilityTopicName')
    SoftwareUsabilityText = request_data.get('SoftwareUsabilityText')
    
    add_softwareUsability(user_id, SoftwareUsabilityID, SoftwareUsabilitySoftware, SoftwareUsabilityTopicName, SoftwareUsabilityText)
    
    return jsonify({"message": "Software usability added successfully"}), 200

# Belirli bir SoftwareUsabilityID'ye göre SoftwareUsability tablosundan veri sorgulama endpoint'i
@app.route('/query_softwareUsability/<int:SoftwareUsabilityID>', methods=['GET'])
def query_softwareUsability_endpoint(SoftwareUsabilityID):
    softwareUsability_data = query_softwareUsability(SoftwareUsabilityID)
    if softwareUsability_data:
        return jsonify(softwareUsability_data), 200
    else:
        return jsonify({"message": "Software usability not found"}), 404

# Belirli bir SoftwareUsabilityID'ye göre SoftwareUsability tablosundan veri silme endpoint'i
@app.route('/delete_softwareUsability/<int:SoftwareUsabilityID>', methods=['DELETE'])
def delete_softwareUsability_endpoint(SoftwareUsabilityID):
    delete_softwareUsability(SoftwareUsabilityID)
    return jsonify({"message": "Software usability deleted successfully"}), 200

# Blog tablosuna veri ekleme endpoint'i
@app.route('/add_blog', methods=['POST'])
def add_blog_endpoint():
    request_data = request.json
    user_id = request_data.get('user_id')
    blog_id = request_data.get('blog_id')
    blog_category = request_data.get('blog_category')
    blog_text = request_data.get('blog_text')
    
    add_blog(user_id, blog_id, blog_category, blog_text)
    
    return jsonify({"message": "Blog added successfully"}), 200

# Belirli bir BlogID'ye göre Blog tablosundan veri sorgulama endpoint'i
@app.route('/query_blog/<int:blog_id>', methods=['GET'])
def query_blog_endpoint(blog_id):
    blog_data = query_blog(blog_id)
    if blog_data:
        return jsonify(blog_data), 200
    else:
        return jsonify({"message": "Blog not found"}), 404

# Belirli bir BlogID'ye göre Blog tablosundan veri silme endpoint'i
@app.route('/delete_blog/<int:blog_id>', methods=['DELETE'])
def delete_blog_endpoint(blog_id):
    delete_blog(blog_id)
    return jsonify({"message": "Blog deleted successfully"}), 200

if __name__ == '__main__':
    app.run(debug=True)
