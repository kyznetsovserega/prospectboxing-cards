import qrcode
import json
from pathlib import Path
import shutil

# Пути
BASE = Path(__file__).parent
OUTPUT = BASE / "docs"

QR_DIR = OUTPUT / "qrcodes"
CSS_DIR = OUTPUT / "css"
IMG_DIR = OUTPUT / "img"
LOGO_SRC = BASE / "logo_prospect.png"
LOGO = "img/logo_prospect.png"

QR_DIR.mkdir(parents=True, exist_ok=True)
CSS_DIR.mkdir(parents=True, exist_ok=True)
IMG_DIR.mkdir(parents=True, exist_ok=True)

# Копируем логотип
shutil.copy(LOGO_SRC, IMG_DIR / LOGO_SRC.name)

# Общий CSS
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
.qr-thumb { width:46px; height:46px; object-fit:contain; border-radius:10px; background:#fff; margin-right:18px; box-shadow:0 2px 6px #0002;}
.person-list { margin-top:32px; }
.person-item { display:flex; align-items:center; background:#181818; border-radius:12px; margin-bottom:16px; padding:10px 18px; box-shadow:0 2px 10px #0004; transition:box-shadow 0.2s; }
.person-item:hover { box-shadow:0 4px 16px #0009; background:#232323;}
.person-link { color:#fff; text-decoration:none; font-size:1.09em; font-weight:500;}
@media (max-width: 500px) {
  .container {padding: 18px 2vw 2vw;}
  .logo img {width: 100px;}
  .icon {width:36px; height:36px; margin:0 8px;}
  .icon img {width:20px; height:20px;}
  .qr-thumb {width:30px; height:30px; margin-right:10px;}
  .person-item {padding:7px 6px;}
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
  <link rel="stylesheet" href="css/style.css">
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

# HTML шаблон для index
index_template = """<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <title>Контакты Prospect Boxing</title>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <link rel="stylesheet" href="css/style.css">
</head>
<body>
  <div class="container">
    <div class="logo"><img src="img/logo_prospect.png" alt="Prospect Boxing Logo"></div>
    <h2 style="text-align:center; margin-bottom:24px;">Контакты Prospect Boxing</h2>
    <div class="person-list">
      {people}
    </div>
  </div>
</body>
</html>
"""

# Список людей с QR в index
people_list = ""

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

    # --- Генерируем QR (ссылку на файл, для GitHub Pages)
    qr_url = f"https://kyznetsovserega.github.io/prospectboxing-cards/{page_name}"
    qr_img = qrcode.make(qr_url)
    qr_path = QR_DIR / f"qr_{p['id']}.png"
    qr_img.save(qr_path)

    # --- Добавляем в список для index
    people_list += f"""
    <div class="person-item">
      <img class="qr-thumb" src="qrcodes/qr_{p['id']}.png" alt="QR {p['name']}">
      <a class="person-link" href="person_{p['id']}.html">{p['name']}</a>
    </div>
    """

# --- Генерируем index.html
index_html = index_template.format(people=people_list)
with open(OUTPUT / "index.html", "w", encoding="utf-8") as f:
    f.write(index_html)

print("Готово! Персональные страницы, index и QR-коды сгенерированы.")
