import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import json
from pathlib import Path
import re

BASE = Path(__file__).parent
IMG_DIR = BASE / 'docs' / 'img'
IMG_DIR.mkdir(parents=True, exist_ok=True)

with open(BASE / 'contacts.json', encoding='utf-8') as f:
    people = json.load(f)

PREVIEW_INFO = {}

def save_image(img_url, out_name):
    try:
        ext = img_url.split('.')[-1].split('?')[0]
        fname = f"{out_name}.{ext}"
        out_path = IMG_DIR / fname
        img_data = requests.get(img_url, timeout=10).content
        with open(out_path, 'wb') as fimg:
            fimg.write(img_data)
        print(f"  --> Картинка сохранена: img/{fname}")
        return f"img/{fname}"
    except Exception as ex:
        print(f"  !! Не удалось скачать изображение: {img_url} ({ex})")
        return None

for p in people:
    info = {"title": "", "desc": "", "image": None, "vk_image": None}
    # --- Сайт превью ---
    site_url = p.get('site')
    if site_url:
        print(f'Парсим сайт: {site_url} ...')
        try:
            r = requests.get(site_url, timeout=15)
            soup = BeautifulSoup(r.text, 'html.parser')
            title = (soup.find('meta', property='og:title') or soup.find('title'))
            title = title['content'] if title and title.has_attr('content') else (title.text if title else '')
            desc = soup.find('meta', property='og:description') or soup.find('meta', attrs={'name': 'description'})
            desc = desc['content'] if desc and desc.has_attr('content') else ''
            # Preview image
            img_url = None
            og_img = soup.find('meta', property='og:image')
            if og_img and og_img.has_attr('content'):
                img_url = og_img['content']
            else:
                first_img = soup.find('img')
                if first_img and first_img.has_attr('src'):
                    img_url = urljoin(site_url, first_img['src'])
            preview_path = None
            if img_url:
                preview_path = save_image(img_url, f"preview_{p['id']}")
            info['title'] = title.strip()
            info['desc'] = desc.strip()
            info['image'] = preview_path
        except Exception as e:
            print(f"  !! Ошибка парсинга сайта: {e}")

    # --- VK preview (аватар) ---
    vk_url = p.get('vk')
    if vk_url:
        print(f'Парсим VK: {vk_url}')
        try:
            vk_id = re.sub(r'^https?://(m\.)?vk\.com/', '', vk_url)
            r = requests.get(vk_url, timeout=15, headers={'User-Agent': 'Mozilla/5.0'})
            soup = BeautifulSoup(r.text, 'html.parser')
            img = None
            # Группы VK
            group_img = soup.find('img', {'class': re.compile(r'page_avatar_img|pi_text|im-page--photo|im-page--photo_img')})
            if not group_img:
                # Пробуем найти по другим классам
                imgs = soup.find_all('img')
                for i in imgs:
                    if i.has_attr('src') and ('ava' in i['src'] or 'camera' in i['src']):
                        group_img = i
                        break
            if group_img and group_img.has_attr('src'):
                img_url = group_img['src']
                vk_img_path = save_image(img_url, f"vk_{vk_id}")
                info['vk_image'] = vk_img_path
        except Exception as e:
            print(f"  !! Ошибка VK: {e}")

    # --- WhatsApp preview (не делаем, нет аватарок в публичном доступе) ---

    PREVIEW_INFO[p['id']] = info

# Сохраняем все превью в отдельный JSON
with open(BASE / 'preview_info.json', 'w', encoding='utf-8') as f:
    json.dump(PREVIEW_INFO, f, ensure_ascii=False, indent=2)

print('\nСобрано превью для всех сайтов и VK!')

