
# ProspectBoxing Cards

Генератор персональных контактных карточек для команды Prospect Boxing с красивым web-интерфейсом и индивидуальными QR-кодами.

## О проекте

- Автоматическая генерация HTML-страниц профилей для участников команды.
- На каждой странице:
  - Логотип, имя, контакты 
  - Индивидуальный QR-код для перехода на страницу.
  - Адаптивный дизайн для десктопа и мобильных.
  - Цветные иконки VK, WhatsApp, email.
  - Кастомный favicon.
  - Превью сайта (если изображение присутствует).
- Вся генерация выполняется автоматически на Python.

## Быстрый старт

1. **Клонируй репозиторий:**
   ```sh
   git clone https://github.com/kyznetsovserega/prospectboxing-cards.git
   cd prospectboxing-cards
   ```

2. **Создай виртуальное окружение и активируй его:**
   ```sh
   python -m venv .venv
   # Windows:
   .venv\Scripts\activate
   # Linux/Mac:
   source .venv/bin/activate
   ```

3. **Установи зависимости:**
   ```sh
   pip install -r requirements.txt
   ```

4. **Запусти генератор:**
   ```sh
   python generate_all.py
   ```

5. **Открой готовые HTML-страницы:**
   - Все сгенерированные файлы находятся в папке `docs`.
   - Открой `docs/index.html` в браузере, чтобы посмотреть каталог контактов.

## Структура проекта

```
prospectboxing-cards/
│
├── docs/                 # Готовые HTML-страницы и ресурсы для публикации на GitHub Pages
│   ├── css/
│   ├── icons/
│   ├── img/
│   ├── qrcodes/
│   ├── index.html
│   └── person_*.html
│
├── icons_svg/            # Исходные SVG-иконки для копирования
├── contacts.json         # Основной файл с данными участников
├── favicon.ico           # Фавикон проекта
├── generate_all.py       # Основной скрипт-генератор
├── logo_prospect.png     # Логотип Prospect Boxing
├── preview_website.jpg   # Превью сайта для блока "Сайт" (опционально)
├── requirements.txt
├── README.md
└── .gitignore
```

## Примечания

- QR-коды сохраняются в SVG-формате.
- Для favicon используется файл `favicon.ico` (автоматически копируется во все страницы).
- Если для сайта есть картинка `preview_website.jpg`, она будет использоваться как превью.

---

## Лицензия

Проект создан для внутренних целей Prospect Boxing. Использование кода возможно с указанием автора.

---

**Вопросы, баги или предложения — пиши в [Issues](https://github.com/kyznetsovserega/prospectboxing-cards/issues) проекта!**
