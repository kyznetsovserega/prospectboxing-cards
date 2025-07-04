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
ICONS_SRC = BASE / "icons_svg"
ICONS_DST = OUTPUT / "icons"
LOGO_SRC = BASE / "logo_prospect.png"
LOGO = "img/logo_prospect.png"

# Создание папок
QR_DIR.mkdir(parents=True, exist_ok=True)
CSS_DIR.mkdir(parents=True, exist_ok=True)
IMG_DIR.mkdir(parents=True, exist_ok=True)
ICONS_DST.mkdir(parents=True, exist_ok=True)

# Копируем preview_website.jpg если он есть в корне
preview_global_src = BASE / "preview_website.jpg"
if preview_global_src.exists():
    shutil.copy(preview_global_src, IMG_DIR / "preview_website.jpg")

# Копируем логотип в docs/img
shutil.copy(LOGO_SRC, IMG_DIR / LOGO_SRC.name)

# Копируем все SVG-иконки (если есть)
icon_files = {
    "phone": "phone.svg",
    "whatsapp": "whatsapp.png",
    "vk": "vk.svg",
    "email": "email.svg",
    "website": "website.svg"
}
for icon_name, icon_file in icon_files.items():
    src = ICONS_SRC / icon_file
    dst = ICONS_DST / icon_file
    if src.exists():
        shutil.copy(src, dst)
    else:
        print(f"Внимание: {src} не найден!")

# --- CSS ---
style_css = """
body { background:#111; color:#fff; font-family:'Segoe UI',Arial,sans-serif; margin:0; }
.container { max-width:440px; margin:0 auto; padding:36px 12px 0 12px;}
.logo { display:flex; justify-content:center; }
.logo img { width:300px; max-width:90vw;}
.person-title { font-size:2em; font-weight:600; text-align:center; margin-bottom:28px;}
.contacts-list { margin-top:36px;}
.contact-block {
  display:flex;
  align-items:center;
  background:#1a1a1a;
  color:#fff;
  border-radius:14px;
  margin-bottom:22px;
  text-decoration:none;
  box-shadow:0 2px 10px #0004;
  min-height:64px;
  transition:box-shadow 0.2s;
}
.contact-block:hover { box-shadow:0 4px 16px #0009; background:#232323;}
.icon {
  width:54px;
  height:54px;
  margin:0 16px;
  border-radius:10px;
  background:#333;
  display:flex;
  align-items:center;
  justify-content:center;
  font-size:2em;
  padding: 0;
}
.icon img, .icon svg {
  width:100%;
  height:100%;
  max-width:100%;
  max-height:100%;
  object-fit:contain;
  display:block;
}
/* Индивидуальные цвета для популярных иконок (можно убрать, если нужны все серые) */
.icon.whatsapp { background: #25D366 !important; }
.icon.vk { background: #0077FF !important; }

.site-preview-block {display:flex;align-items:center;gap:16px; background:#1a1a1a; border-radius:14px; margin-bottom:22px; min-height:64px; box-shadow:0 2px 10px #0004;}
.site-preview-block:hover { box-shadow:0 4px 16px #0009; background:#232323;}
.site-preview-img {width:54px; height:54px; object-fit:cover; border-radius:10px; margin-left:16px;}
.site-preview-content {padding:8px 0;}
.site-preview-title {font-weight:600; font-size:1.09em;}
.site-preview-desc {opacity:0.77; font-size:0.95em;}
.contact-content { flex:1; min-width:0;}
.contact-title { font-size:1.09em; font-weight:600; margin-bottom:2px;}
.contact-desc { font-size:0.97em; opacity:0.77;}
.qr-thumb { width:46px; height:46px; object-fit:contain; border-radius:10px; background:#fff; margin-right:18px; box-shadow:0 2px 6px #0002;}
.person-list { margin-top:32px; }
.person-item { display:flex; align-items:center; background:#181818; border-radius:12px; margin-bottom:16px; padding:10px 18px; box-shadow:0 2px 10px #0004; transition:box-shadow 0.2s; }
.person-item:hover { box-shadow:0 4px 16px #0009; background:#232323;}
.person-link { color:#fff; text-decoration:none; font-size:1.09em; font-weight:500;}
/* --- Правим visited/underline для кнопок --- */
.contact-block, .contact-block:visited,
.site-preview-block, .site-preview-block:visited,
.contact-block *, .contact-block:visited *,
.site-preview-block *, .site-preview-block:visited * {
  color: #fff !important;
  text-decoration: none !important;
}
@media (max-width: 500px) {
  .container {padding: 18px 2vw 2vw;}
  .logo img {width: 150px;}
  .icon {width:36px; height:36px; margin:0 8px;}
  .icon img, .icon svg {width:100%; height:100%;}
  .qr-thumb {width:30px; height:30px; margin-right:10px;}
  .person-item {padding:7px 6px;}
  .site-preview-img {width:36px; height:36px;}
}
"""

