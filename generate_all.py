import qrcode
import json
from pathlib import Path
import shutil

# Пути
BASE = Path(__file__).parent
OUTPUT = BASE / "output"
QR_DIR = OUTPUT / "assets/qrcodes"
CSS_DIR = OUTPUT / "assets/css"
IMG_DIR = OUTPUT / "assets/img"
LOGO_SRC = BASE / "ProspectBoxing2.png"
LOGO = "assets/img/ProspectBoxing2.png"

# Создаём директории
QR_DIR.mkdir(parents=True, exist_ok=True)
CSS_DIR.mkdir(parents=True, exist_ok=True)
IMG_DIR.mkdir(parents=True, exist_ok=True)

# Копируем логотип (один раз)
shutil.copy(LOGO_SRC, IMG_DIR / LOGO_SRC.name)

# Генерируем style.css
style_css = """
body { background:#111; color:#fff; font-family:'Segoe UI',Arial,sans-serif; margin:0; }
.container { max-width:440px; margin:0 auto; padding:36px 12px 0 12px;}
.logo { display:flex; justify-content:center; margin-bottom:34px;}
.logo img { width:150px; max-width:80vw;}
.person-title { font-size:2em; font-weight:600; text-align:center; margin-bottom:28px;}
.contacts-list { margin-top:36px;}
.contact-block { display:flex; align-items:center; background:#1a1a1a; color:#fff; border-radius:14px; margin-bottom:22px; text-decoration:none; box-shadow:0 2px 10px #0004; min-height:64px; transition:box-shadow 0.2s;}
.contact-block:hover { box-shadow:0 4px 16px #0009; background:#232323;}
.icon { width:54px; height:54px; margin:0 16px; border-radius:10px; background:#333; display:flex; align-items:center; justify-content:center; font-size:2em;}
.icon img { width:32px; height:32px; object-fit:contain;}
.contact-content { flex:1; min-width:0;}
.contact-title { font-size:1.09em; font-weight:600; margin-bottom:2px;}
.contact-desc { font-size:0.97em; opacity:0.77;}
@media (max-width: 500px) {
  .container {padding: 18px 2vw 2vw;}
  .logo img {width: 100px;}
  .icon {width:36px; height:36px; margin:0 8px;}
  .icon img {width:20px; height:20px;}
}
"""
with open(CSS_DIR / "style.css", "w", encoding="utf-8") as f:
    f.write(style_css)

# Загружаем контакты
with open(BASE / "contacts.json", encoding="utf-8") as f:
    people = json.load(f)

# HTML шаблон для личной страницы
html_template = """<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <title>{name} — Prospect Boxing</title>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <link rel="stylesheet" href="assets/css/style.css">
</head>
<body>
  <div class="container">
    <div class="logo"><img src="{logo}" alt="Prospect Boxing Logo"></div>
    <div class="person-title">{name}</div>
    <div class="contacts-list">
      {blocks}
    </div>
  </div>
</body>
</html>
"""

# Генерация персональных html и QR
for p in people:
    blocks = ""
    # WhatsApp
    if p.get("whatsapp"):
        for wa in p["whatsapp"]:
            blocks += f"""
    <a class="contact-block" href="https://wa.me/{wa}" target="_blank">
      <span class="icon"><img src="https://upload.wikimedia.org/wikipedia/commons/6/6b/WhatsApp.svg" alt="WA"></span>
      <span class="contact-content">
        <div class="contact-title">WhatsApp</div>
        <div class="contact-desc">+{wa}</div>
      </span>
    </a>"""
    # Телефон
    if p.get("phones"):
        for phone in p["phones"]:
            blocks += f"""
    <a class="contact-block" href="tel:+{phone}">
      <span class="icon">📞</span>
      <span class="contact-content">
        <div class="contact-title">Телефон</div>
        <div class="contact-desc">+{phone}</div>
      </span>
    </a>"""
    # Email
    if p.get("email"):
        blocks += f"""
    <a class="contact-block" href="mailto:{p['email']}">
      <span class="icon">✉️</span>
      <span class="contact-content">
        <div class="contact-title">Email</div>
        <div class="contact-desc">{p['email']}</div>
      </span>
    </a>"""
    # Сайт
    if p.get("site"):
        blocks += f"""
    <a class="contact-block" href="{p['site']}" target="_blank">
      <span class="icon"><img src="https://www.prospectboxing.ru/favicon.ico" alt="Site"></span>
      <span class="contact-content">
        <div class="contact-title">Сайт</div>
        <div class="contact-desc">{p['site'].replace('https://','')}</div>
      </span>
    </a>"""
    # VK
    if p.get("vk"):
        blocks += f"""
    <a class="contact-block" href="{p['vk']}" target="_blank">
      <span class="icon"><img src="https://upload.wikimedia.org/wikipedia/commons/2/21/VK.com-logo.svg" alt="VK"></span>
      <span class="contact-content">
        <div class="contact-title">ВКонтакте</div>
        <div class="contact-desc">{p['vk'].replace('https://vk.com/','vk.com/')}</div>
      </span>
    </a>"""

    # --- Сохраняем персональный HTML
    page_name = f"person_{p['id']}.html"
    html_out = html_template.format(name=p["name"], logo=LOGO, blocks=blocks)
    with open(OUTPUT / page_name, "w", encoding='utf-8') as f:
        f.write(html_out)

    # --- Генерируем QR (ссылку на файл, предполагается, что будет на GitHub Pages)
    qr_url = f"https://kyznetsovserega.github.io/prospectboxing-cards/{page_name}"  # <-- подставь свой путь!
    qr_img = qrcode.make(qr_url)
    qr_img.save(QR_DIR / f"qr_{p['id']}.png")

print("Готово! Персональные страницы и QR-коды сгенерированы.")
