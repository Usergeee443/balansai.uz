-- BalansAI Database Schema

CREATE DATABASE IF NOT EXISTS balansai CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE balansai;

-- Users table
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255),
    phone VARCHAR(50),
    company VARCHAR(255),
    plan_type ENUM('free', 'basic', 'premium') DEFAULT 'free',
    is_active BOOLEAN DEFAULT 1,
    email_verified BOOLEAN DEFAULT 0,
    last_login DATETIME,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_email (email),
    INDEX idx_plan (plan_type),
    INDEX idx_active (is_active)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Payments table
CREATE TABLE IF NOT EXISTS payments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    amount DECIMAL(10, 2) NOT NULL,
    plan_type VARCHAR(50) NOT NULL,
    payment_method VARCHAR(50),
    status ENUM('pending', 'completed', 'failed', 'refunded') DEFAULT 'pending',
    transaction_id VARCHAR(255),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user (user_id),
    INDEX idx_status (status),
    INDEX idx_date (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Contacts table
CREATE TABLE IF NOT EXISTS contacts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    message TEXT NOT NULL,
    is_read BOOLEAN DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_read (is_read),
    INDEX idx_date (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Settings table
CREATE TABLE IF NOT EXISTS settings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    key_name VARCHAR(100) UNIQUE NOT NULL,
    value TEXT,
    description VARCHAR(255),
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_key (key_name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Blog posts table
CREATE TABLE IF NOT EXISTS blog_posts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    slug VARCHAR(255) UNIQUE NOT NULL,
    excerpt TEXT,
    content TEXT NOT NULL,
    image_url VARCHAR(500),
    author VARCHAR(255) DEFAULT 'BalansAI Team',
    category VARCHAR(100),
    tags VARCHAR(255),
    is_published BOOLEAN DEFAULT 0,
    views INT DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    published_at DATETIME,
    INDEX idx_slug (slug),
    INDEX idx_published (is_published),
    INDEX idx_category (category),
    INDEX idx_date (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Testimonials table
CREATE TABLE IF NOT EXISTS testimonials (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    position VARCHAR(255),
    company VARCHAR(255),
    content TEXT NOT NULL,
    rating INT DEFAULT 5,
    avatar_url VARCHAR(500),
    is_active BOOLEAN DEFAULT 1,
    display_order INT DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_active (is_active),
    INDEX idx_order (display_order)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- User conversations table (for AI assistant)
CREATE TABLE IF NOT EXISTS conversations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    title VARCHAR(255),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user (user_id),
    INDEX idx_date (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Chat messages table
CREATE TABLE IF NOT EXISTS messages (
    id INT AUTO_INCREMENT PRIMARY KEY,
    conversation_id INT NOT NULL,
    role ENUM('user', 'assistant') NOT NULL,
    content TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (conversation_id) REFERENCES conversations(id) ON DELETE CASCADE,
    INDEX idx_conversation (conversation_id),
    INDEX idx_date (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Password reset tokens table
CREATE TABLE IF NOT EXISTS password_resets (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    token VARCHAR(255) NOT NULL,
    expires_at DATETIME NOT NULL,
    used BOOLEAN DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_token (token),
    INDEX idx_user (user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Insert default settings
INSERT INTO settings (key_name, value, description) VALUES
('site_title', 'BalansAI.uz', 'Sayt nomi'),
('site_description', 'AI yordamchi biznesingiz uchun', 'Sayt tavsifi'),
('free_plan_price', '0', 'Free tarif narxi'),
('basic_plan_price', '99000', 'Basic tarif narxi'),
('premium_plan_price', '299000', 'Premium tarif narxi'),
('contact_email', 'info@balansai.uz', 'Kontakt email'),
('telegram_link', 'https://t.me/balansai', 'Telegram link'),
('phone_number', '+998 90 123 45 67', 'Telefon raqam')
ON DUPLICATE KEY UPDATE value=value;

-- Insert demo data
INSERT INTO users (full_name, email, phone, plan_type, is_active) VALUES
('Test User', 'test@balansai.uz', '+998901234567', 'free', 1),
('Premium User', 'premium@balansai.uz', '+998901234568', 'premium', 1),
('Basic User', 'basic@balansai.uz', '+998901234569', 'basic', 1)
ON DUPLICATE KEY UPDATE email=email;

INSERT INTO payments (user_id, amount, plan_type, payment_method, status) VALUES
(2, 299000, 'premium', 'payme', 'completed'),
(3, 99000, 'basic', 'click', 'completed')
ON DUPLICATE KEY UPDATE id=id;

-- Insert demo blog posts
INSERT INTO blog_posts (title, slug, excerpt, content, category, tags, is_published, published_at) VALUES
('Sun\'iy intellekt biznesda: 2026 yil tendensiyalari',
 'suniy-intellekt-biznesda-2026',
 'Sun\'iy intellekt texnologiyalari biznes jarayonlarini qanday o\'zgartirmoqda va kelajakda qanday imkoniyatlar yaratadi.',
 '<h2>Sun\'iy intellekt - biznesning kelajagi</h2><p>2026 yilda sun\'iy intellekt texnologiyalari biznes dunyosida yanada keng qo\'llanilmoqda. BalansAI kabi platformalar orqali kichik va o\'rta bizneslar ham yuqori texnologiyalardan foydalanish imkoniyatiga ega bo\'lmoqda.</p><h3>Asosiy tendensiyalar:</h3><ul><li>Moliyaviy hisobotlarni avtomatlashtirish</li><li>Bashoratli tahlillar</li><li>Real vaqtda biznes ko\'rsatkichlarini monitoring qilish</li><li>Avtomatlashtirilgan maslahatlar</li></ul><p>BalansAI sizning biznesingizni raqamli davrda muvaffaqiyatga olib boradi.</p>',
 'Yangiliklar',
 'AI,Biznes,Texnologiya',
 1,
 NOW()),

('Moliyaviy hisobotlarni avtomatlashtirish: Vaqtingizni tejang',
 'moliyaviy-hisobotlarni-avtomatlashtirish',
 'Qo\'lda kiritish o\'rniga, BalansAI yordamida moliyaviy hisobotlarni avtomatik tarzda yarating.',
 '<h2>Vaqtingiz - eng qimmatli resurs</h2><p>Tadbirkorlar uchun vaqt eng muhim resurs hisoblanadi. Moliyaviy hisobotlarni tayyorlash ko\'p vaqt va kuch talab qiladi. BalansAI bu jarayonni 10 barobar tezlashtiradi.</p><h3>BalansAI bilan:</h3><ul><li>Bir necha daqiqada to\'liq hisobot</li><li>Xatolarsiz hisob-kitoblar</li><li>Har qanday vaqtda ma\'lumotlarga kirish</li><li>Professional ko\'rinishdagi hisobotlar</li></ul><p>Biznesingizni rivojlantirishga e\'tibor qarating, qolganini BalansAI qiladi.</p>',
 'Qo\'llanma',
 'Avtomatlashtirish,Moliya,Hisobotlar',
 1,
 NOW()),

('Kichik biznes uchun AI: Qanday boshlash kerak?',
 'kichik-biznes-uchun-ai',
 'Sun\'iy intellekt faqat yirik korporatsiyalar uchunmi? Yo\'q! Kichik bizneslar ham AI dan foydalanishi mumkin.',
 '<h2>AI hamma uchun ochiq</h2><p>Ko\'p tadbirkorlar sun\'iy intellekt texnologiyalarini faqat yirik kompaniyalar uchun deb o\'ylashadi. Ammo bugungi kunda BalansAI kabi platformalar orqali har qanday biznes AI dan foydalanishi mumkin.</p><h3>Qanday boshlash kerak:</h3><ol><li>BalansAI.uz saytida ro\'yxatdan o\'ting</li><li>Biznes ma\'lumotlaringizni kiriting</li><li>AI yordamchi bilan suhbatni boshlang</li><li>Tahlillar va tavsiyalarni oling</li></ol><p>Bepul rejadan boshlab, keyin biznesingiz o\'sib borar ekan, Premium rejaga o\'ting.</p>',
 'Qo\'llanma',
 'Kichik biznes,AI,Boshlang\'ich',
 1,
 NOW())
ON DUPLICATE KEY UPDATE slug=slug;

-- Insert demo testimonials
INSERT INTO testimonials (name, position, company, content, rating, display_order, is_active) VALUES
('Aziz Karimov', 'Asoschisi', 'TechStart.uz', 'BalansAI biznesimizni boshqarishni ancha osonlashtirdi. Hozir moliyaviy hisobotlarni bir necha daqiqada tayyorlaymiz. Juda qulay va samarali!', 5, 1, 1),
('Dilnoza Rahimova', 'Moliya direktori', 'SmartRetail', 'AI yordamchi har doim yordam berishga tayyor. Murakkab moliyaviy savollarimga aniq javoblar beradi. Jamoamizning samaradorligi 40% oshdi.', 5, 2, 1),
('Jamshid Tursunov', 'Tadbirkor', 'FoodExpress', 'Premium rejaga o\'tganidan keyin biznesimning barcha ko\'rsatkichlarini real vaqtda kuzatib boraman. Bu juda katta ustunlik!', 5, 3, 1),
('Nodira Alimova', 'Bosh direktor', 'BeautyStyle', 'BalansAI bilan ishlash juda qulay. Interfeysi tushunarli, xizmat ko\'rsatish a\'lo darajada. Tavsiya qilaman!', 5, 4, 1),
('Rustam Yusupov', 'Asoschisi', 'LogistPro', 'Avval moliyaviy hisobotlarni tayyorlash uchun buxgalter yollagan edim. Hozir BalansAI bilan hammasi avtomatik. Xarajatlar ham kamaydi!', 5, 5, 1),
('Zarina Ismoilova', 'Marketing direktori', 'DigitalAgency', 'AI tahlillar bizga to\'g\'ri qarorlar qabul qilishda yordam beradi. Biznes strategiyamizni yanada yaxshiladik.', 5, 6, 1)
ON DUPLICATE KEY UPDATE name=name;
