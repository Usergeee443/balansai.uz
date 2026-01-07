# 3D Rasmlar va Iconlar Qo'llanmasi

Bu fayl sizning 3D rasmlar va iconlaringizni qayerga joylashtirish kerakligini tushuntiradi.

## 📁 3D Rasmlar Joylashuvi

Barcha 3D rasmlar va iconlarni `static/images/3d/` papkasiga joylashtirishingiz mumkin.

## 🎨 3D Icon Joylar (Placeholders)

Saytda quyidagi joylarda 3D icon/rasm uchun joylar tayyorlangan:

### 1. **Hero Section** (Bosh sahifa yuqorisi)
- **Fayl**: `templates/pages/index.html` (34-42 qator)
- **O'lchami**: 300x300px (ideal)
- **Tavsiya**: Asosiy AI yordamchi yoki biznes grafika
- **CSS class**: `.icon-3d`

### 2. **Value Proposition Cards** (3 ta karta)
- **Fayl**: `templates/pages/index.html` (76-107 qator)
- **O'lchami**: 96x96px har biri (w-24 h-24)
- **Soni**: 3 ta icon
- **Tavsiya**:
  1. Tezlik/avtomatlashtirish iconi
  2. Xavfsizlik/himoya iconi
  3. Tahlil/statistika iconi
- **CSS class**: `.float-3d`

### 3. **Features Section Icons** (4 ta kichik icon)
- **Fayl**: `templates/pages/index.html` (129-178 qator)
- **O'lchami**: 64x64px har biri (w-16 h-16)
- **Soni**: 4 ta icon
- **Tavsiya**:
  1. AI yordamchi iconi
  2. Biznes tahlil iconi
  3. Moliyaviy rejalashtirish iconi
  4. Real-time statistika iconi
- **CSS class**: `.float-3d`

### 4. **Features Section - Katta Rasm**
- **Fayl**: `templates/pages/index.html` (182-209 qator)
- **O'lchami**: 800x450px (aspect-video)
- **Tavsiya**: Dashboard screenshot yoki 3D visualization
- **CSS class**: `.image-zoom`

### 5. **How It Works Steps** (3 ta qadam)
- **Fayl**: `templates/pages/index.html` (230-269 qator)
- **O'lchami**: 128x128px har biri (w-32 h-32)
- **Soni**: 3 ta icon
- **Tavsiya**:
  1. Ro'yxatdan o'tish iconi
  2. Ma'lumot kiritish iconi
  3. AI dan foydalanish iconi
- **CSS class**: `.float-3d`

### 6. **CTA Section - Kichik Iconlar** (3 ta)
- **Fayl**: `templates/pages/index.html` (450-471 qator)
- **O'lchami**: 80x80px har biri (w-20 h-20)
- **Soni**: 3 ta icon
- **Tavsiya**: Asosiy xususiyatlar iconi
- **CSS class**: `.float-3d`

## 🔧 3D Rasmlarni Qo'shish

### HTML dagi placeholder kodni almashtiring:

**Eski kod (placeholder):**
```html
<div class="icon-3d float-3d shimmer-3d">
    <div class="text-white text-center p-8">
        <svg class="w-32 h-32 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <!-- SVG path -->
        </svg>
        <p class="text-lg font-bold">3D Icon Joy</p>
    </div>
</div>
```

**Yangi kod (3D rasm bilan):**
```html
<div class="icon-3d float-3d">
    <img src="{{ url_for('static', filename='images/3d/hero-icon.png') }}"
         alt="AI Yordamchi"
         class="w-full h-full object-contain p-8">
</div>
```

## 🎭 CSS Animation Classlar

Barcha 3D elementlar uchun quyidagi animation classlar mavjud:

- `.float-3d` - Floating 3D animation
- `.icon-3d` - 3D transform effects on hover
- `.shimmer-3d` - Shimmer loading effect
- `.reveal-scale` - Scale reveal on scroll
- `.reveal-rotate` - Rotate reveal on scroll
- `.reveal-slide-left/right` - Slide reveal from left/right
- `.image-zoom` - Zoom effect on scroll

## 📐 Tavsiya Etiladigan Format

- **Format**: PNG yoki WebP (transparency bilan)
- **Background**: Transparent (shaffof)
- **O'lcham**: Yuqorida ko'rsatilgan o'lchamlar
- **Rangli**: Sizning 3D rasmlaringizga mos
- **Optimized**: Web uchun optimizatsiya qilingan

## 🚀 Animatsiya Sozlamalari

JavaScript fayli (`static/js/main.js`) da quyidagi animatsiyalar avtomatik ishlaydi:

1. **Mouse Tracking** - 3D iconlar mouse harakatiga javob beradi
2. **Scroll Reveal** - Scroll qilganda animatsiya bilan ko'rinadi
3. **Float Animation** - Doimiy floating effekt
4. **Parallax** - Parallax scroll effekti
5. **Zoom on Scroll** - Scroll qilganda zoom effekti

## 📝 Eslatma

- Har bir placeholder `<!-- 3D Icon Placeholder -->` comment bilan belgilangan
- Rasmlarni qo'shganingizdan keyin, placeholder textni olib tashlashingiz mumkin
- CSS classlarni o'zgartirmasangiz, animatsiyalar avtomatik ishlaydi
- Agar rasmlar og'ir bo'lsa, WebP formatga o'zgartiring

## 🎨 Ranglar

Agar sizning 3D rasmlaringiz sayt ranglari bilan mos kelmasa, CSS da o'zgartirishingiz mumkin:

```css
--color-primary: #034f46 (dark green/teal)
--color-accent: #4d65ff (blue)
```

## 💡 Qo'shimcha Yordam

Agar qo'shimcha yordam kerak bo'lsa yoki animatsiyalarni sozlash kerak bo'lsa, HTML va CSS fayllarni tahrirlashingiz mumkin.

**Muvaffaqiyatlar!** 🎉
