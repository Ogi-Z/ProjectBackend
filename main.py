import DbConnection as Db
import string
from flask import Flask, request, jsonify
import secrets
import MailSender as ms
import userFunctions as uf
import softwareUsabilityFunctions as sUF
import blogFunctions as bF
import softwareOwnerFunctions as so
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Doğrulama anahtarı oluşturma fonksiyonu
def generate_verification_key(length=16):
    """Generate a random verification key."""
    characters = string.ascii_letters + string.digits
    verification_key = ''.join(secrets.choice(characters) for _ in range(length))
    return verification_key

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
    if user:
        if user[4] == userpassword:  
            # Sifre Dogru, isverified kontrolu yapma
            cursor.execute("SELECT * FROM users WHERE useremail = %s AND isverified = true", (useremail,))
            verified_user = cursor.fetchone()
            conn.close()
            if verified_user:
            # Hersey Dogru, login basarili
                return jsonify({'success': True}), 200
            else:
            # User verify edilmemis, login basarisiz
                return jsonify({'success': False, 'message': 'User is not verified'}), 401
        else:
            # Sifre Yanlıs, login basarisiz
            return jsonify({'success': False, 'message': 'Invalid password'}), 401
    else:
        # User bulunamadı, login basarisiz
        conn.close()
        return jsonify({'success': False, 'message': 'User not found'}), 404
    
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
    # E-posta gönderme işlemi
    ms.sendMail(useremail, verification_key)
    uf.add_user(username, usersurname, useremail, userpassword, usercity, role_id, verification_key)
    return f"Verification key sent to {useremail}: {verification_key}"
 
@app.route('/verify', methods=['GET'])
def verify():
    # Kullanıcıyı doğrula
    request_data = request.json
    verificationkeys = request_data.get('verificationkey')
    conn = Db.connect_to_database()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE verificationKey = %s", (verificationkeys,))
    user = cursor.fetchone()
    if user:
        cursor.execute("UPDATE users SET isverified = TRUE WHERE verificationkey= %s", (verificationkeys,))
        conn.commit()
        conn.close()
        return "User verified successfully"
    else:
        conn.close()
        return "Invalid verification key"

# Tüm kullanıcıları getiren endpoint
@app.route('/users', methods=['GET'])
def get_all_users_endpoint():
    users = uf.get_all_users()
    if users:
        return jsonify(users), 200
    else:
        return jsonify({"message": "No users found"}), 404

# Belirli bir UserID'ye göre User tablosundan veri sorgulama endpoint'i
@app.route('/query_user/<int:user_id>', methods=['GET'])
def query_user_endpoint(user_id):
    user_data = uf.query_user(user_id)
    if user_data:
        return jsonify(user_data), 200
    else:
        return jsonify({"message": "User not found"}), 404

# Belirli bir UserID'ye göre User tablosundan veri silme endpoint'i
@app.route('/delete_user/<int:user_id>', methods=['DELETE'])
def delete_user_endpoint(user_id):
    uf.delete_user(user_id)
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
    sUF.add_softwareUsability(user_id, SoftwareUsabilityID, SoftwareUsabilitySoftware, SoftwareUsabilityTopicName, SoftwareUsabilityText)
    return jsonify({"message": "Software usability added successfully"}), 200
# Tüm SoftwareUsabilityleri getiren endpoint
@app.route('/softwareUsability', methods=['GET'])
def get_all_softwareUsabilitys_endpoint():
    softwareUsability = sUF.get_all_softwareUsability()
    if softwareUsability:
        return jsonify(softwareUsability), 200
    else:
        return jsonify({"message": "No Software Usability found"}), 404

# Belirli bir SoftwareUsabilityID'ye göre SoftwareUsability tablosundan veri sorgulama endpoint'i
@app.route('/query_softwareUsability/<int:SoftwareUsabilityID>', methods=['GET'])
def query_softwareUsability_endpoint(SoftwareUsabilityID):
    softwareUsability_data = sUF.query_softwareUsability(SoftwareUsabilityID)
    if softwareUsability_data:
        return jsonify(softwareUsability_data), 200
    else:
        return jsonify({"message": "Software usability not found"}), 404

