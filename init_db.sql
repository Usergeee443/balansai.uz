-- BalansAI Database Schema

CREATE DATABASE IF NOT EXISTS balansai CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE balansai;

-- Users table
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    phone VARCHAR(50),
    plan_type ENUM('free', 'basic', 'premium') DEFAULT 'free',
    is_active BOOLEAN DEFAULT 1,
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
