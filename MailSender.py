import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# E-posta gönderme fonksiyonu
def sendMailSoftwareOwner(email, verificationKey):
    # Gönderici ve alıcı bilgileri
    gonderici = 'bubirddeneme@gmail.com'
    alici = 'bubirddeneme@gmail.com'
    # E-posta başlık ve içeriği
    baslik = 'Verification Code for Coma Gen-e' # buraya kayıt olma doğrulama zart zurt yazılır
    icerik = f'Hello Welcome To Coma Gen-e. Here is your verification code: {verificationKey}, The Software Owners E-Mail is: {email}' # buraya doğrulama kodu yazılır 
    # SMTP sunucu ve bağlantı bilgileri
    # bu kısma hiç dokunma 
    smtp_sunucu = 'smtp.gmail.com'
    smtp_port = 587
    kullanici = 'bubirddeneme@gmail.com'
    sifre = 'kurn dljr pufh mmcm' 
    # E-posta gövdesi oluşturma
    msg = MIMEMultipart()
    msg['From'] = gonderici
    msg['To'] = alici
    msg['Subject'] = baslik
    msg.attach(MIMEText(icerik, 'plain'))
    # SMTP bağlantısı ve e-posta gönderme
    try:
        server = smtplib.SMTP(smtp_sunucu, smtp_port)
        server.starttls()
        server.login(kullanici, sifre)
        server.sendmail(gonderici, alici, msg.as_string())
        print('E-posta başarıyla gönderildi.')
    except Exception as e:
        print('E-posta gönderme hatası:', e)
    finally:
        server.quit()

def sendMail(alici, verificationKey):
    # Gönderici ve alıcı bilgileri
    gonderici = 'bubirddeneme@gmail.com'
    # E-posta başlık ve içeriği
    baslik = 'Verification Code for Coma Gen-e' # buraya kayıt olma doğrulama zart zurt yazılır
    icerik = f'Hello Welcome To Coma Gen-e. Here is your verification code: {verificationKey}' # buraya doğrulama kodu yazılır 

    # SMTP sunucu ve bağlantı bilgileri
    # bu kısma hiç dokunma 
    smtp_sunucu = 'smtp.gmail.com'
    smtp_port = 587
    kullanici = 'bubirddeneme@gmail.com'
    sifre = 'kurn dljr pufh mmcm' 

    # E-posta gövdesi oluşturma
    msg = MIMEMultipart()
    msg['From'] = gonderici
    msg['To'] = alici
    msg['Subject'] = baslik
    msg.attach(MIMEText(icerik, 'plain'))

    # SMTP bağlantısı ve e-posta gönderme
    try:
        server = smtplib.SMTP(smtp_sunucu, smtp_port)
        server.starttls()
        server.login(kullanici, sifre)
        server.sendmail(gonderici, alici, msg.as_string())
        print('E-posta başarıyla gönderildi.')
    except Exception as e:
        print('E-posta gönderme hatası:', e)
    finally:
        server.quit()
