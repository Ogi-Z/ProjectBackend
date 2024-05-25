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

# Kullanıcı giriş endpoint'i
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
                return jsonify({'success': True},{'id': user[0]}), 200
            else:
            # User verify edilmemis, login basarisiz
                return jsonify({'success': False, 'message': 'User is not verified'}), 401
        else:
            # Sifre Yanlıs, login basarisiz
            return jsonify({'success': False, 'message': 'Invalid password'}), 409
    else:
        # User bulunamadı, login basarisiz
        conn.close()
        return jsonify({'success': False, 'message': 'User not found'}), 404
    
# Kullanıcı kayıt endpoint'i
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
 
@app.route('/verify', methods=['POST'])
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
        return "User verified successfully",200
    else:
        conn.close()
        return "Invalid verification key",401

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
    SoftwareUsabilitySoftware = request_data.get('SoftwareUsabilitySoftware')
    SoftwareUsabilityTopicName = request_data.get('SoftwareUsabilityTopicName')
    SoftwareUsabilityText = request_data.get('SoftwareUsabilityText')
    if 'image' in request.files:
        file = request.files['image']
        image_data = file.read()
        sUF.add_softwareUsability_with_image(user_id, SoftwareUsabilitySoftware, SoftwareUsabilityTopicName, SoftwareUsabilityText,image_data)
    else:
        image_data = None
        sUF.add_softwareUsability(user_id, SoftwareUsabilitySoftware, SoftwareUsabilityTopicName, SoftwareUsabilityText)

    return jsonify({"message": "Software usability added successfully"}), 200

# Tüm SoftwareUsabilityleri getiren endpoint
@app.route('/softwareUsability', methods=['GET'])
def get_all_softwareUsabilitys_endpoint():
    softwareUsability = sUF.get_all_softwareUsability()
    if softwareUsability:
        return jsonify(softwareUsability), 200
    else:
        return jsonify({"message": "No Software Usability found"}), 404

# Tüm SoftwareUsabilityleri getiren endpoint
@app.route('/softwareUsabilityUnApproved', methods=['GET'])
def get_all_softwareUsabilityUnApproved_endpoint():
    softwareUsability = sUF.get_all_softwareUsabilityUnApproved()
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
    blog_category = request_data.get('blog_category')
    blog_title = request_data.get('blog_title')
    blog_text = request_data.get('blog_text')
    if 'image' in request.files:
        file = request.files['image']
        image_data = file.read()
        bF.add_blog_with_image(user_id, blog_category, blog_title, blog_text, image_data)
    else:
        image_data = None
        bF.add_blog(user_id, blog_category,blog_title, blog_text)
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

# Unverified software ownerları getiren endpoint
@app.route('/unverifiedsoftwareowners', methods=['GET'])
def get_all_unverified_softwareowners_endpoint():
    owners = so.get_all_unverified_owners()
    if owners:
        return jsonify(owners), 200
    else:
        return jsonify({"message": "No Software Owner found"}), 404
    
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
    ownersoftware = request_data.get('ownersoftware')
    usercity = request_data.get('usercity')
    role_id = request_data.get('role_id')
    softwareproduct = request_data.get('softwareproduct')
    conn = Db.connect_to_database()
    verification_key = generate_verification_key()
    print (verification_key)
    # E-posta gönderme işlemi
    so.add_softwareOwner(username, usersurname, useremail, userpassword, ownersoftware, usercity, role_id, verification_key)
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
    
# Software Owner doğrulama
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

# Blog onaylama
@app.route('/approveblog', methods=['POST'])
def approveBlog():
    request_data = request.json
    blog_id = request_data.get('blog_id')
    conn = Db.connect_to_database()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Blog WHERE blogid = %s", (blog_id,))
    user = cursor.fetchone()
    if user:
        cursor.execute("UPDATE blog SET approved = TRUE WHERE blogid= %s", (blog_id,))
        conn.commit()
        conn.close()
        return "Blog approved successfully"
    else:
        conn.close()
        return "Invalid blog id"
    

