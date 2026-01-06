# BalansAI.uz - Rasmiy Veb-Sayt

BalansAI.uz - Balans AI loyihasining rasmiy, professional va ishonchli veb-sayti.

## Texnologiyalar

### Frontend
- HTML5
- Tailwind CSS
- JavaScript (minimal)

### Backend
- Python Flask
- Jinja2 Template Engine

### Database
- MySQL

## Xususiyatlar

### Public Sahifalar
- **Bosh sahifa** - Hero, Features, Pricing preview, FAQ, CTA
- **Haqida** - Balans AI haqida to'liq ma'lumot
- **Imkoniyatlar** - Barcha imkoniyatlar batafsil
- **Tariflar** - Free, Basic, Premium tariflar
- **FAQ** - Tez-tez beriladigan savollar
- **Aloqa** - Kontakt forma va bog'lanish

### Admin Panel
- **Dashboard** - Umumiy statistika
- **Foydalanuvchilar** - Foydalanuvchilarni boshqarish
- **Daromadlar** - To'lovlar va statistika
- **Xabarlar** - Kontakt formadan xabarlar
- **Sozlamalar** - Sayt sozlamalari

### SEO
- Semantic HTML
- Meta tags
- OpenGraph
- Sitemap.xml
- Robots.txt
- Optimized performance

## O'rnatish

### 1. Repository clone qilish

```bash
git clone https://github.com/your-username/balansai.uz.git
cd balansai.uz
```

### 2. Virtual environment yaratish

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# yoki
venv\Scripts\activate  # Windows
```

### 3. Dependencies o'rnatish

```bash
pip install -r requirements.txt
```

### 4. Environment variables sozlash

`.env.example` faylini `.env` ga nusxalang va sozlang:

```bash
cp .env.example .env
```

`.env` faylini tahrirlang:

```
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=your-secret-key-here

DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=balansai

ADMIN_USERNAME=admin
ADMIN_PASSWORD=your_secure_password

CONTACT_EMAIL=info@balansai.uz
```

### 5. Database yaratish

MySQL da database yarating va init_db.sql ni import qiling:

```bash
mysql -u root -p < init_db.sql
```

### 6. Serverni ishga tushirish

```bash
flask run
# yoki
python app.py
```

Sayt `http://localhost:5000` da ochiladi.

## Admin Panel

Admin panelga kirish:
- URL: `http://localhost:5000/admin/login`
- Username: `.env` fayldagi `ADMIN_USERNAME`
- Password: `.env` fayldagi `ADMIN_PASSWORD`

## Fayl Strukturasi

```
balansai.uz/
├── app.py                  # Asosiy Flask application
├── requirements.txt        # Python dependencies
├── init_db.sql            # Database schema
├── .env.example           # Environment variables template
├── README.md              # Bu fayl
│
├── static/
│   ├── css/
│   │   └── main.css       # Custom CSS
│   ├── js/
│   │   └── main.js        # Custom JavaScript
│   └── images/            # Rasmlar
│
├── templates/
│   ├── base.html          # Base template
│   ├── 404.html           # 404 error page
│   ├── 500.html           # 500 error page
│   ├── sitemap.xml        # Sitemap template
│   │
│   ├── components/
│   │   ├── navbar.html
│   │   └── footer.html
│   │
│   ├── pages/
│   │   ├── index.html
│   │   ├── about.html
│   │   ├── features.html
│   │   ├── pricing.html
│   │   ├── faq.html
│   │   └── contact.html
│   │
│   └── admin/
│       ├── base.html
│       ├── login.html
│       ├── dashboard.html
│       ├── users.html
│       ├── revenue.html
│       ├── contacts.html
│       └── settings.html
```

## Xavfsizlik

- Environment variables orqali maxfiy ma'lumotlar
- Session-based authentication
- CSRF protection
- Password hashing (production uchun Werkzeug)
- SQL injection prevention

## Production uchun tavsiyalar

1. **SECRET_KEY ni o'zgartiring** - kuchli, random key ishlating
2. **FLASK_ENV=production** qiling
3. **Admin parolni o'zgartiring** - kuchli parol ishlating
4. **SSL sertifikati** o'rnating (HTTPS)
5. **Gunicorn/uWSGI** ishlatib production serverda deploy qiling
6. **Nginx** reverse proxy sifatida sozlang
7. **Database backup** strategiyasini o'rnating

## Production Deploy

### Gunicorn bilan

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Nginx konfiguratsiya

```nginx
server {
    listen 80;
    server_name balansai.uz www.balansai.uz;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /static {
        alias /path/to/balansai.uz/static;
    }
}
```

## Texnik Yordam

- Email: info@balansai.uz
- Telegram: @balansai

## License

© 2025 BalansAI.uz. Barcha huquqlar himoyalangan.
