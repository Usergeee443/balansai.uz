# Render.com ga Deploy Qilish Bo'yicha Qo'llanma

## O'zgartirilgan Fayllar

1. **requirements.txt** - Gunicorn production server qo'shildi
2. **app.py** - PORT environment variable va production sozlamalari qo'shildi
3. **render.yaml** - Render.com konfiguratsiya fayli yaratildi

## Render.com da Deploy Qilish

### 1-Qadam: Render.com ga Kirish

1. [Render.com](https://render.com) saytiga kiring
2. GitHub akkauntingiz bilan sign in qiling

### 2-Qadam: Yangi Web Service Yaratish

1. Dashboard da **"New +"** tugmasini bosing
2. **"Web Service"** ni tanlang
3. GitHub repository sini ulang (balansai.uz)
4. Branch ni tanlang: `claude/prepare-render-deployment-P92rg`

### 3-Qadam: Service Sozlamalarini To'ldirish

Render avtomatik ravishda `render.yaml` faylini o'qiydi, lekin quyidagi sozlamalarni tekshiring:

- **Name**: balansai-uz
- **Runtime**: Python
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn app:app`

### 4-Qadam: MySQL Database Yaratish

1. Dashboard da **"New +"** tugmasini bosing
2. **"PostgreSQL"** ni tanlang (Render MySQL taqdim etmaydi, PostgreSQL ishlatishingiz kerak)

   **MUHIM**: Loyihangiz MySQL ishlatadi. Siz quyidagi variantlardan birini tanlashingiz kerak:

   **Variant A: PostgreSQL ga o'tish (Tavsiya etiladi)**
   - Render da PostgreSQL yarating
   - `requirements.txt` da `Flask-MySQLdb` va `mysqlclient` o'rniga quyidagilarni qo'shing:
     ```
     psycopg2-binary==2.9.9
     Flask-SQLAlchemy==3.1.1
     ```
   - `app.py` da database konfiguratsiyasini o'zgartiring

   **Variant B: Tashqi MySQL Service Ishlatish**
   - [PlanetScale](https://planetscale.com) (bepul tarif bor)
   - [Railway](https://railway.app) (MySQL taqdim etadi)
   - Yoki boshqa MySQL hosting providerlaridan foydalaning

### 5-Qadam: Environment Variables Sozlash

Render Dashboard da **Environment Variables** bo'limida quyidagilarni qo'shing:

```
FLASK_ENV=production
SECRET_KEY=<kuchli-random-key-yarating>
DB_HOST=<database-host>
DB_USER=<database-user>
DB_PASSWORD=<database-password>
DB_NAME=balansai
ADMIN_USERNAME=<admin-username>
ADMIN_PASSWORD=<kuchli-parol>
CONTACT_EMAIL=info@balansai.uz
```

**SECRET_KEY yaratish:**
```python
import secrets
print(secrets.token_hex(32))
```

### 6-Qadam: Database ni Boshlang'ich Holatga Keltirish

Database yaratilgandan keyin, Render shell orqali SQL ni import qiling:

1. Render Dashboard da service ni oching
2. **"Shell"** tab ni tanlang
3. Database ga ulanish va `init_db.sql` ni import qilish

### 7-Qadam: Deploy Qilish

1. **"Create Web Service"** tugmasini bosing
2. Render avtomatik ravishda deploy qilishni boshlaydi
3. Build va deploy jarayonini kuzating

### 8-Qadam: Domain Sozlash (Ixtiyoriy)

1. Deploy muvaffaqiyatli bo'lgandan keyin, Render sizga URL beradi: `https://balansai-uz.onrender.com`
2. O'z domeningizni ulash uchun:
   - Render Dashboard da **"Settings"** > **"Custom Domain"**
   - Domeningizni qo'shing: `balansai.uz`
   - DNS sozlamalaringizda CNAME record yarating

## Production Checklist

- [ ] SECRET_KEY kuchli random qiymatga o'rnatilgan
- [ ] FLASK_ENV=production o'rnatilgan
- [ ] Database yaratilgan va init_db.sql import qilingan
- [ ] Barcha environment variables to'g'ri sozlangan
- [ ] Admin parol kuchli parolga o'zgartirilgan
- [ ] SSL/HTTPS avtomatik yoqilgan (Render tomonidan)
- [ ] Custom domain sozlangan (agar kerak bo'lsa)

## Muammolarni Hal Qilish

### Database Connection Error
- Database host, user, password to'g'ri ekanligini tekshiring
- Database service ishlab turishini tekshiring
- Render Logs ni ko'rib chiqing

### Build Failed
- `requirements.txt` faylidagi dependencies ni tekshiring
- Python versiyasi mos ekanligini tekshiring (3.11)

### Application Error
- Environment variables to'g'ri sozlanganligini tekshiring
- Render Logs dan xatoliklarni o'qing
- Database connection stringini tekshiring

## Foydali Linklar

- [Render Docs](https://render.com/docs)
- [Python on Render](https://render.com/docs/deploy-flask)
- [Environment Variables](https://render.com/docs/environment-variables)

## Qo'shimcha Yordam

Agar qiyinchiliklar bo'lsa, Render Support ga murojaat qiling yoki loyiha README.md faylini o'qing.

---

© 2025 BalansAI.uz. Barcha huquqlar himoyalangan.