with open(CSS_DIR / "style.css", "w", encoding="utf-8") as f:
    f.write(style_css)

# --- Загрузка контактов ---
with open(BASE / "contacts.json", encoding="utf-8") as f:
    people = json.load(f)

# --- HTML шаблоны ---
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

# --- Генерация персональных страниц и QR ---
people_list = ""
for p in people:
    blocks = ""
    # --- Телефон ---
    if p.get("phones"):
        for phone in p["phones"]:
            blocks += f"""
    <a class="contact-block" href="tel:+{phone}">
      <span class="icon"><img src="icons/phone.svg" alt="Phone"></span>
      <span class="contact-content">
        <div class="contact-title">Телефон</div>
        <div class="contact-desc">+{phone}</div>
      </span>
    </a>"""
    # --- WhatsApp ---
    if p.get("whatsapp"):
        for wa in p["whatsapp"]:
            blocks += f"""
    <a class="contact-block" href="https://wa.me/{wa}" target="_blank">
      <span class="icon"><img src="icons/whatsapp.png" alt="WhatsApp"></span>
      <span class="contact-content">
        <div class="contact-title">WhatsApp</div>
        <div class="contact-desc">+{wa}</div>
      </span>
    </a>"""
    # --- ВКонтакте ---
    if p.get("vk"):
        blocks += f"""
    <a class="contact-block" href="{p['vk']}" target="_blank">
      <span class="icon"><img src="icons/vk.svg" alt="VK"></span>
      <span class="contact-content">
        <div class="contact-title">ВКонтакте</div>
        <div class="contact-desc">{p['vk'].replace('https://vk.com/','vk.com/')}</div>
      </span>
    </a>"""
    # --- Email ---
    if p.get("email"):
        blocks += f"""
    <a class="contact-block" href="mailto:{p['email']}">
      <span class="icon"><img src="icons/email.svg" alt="Email"></span>
      <span class="contact-content">
        <div class="contact-title">Email</div>
        <div class="contact-desc">{p['email']}</div>
      </span>
    </a>"""
    # --- Сайт (preview_website.jpg или иконка, стиль всегда белый) ---
    site_url = str(p.get("site", "")).strip()
    if site_url:
        site_domain = site_url.replace('https://', '').replace('http://', '').replace('/', '')
        preview_jpg_global = IMG_DIR / "preview_website.jpg"
        if preview_jpg_global.exists():
            blocks += f"""
    <a class="site-preview-block" href="{site_url}" target="_blank">
      <img class="site-preview-img" src="img/preview_website.jpg" alt="Preview">
      <div class="site-preview-content">
        <div class="site-preview-title">Сайт</div>
        <div class="site-preview-desc">{site_domain}</div>
      </div>
    </a>"""
        else:
            blocks += f"""
    <a class="contact-block" href="{site_url}" target="_blank">
      <span class="icon"><img src="icons/website.svg" alt="Site"></span>
      <span class="contact-content">
        <div class="contact-title">Сайт</div>
        <div class="contact-desc">{site_domain}</div>
      </span>
    </a>"""

    # --- Сохраняем персональный HTML
    page_name = f"person_{p['id']}.html"
    html_out = html_template.format(name=p["name"], logo=LOGO, blocks=blocks)
    with open(OUTPUT / page_name, "w", encoding='utf-8') as f:
        f.write(html_out)

    # --- Генерируем QR (GitHub Pages)
    qr_url = f"https://kyznetsovserega.github.io/prospectboxing-cards/{page_name}"
    qr_img = qrcode.make(qr_url)
    qr_path = QR_DIR / f"qr_{p['id']}.png"
    qr_img.save(qr_path)

    # --- Для index
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

print("Готово! Все страницы, QR-коды, стили, превью и иконки скопированы и сгенерированы.")