# Belirli bir SoftwareUsabilityID'ye göre SoftwareUsability tablosundan veri silme endpoint'i
@app.route('/delete_softwareUsability/<int:SoftwareUsabilityID>', methods=['DELETE'])
def delete_softwareUsability_endpoint(SoftwareUsabilityID):
    sUF.delete_softwareUsability(SoftwareUsabilityID)
    return jsonify({"message": "Software usability deleted successfully"}), 200

# Blog tablosuna veri ekleme endpoint'i
@app.route('/add_blog', methods=['POST'])
def add_blog_endpoint():
    request_data = request.json
    user_id = request_data.get('user_id')
    blog_id = request_data.get('blog_id')
    blog_category = request_data.get('blog_category')
    blog_text = request_data.get('blog_text')
    
    bF.add_blog(user_id, blog_id, blog_category, blog_text)
    
    return jsonify({"message": "Blog added successfully"}), 200

# Belirli bir BlogID'ye göre Blog tablosundan veri sorgulama endpoint'i
@app.route('/query_blog/<int:blog_id>', methods=['GET'])
def query_blog_endpoint(blog_id):
    blog_data = bF.query_blog(blog_id)
    if blog_data:
        return jsonify(blog_data), 200
    else:
        return jsonify({"message": "Blog not found"}), 404

# Belirli bir BlogID'ye göre Blog tablosundan veri silme endpoint'i
@app.route('/delete_blog/<int:blog_id>', methods=['DELETE'])
def delete_blog_endpoint(blog_id):
    bF.delete_blog(blog_id)
    return jsonify({"message": "Blog deleted successfully"}), 200

# Tüm blogları getiren endpoint
@app.route('/blogs', methods=['GET'])
def get_all_blogs_endpoint():
    blog = bF.get_all_blogs()
    if blog:
        return jsonify(blog), 200
    else:
        return jsonify({"message": "No users found"}), 404
# Tüm software ownerları getiren endpoint  
@app.route('/softwareowners', methods=['GET'])
def get_all_softwareowners_endpoint():
    owners = so.get_all_owners()
    if owners:
        return jsonify(owners), 200
    else:
        return jsonify({"message": "No Software Owner found"}), 404
    
# Software Owner ekleme endpointi
@app.route('/add_softwareowner', methods=['POST'])
def add_owner_endpoint():
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
    # E-posta gönderme işlemi
    so.add_softwareOwner(username, usersurname, useremail, userpassword, usercity, role_id, verification_key)
    ms.sendMailSoftwareOwner(useremail, verification_key)
    
    return f"Your register request send to admin"

# Software Ownerlar için giriş
@app.route('/ownerlogin', methods=['POST'])
def ownerlogin():
    # İstek verilerini al
    request_data = request.json
    useremail = request_data.get('useremail')
    userpassword = request_data.get('userpassword')
    # Veritabanından kullanıcıyı sorgula
    conn = Db.connect_to_database()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM softwareowner WHERE owneremail = %s", (useremail,))
    user = cursor.fetchone()
    if user:
        if user[4] == userpassword:  
            # Sifre Dogru, isverified kontrolu yapma
            cursor.execute("SELECT * FROM softwareowner WHERE owneremail = %s AND isverified = true", (useremail,))
            verified_owner = cursor.fetchone()
            conn.close()
            if verified_owner:
            # Hersey Dogru, login basarili
                return jsonify({'success': True}), 200
            else:
            # User verify edilmemis, login basarisiz
                return jsonify({'success': False, 'message': 'Owner is not verified'}), 401
        else:
            # Sifre Yanlıs, login basarisiz
            return jsonify({'success': False, 'message': 'Invalid password'}), 401
    else:
        # User bulunamadı, login basarisiz
        conn.close()
        return jsonify({'success': False, 'message': 'Owner not found'}), 404
@app.route('/verifyowner', methods=['GET'])
def verifyOwner():
    # Kullanıcıyı doğrula
    request_data = request.json
    verificationkeys = request_data.get('verificationkey')
    conn = Db.connect_to_database()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM softwareowner WHERE verificationKey = %s", (verificationkeys,))
    user = cursor.fetchone()
    if user:
        cursor.execute("UPDATE softwareowner SET isverified = TRUE WHERE verificationkey= %s", (verificationkeys,))
        conn.commit()
        conn.close()
        return "SoftwareOwner verified successfully"
    else:
        conn.close()
        return "Invalid verification key"

if __name__ == '__main__':
    app.run(debug=True)
