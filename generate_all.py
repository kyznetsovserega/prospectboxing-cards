import qrcode
import json
from pathlib import Path

FOLDER = Path('.')
OUTPUT = FOLDER / 'qr_json'
OUTPUT.mkdir(exist_ok=True)

with open(FOLDER / 'contacts.json', encoding='utf-8') as f:
    people = json.load(f)

for p in people:
    # Кодируем JSON для одного сотрудника
    json_str = json.dumps(p, ensure_ascii=False, indent=None)
    img = qrcode.make(json_str)
    img.save(OUTPUT / f"qr_{p['id']}_json.png")
    print(f"Сохранено: qr_{p['id']}_json.png")

print("Готово! Все QR-коды (по одному на сотрудника, весь JSON) сохранены в папке qr_json/")
