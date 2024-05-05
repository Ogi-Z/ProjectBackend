import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Gönderici ve alıcı bilgileri
gonderici = 'bubirddeneme@gmail.com'
alici = 'alparslanfatihkaya@gmail.com' # kullanıcı mail adresi 

# E-posta başlık ve içeriği
baslik = 'Python ile E-posta Gönderme' # buraya kayıt olma doğrulama zart zurt yazılır
icerik = 'Merhaba, bu bir Python ile gönderilen e-posta örneğidir.' # buraya doğrulama kodu yazılır 

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