# Software Usability onaylama
@app.route('/approvesoftwareusability', methods=['POST'])
def approveSoftwareUsability():
    request_data = request.json
    softwareusability_id = request_data.get('softwareusability_id')
    conn = Db.connect_to_database()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM softwareusability WHERE softwareusabilityid = %s", (softwareusability_id,))
    user = cursor.fetchone()
    if user:
        cursor.execute("UPDATE softwareusability SET approved = TRUE WHERE softwareusabilityid= %s", (softwareusability_id,))
        conn.commit()
        conn.close()
        return "Software usability approved successfully"
    else:
        conn.close()
        return "Invalid software usability id"
    
# Unapprowed Software Usability
@app.route('/unapprovedsoftwareusability', methods=['GET'])
def unapprovedSoftwareUsability():
    softwareUsability = sUF.get_all_softwareUsabilityUnApproved()
    if softwareUsability:
        return jsonify(softwareUsability), 200
    else:
        return jsonify({"message": "No Software Usability found"}), 404
    
# Unapproved Blog
@app.route('/unapprovedblogs', methods=['GET'])
def unapprovedBlogs():
    blog = bF.get_all_unapprovedblogs()
    if blog:
        return jsonify(blog), 200
    else:
        return jsonify({"message": "No users found"}), 404
    
# SoftwareUsability yorum ekleme endpoint'i
@app.route('/add_softwareUsabilityComment', methods=['POST'])
def add_softwareUsabilityComment_endpoint():
    request_data = request.json
    user_id = request_data.get('user_id')
    softwareusability_id = request_data.get('softwareusability_id')
    comment_text = request_data.get('comment_text')
    sUF.add_softwareusability_comment(user_id, softwareusability_id, comment_text)
    return jsonify({"message": "Software usability comment added successfully"}), 200

# Software Usability yorumları getiren endpoint
@app.route('/softwareUsabilityComments/<int:softwareusability_id>', methods=['GET'])
def get_softwareUsabilityComments_endpoint(softwareusability_id):
    comments = sUF.get_softwareusability_comments(softwareusability_id)
    if comments:
        return jsonify(comments), 200
    else:
        return jsonify({"message": "No comments found"}), 404
    
# Software Usability Softwarelarını getiren endpoint
@app.route('/softwareUsabilitySoftwares', methods=['GET'])
def get_softwareUsabilitySoftwares_endpoint():
    softwares = sUF.get_softwareusability_softwares()
    if softwares:
        return jsonify(softwares), 200
    else:
        return jsonify({"message": "No softwares found"}), 404
    
# Software Usability beğenme endpoint'i
@app.route('/like_softwareusability', methods=['POST'])
def like_softwareusability_endpoint():
    request_data = request.json
    softwareusability_id = request_data.get('softwareusability_id')
    sUF.like_softwareusability(softwareusability_id)
    return jsonify({"message": "Software usability liked successfully"}), 200

# Software Usability beğenmeme endpoint'i
@app.route('/dislike_softwareusability', methods=['POST'])
def dislike_softwareusability_endpoint():
    request_data = request.json
    softwareusability_id = request_data.get('softwareusability_id')
    sUF.dislike_softwareusability(softwareusability_id)
    return jsonify({"message": "Software usability disliked successfully"}), 200

# Blog beğenme endpoint'i
@app.route('/like_blog', methods=['POST'])
def like_blog_endpoint():
    request_data = request.json
    blog_id = request_data.get('blog_id')
    bF.like_blog(blog_id)
    return jsonify({"message": "Blog liked successfully"}), 200

# Blog beğenmeme endpoint'i
@app.route('/dislike_blog', methods=['POST'])
def dislike_blog_endpoint():
    request_data = request.json
    blog_id = request_data.get('blog_id')
    bF.dislike_blog(blog_id)
    return jsonify({"message": "Blog disliked successfully"}), 200

if __name__ == '__main__':
    app.run(debug=True)
