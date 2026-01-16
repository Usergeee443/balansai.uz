import os
import csv
import secrets
from io import StringIO
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify, make_response
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
from functools import wraps
import datetime
import re

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')

# MySQL Configuration
app.config['MYSQL_HOST'] = os.getenv('DB_HOST', 'localhost')
app.config['MYSQL_USER'] = os.getenv('DB_USER', 'root')
app.config['MYSQL_PASSWORD'] = os.getenv('DB_PASSWORD', '')
app.config['MYSQL_DB'] = os.getenv('DB_NAME', 'balansai')

mysql = MySQL(app)

# ============ DECORATORS ============

def admin_required(f):
    """Admin authentication decorator"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_logged_in' not in session:
            flash('Iltimos, avval tizimga kiring', 'error')
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function

def login_required(f):
    """User authentication decorator"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Iltimos, avval tizimga kiring', 'error')
            return redirect(url_for('user_login'))
        return f(*args, **kwargs)
    return decorated_function

# ============ HELPER FUNCTIONS ============

def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_password(password):
    """Validate password strength"""
    if len(password) < 8:
        return False, "Parol kamida 8 ta belgidan iborat bo'lishi kerak"
    if not re.search(r'[A-Z]', password):
        return False, "Parolda kamida bitta katta harf bo'lishi kerak"
    if not re.search(r'[a-z]', password):
        return False, "Parolda kamida bitta kichik harf bo'lishi kerak"
    if not re.search(r'\d', password):
        return False, "Parolda kamida bitta raqam bo'lishi kerak"
    return True, "OK"

def generate_slug(title):
    """Generate URL-friendly slug from title"""
    uzbek_chars = {
        'o\'': 'o', 'g\'': 'g', 'sh': 'sh', 'ch': 'ch',
        'ʻ': '', ''': '', '"': '', '"': ''
    }
    slug = title.lower()
    for uz, lat in uzbek_chars.items():
        slug = slug.replace(uz, lat)
    slug = re.sub(r'[^a-z0-9-]', '-', slug)
    slug = re.sub(r'-+', '-', slug)
    return slug.strip('-')

# ============ PUBLIC ROUTES ============

@app.route('/')
def index():
    """Bosh sahifa"""
    cursor = mysql.connection.cursor()

    # Get testimonials
    cursor.execute("""
        SELECT * FROM testimonials
        WHERE is_active = 1
        ORDER BY display_order ASC, created_at DESC
        LIMIT 6
    """)
    testimonials = cursor.fetchall()

    # Get latest blog posts
    cursor.execute("""
        SELECT * FROM blog_posts
        WHERE is_published = 1
        ORDER BY published_at DESC
        LIMIT 3
    """)
    blog_posts = cursor.fetchall()

    cursor.close()

    return render_template('pages/index.html',
                         testimonials=testimonials,
                         blog_posts=blog_posts)

@app.route('/about')
def about():
    """Biz haqimizda"""
    return render_template('pages/about.html')

@app.route('/features')
def features():
    """Imkoniyatlar"""
    return render_template('pages/features.html')

@app.route('/pricing')
def pricing():
    """Tariflar"""
    return render_template('pages/pricing.html')

@app.route('/faq')
def faq():
    """Tez-tez beriladigan savollar"""
    return render_template('pages/faq.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    """Aloqa"""
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        message = request.form.get('message', '').strip()

        # Validation
        if not name or not email or not message:
            flash('Barcha maydonlarni to\'ldiring', 'error')
            return redirect(url_for('contact'))

        if not validate_email(email):
            flash('Email manzil noto\'g\'ri', 'error')
            return redirect(url_for('contact'))

        # Save to database
        cursor = mysql.connection.cursor()
        cursor.execute(
            "INSERT INTO contacts (name, email, message, created_at) VALUES (%s, %s, %s, %s)",
            (name, email, message, datetime.datetime.now())
        )
        mysql.connection.commit()
        cursor.close()

        flash('Xabaringiz muvaffaqiyatli yuborildi! Tez orada siz bilan bog\'lanamiz.', 'success')
        return redirect(url_for('contact'))

    return render_template('pages/contact.html')

# ============ BLOG ROUTES ============

@app.route('/blog')
def blog():
    """Blog listing"""
    page = request.args.get('page', 1, type=int)
    per_page = 9
    category = request.args.get('category', '')

    cursor = mysql.connection.cursor()

    # Build query
    if category:
        cursor.execute("""
            SELECT COUNT(*) FROM blog_posts
            WHERE is_published = 1 AND category = %s
        """, (category,))
    else:
        cursor.execute("SELECT COUNT(*) FROM blog_posts WHERE is_published = 1")

    total = cursor.fetchone()[0]
    total_pages = (total + per_page - 1) // per_page
    offset = (page - 1) * per_page

    # Get posts
    if category:
        cursor.execute("""
            SELECT * FROM blog_posts
            WHERE is_published = 1 AND category = %s
            ORDER BY published_at DESC
            LIMIT %s OFFSET %s
        """, (category, per_page, offset))
    else:
        cursor.execute("""
            SELECT * FROM blog_posts
            WHERE is_published = 1
            ORDER BY published_at DESC
            LIMIT %s OFFSET %s
        """, (per_page, offset))

    posts = cursor.fetchall()

    # Get categories
    cursor.execute("""
        SELECT DISTINCT category FROM blog_posts
        WHERE is_published = 1 AND category IS NOT NULL
    """)
    categories = [row[0] for row in cursor.fetchall()]

    cursor.close()

    return render_template('pages/blog.html',
                         posts=posts,
                         categories=categories,
                         current_category=category,
                         page=page,
                         total_pages=total_pages)

@app.route('/blog/<slug>')
def blog_post(slug):
    """Single blog post"""
    cursor = mysql.connection.cursor()

    # Get post
    cursor.execute("""
        SELECT * FROM blog_posts
        WHERE slug = %s AND is_published = 1
    """, (slug,))
    post = cursor.fetchone()

    if not post:
        cursor.close()
        return render_template('404.html'), 404

    # Increment views
    cursor.execute("UPDATE blog_posts SET views = views + 1 WHERE id = %s", (post[0],))
    mysql.connection.commit()

    # Get related posts
    cursor.execute("""
        SELECT * FROM blog_posts
        WHERE is_published = 1 AND id != %s AND category = %s
        ORDER BY published_at DESC
        LIMIT 3
    """, (post[0], post[7]))
    related_posts = cursor.fetchall()

    cursor.close()

    return render_template('pages/blog_post.html', post=post, related_posts=related_posts)

# ============ LEGAL PAGES ============

@app.route('/terms')
def terms():
    """Foydalanish shartlari"""
    return render_template('pages/terms.html')

@app.route('/privacy')
def privacy():
    """Maxfiylik siyosati"""
    return render_template('pages/privacy.html')

# ============ USER AUTHENTICATION ============

@app.route('/register', methods=['GET', 'POST'])
def user_register():
    """Foydalanuvchi ro'yxatdan o'tishi"""
    if 'user_id' in session:
        return redirect(url_for('user_dashboard'))

    if request.method == 'POST':
        full_name = request.form.get('full_name', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        phone = request.form.get('phone', '').strip()
        company = request.form.get('company', '').strip()

        # Validation
        if not full_name or not email or not password:
            flash('Barcha majburiy maydonlarni to\'ldiring', 'error')
            return redirect(url_for('user_register'))

        if not validate_email(email):
            flash('Email manzil noto\'g\'ri', 'error')
            return redirect(url_for('user_register'))

        if password != confirm_password:
            flash('Parollar mos kelmadi', 'error')
            return redirect(url_for('user_register'))

        is_valid, msg = validate_password(password)
        if not is_valid:
            flash(msg, 'error')
            return redirect(url_for('user_register'))

        # Check if email exists
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
        if cursor.fetchone():
            cursor.close()
            flash('Bu email manzil allaqachon ro\'yxatdan o\'tgan', 'error')
            return redirect(url_for('user_register'))

        # Create user
        hashed_password = generate_password_hash(password)
        cursor.execute("""
            INSERT INTO users (full_name, email, password, phone, company, created_at)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (full_name, email, hashed_password, phone, company, datetime.datetime.now()))
        mysql.connection.commit()
        user_id = cursor.lastrowid
        cursor.close()

        # Login user
        session['user_id'] = user_id
        session['user_name'] = full_name
        session['user_email'] = email

        flash('Ro\'yxatdan muvaffaqiyatli o\'tdingiz!', 'success')
        return redirect(url_for('user_dashboard'))

    return render_template('pages/register.html')

@app.route('/login', methods=['GET', 'POST'])
def user_login():
    """Foydalanuvchi tizimga kirishi"""
    if 'user_id' in session:
        return redirect(url_for('user_dashboard'))

    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')

        if not email or not password:
            flash('Email va parolni kiriting', 'error')
            return redirect(url_for('user_login'))

        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()

        if user and user[3] and check_password_hash(user[3], password):
            # Check if active
            if not user[7]:
                flash('Hisobingiz bloklangan. Iltimos, administrator bilan bog\'laning', 'error')
                cursor.close()
                return redirect(url_for('user_login'))

            # Update last login
            cursor.execute("UPDATE users SET last_login = %s WHERE id = %s",
                         (datetime.datetime.now(), user[0]))
            mysql.connection.commit()

            # Set session
            session['user_id'] = user[0]
            session['user_name'] = user[1]
            session['user_email'] = user[2]
            session['user_plan'] = user[6]

            cursor.close()
            flash('Xush kelibsiz!', 'success')
            return redirect(url_for('user_dashboard'))
        else:
            cursor.close()
            flash('Email yoki parol noto\'g\'ri', 'error')
            return redirect(url_for('user_login'))

    return render_template('pages/login.html')

@app.route('/logout')
def user_logout():
    """Foydalanuvchi tizimdan chiqishi"""
    session.clear()
    flash('Tizimdan chiqdingiz', 'info')
    return redirect(url_for('index'))

# ============ USER DASHBOARD ============

@app.route('/dashboard')
@login_required
def user_dashboard():
    """Foydalanuvchi paneli"""
    cursor = mysql.connection.cursor()

    # Get user info
    cursor.execute("SELECT * FROM users WHERE id = %s", (session['user_id'],))
    user = cursor.fetchone()

    # Get conversations
    cursor.execute("""
        SELECT * FROM conversations
        WHERE user_id = %s
        ORDER BY updated_at DESC
        LIMIT 10
    """, (session['user_id'],))
    conversations = cursor.fetchall()

    # Get recent payments
    cursor.execute("""
        SELECT * FROM payments
        WHERE user_id = %s
        ORDER BY created_at DESC
        LIMIT 5
    """, (session['user_id'],))
    payments = cursor.fetchall()

    cursor.close()

    return render_template('pages/dashboard.html',
                         user=user,
                         conversations=conversations,
                         payments=payments)

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def user_profile():
    """Foydalanuvchi profili"""
    cursor = mysql.connection.cursor()

    if request.method == 'POST':
        full_name = request.form.get('full_name', '').strip()
        phone = request.form.get('phone', '').strip()
        company = request.form.get('company', '').strip()

        if not full_name:
            flash('Ismingizni kiriting', 'error')
            return redirect(url_for('user_profile'))

        cursor.execute("""
            UPDATE users SET full_name = %s, phone = %s, company = %s
            WHERE id = %s
        """, (full_name, phone, company, session['user_id']))
        mysql.connection.commit()

        session['user_name'] = full_name
        flash('Profil muvaffaqiyatli yangilandi', 'success')
        return redirect(url_for('user_profile'))

    cursor.execute("SELECT * FROM users WHERE id = %s", (session['user_id'],))
    user = cursor.fetchone()
    cursor.close()

    return render_template('pages/profile.html', user=user)

@app.route('/chat')
@login_required
def user_chat():
    """AI yordamchi chat"""
    conversation_id = request.args.get('id', type=int)

    cursor = mysql.connection.cursor()
    messages = []

    if conversation_id:
        # Get messages for this conversation
        cursor.execute("""
            SELECT * FROM messages
            WHERE conversation_id = %s
            ORDER BY created_at ASC
        """, (conversation_id,))
        messages = cursor.fetchall()

    cursor.close()

    return render_template('pages/chat.html',
                         conversation_id=conversation_id,
                         messages=messages)

# ============ ADMIN ROUTES ============

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    """Admin login"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        admin_username = os.getenv('ADMIN_USERNAME', 'admin')
        admin_password = os.getenv('ADMIN_PASSWORD', 'admin123')

        if username == admin_username and password == admin_password:
            session['admin_logged_in'] = True
            session['admin_username'] = username
            flash('Xush kelibsiz!', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Login yoki parol noto\'g\'ri', 'error')

    return render_template('admin/login.html')

@app.route('/admin/logout')
def admin_logout():
    """Admin logout"""
    session.pop('admin_logged_in', None)
    session.pop('admin_username', None)
    flash('Tizimdan chiqdingiz', 'info')
    return redirect(url_for('admin_login'))

@app.route('/admin')
@admin_required
def admin_dashboard():
    """Admin dashboard"""
    cursor = mysql.connection.cursor()

    # Get statistics
    cursor.execute("SELECT COUNT(*) FROM users")
    total_users = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM users WHERE is_active = 1")
    active_users = cursor.fetchone()[0]

    cursor.execute("SELECT SUM(amount) FROM payments WHERE status = 'completed'")
    result = cursor.fetchone()
    total_revenue = result[0] if result[0] else 0

    cursor.execute("SELECT COUNT(*) FROM contacts WHERE is_read = 0")
    unread_messages = cursor.fetchone()[0]

    # Get revenue data for chart (last 12 months)
    cursor.execute("""
        SELECT DATE_FORMAT(created_at, '%Y-%m') as month, SUM(amount) as total
        FROM payments
        WHERE status = 'completed' AND created_at >= DATE_SUB(NOW(), INTERVAL 12 MONTH)
        GROUP BY month
        ORDER BY month ASC
    """)
    revenue_data = cursor.fetchall()

    # Get user growth data (last 12 months)
    cursor.execute("""
        SELECT DATE_FORMAT(created_at, '%Y-%m') as month, COUNT(*) as total
        FROM users
        WHERE created_at >= DATE_SUB(NOW(), INTERVAL 12 MONTH)
        GROUP BY month
        ORDER BY month ASC
    """)
    user_growth_data = cursor.fetchall()

    cursor.close()

    stats = {
        'total_users': total_users,
        'active_users': active_users,
        'total_revenue': total_revenue,
        'unread_messages': unread_messages,
        'revenue_data': revenue_data,
        'user_growth_data': user_growth_data
    }

    return render_template('admin/dashboard.html', stats=stats)

# ============ ADMIN USER MANAGEMENT ============

@app.route('/admin/users')
@admin_required
def admin_users():
    """Foydalanuvchilar boshqaruvi"""
    page = request.args.get('page', 1, type=int)
    per_page = 20
    search = request.args.get('search', '')
    plan = request.args.get('plan', '')
    status = request.args.get('status', '')

    cursor = mysql.connection.cursor()

    # Build query
    query = "SELECT * FROM users WHERE 1=1"
    params = []

    if search:
        query += " AND (full_name LIKE %s OR email LIKE %s OR phone LIKE %s)"
        search_term = f"%{search}%"
        params.extend([search_term, search_term, search_term])

    if plan:
        query += " AND plan_type = %s"
        params.append(plan)

    if status:
        query += " AND is_active = %s"
        params.append(1 if status == 'active' else 0)

    # Get total count
    count_query = query.replace("SELECT *", "SELECT COUNT(*)")
    cursor.execute(count_query, params)
    total = cursor.fetchone()[0]
    total_pages = (total + per_page - 1) // per_page

    # Get users
    query += " ORDER BY created_at DESC LIMIT %s OFFSET %s"
    params.extend([per_page, (page - 1) * per_page])
    cursor.execute(query, params)
    users = cursor.fetchall()

    cursor.close()

    return render_template('admin/users.html',
                         users=users,
                         page=page,
                         total_pages=total_pages,
                         search=search,
                         plan=plan,
                         status=status)

@app.route('/admin/users/export')
@admin_required
def admin_users_export():
    """Export users to CSV"""
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM users ORDER BY created_at DESC")
    users = cursor.fetchall()
    cursor.close()

    # Create CSV
    si = StringIO()
    writer = csv.writer(si)
    writer.writerow(['ID', 'Full Name', 'Email', 'Phone', 'Company', 'Plan', 'Status', 'Created At'])

    for user in users:
        writer.writerow([
            user[0], user[1], user[2], user[4] or '', user[5] or '',
            user[6], 'Active' if user[7] else 'Inactive', user[10]
        ])

    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename=users.csv"
    output.headers["Content-type"] = "text/csv"
    return output

@app.route('/admin/users/edit/<int:user_id>', methods=['GET', 'POST'])
@admin_required
def admin_user_edit(user_id):
    """Edit user"""
    cursor = mysql.connection.cursor()

    if request.method == 'POST':
        full_name = request.form.get('full_name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        company = request.form.get('company')
        plan_type = request.form.get('plan_type')
        is_active = 1 if request.form.get('is_active') else 0

        cursor.execute("""
            UPDATE users
            SET full_name = %s, email = %s, phone = %s, company = %s,
                plan_type = %s, is_active = %s
            WHERE id = %s
        """, (full_name, email, phone, company, plan_type, is_active, user_id))
        mysql.connection.commit()
        cursor.close()

        flash('Foydalanuvchi muvaffaqiyatli yangilandi', 'success')
        return redirect(url_for('admin_users'))

    cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    user = cursor.fetchone()
    cursor.close()

    if not user:
        flash('Foydalanuvchi topilmadi', 'error')
        return redirect(url_for('admin_users'))

    return render_template('admin/user_edit.html', user=user)

@app.route('/admin/users/delete/<int:user_id>', methods=['POST'])
@admin_required
def admin_user_delete(user_id):
    """Delete user"""
    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
    mysql.connection.commit()
    cursor.close()

    flash('Foydalanuvchi o\'chirildi', 'success')
    return redirect(url_for('admin_users'))

# ============ ADMIN REVENUE ============

@app.route('/admin/revenue')
@admin_required
def admin_revenue():
    """Daromadlar"""
    page = request.args.get('page', 1, type=int)
    per_page = 20

    cursor = mysql.connection.cursor()

    # Get total count
    cursor.execute("SELECT COUNT(*) FROM payments")
    total = cursor.fetchone()[0]
    total_pages = (total + per_page - 1) // per_page

    # Get payments
    cursor.execute("""
        SELECT p.*, u.full_name, u.email
        FROM payments p
        LEFT JOIN users u ON p.user_id = u.id
        ORDER BY p.created_at DESC
        LIMIT %s OFFSET %s
    """, (per_page, (page - 1) * per_page))
    payments = cursor.fetchall()

    cursor.close()

    return render_template('admin/revenue.html',
                         payments=payments,
                         page=page,
                         total_pages=total_pages)

@app.route('/admin/revenue/export')
@admin_required
def admin_revenue_export():
    """Export payments to CSV"""
    cursor = mysql.connection.cursor()
    cursor.execute("""
        SELECT p.*, u.full_name, u.email
        FROM payments p
        LEFT JOIN users u ON p.user_id = u.id
        ORDER BY p.created_at DESC
    """)
    payments = cursor.fetchall()
    cursor.close()

    # Create CSV
    si = StringIO()
    writer = csv.writer(si)
    writer.writerow(['ID', 'User', 'Email', 'Amount', 'Plan', 'Method', 'Status', 'Date'])

    for payment in payments:
        writer.writerow([
            payment[0], payment[8] or 'N/A', payment[9] or 'N/A',
            payment[2], payment[3], payment[4] or 'N/A', payment[5], payment[7]
        ])

    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename=payments.csv"
    output.headers["Content-type"] = "text/csv"
    return output

# ============ ADMIN CONTACTS ============

@app.route('/admin/contacts')
@admin_required
def admin_contacts():
    """Xabarlar"""
    page = request.args.get('page', 1, type=int)
    per_page = 20

    cursor = mysql.connection.cursor()

    # Get total count
    cursor.execute("SELECT COUNT(*) FROM contacts")
    total = cursor.fetchone()[0]
    total_pages = (total + per_page - 1) // per_page

    # Get contacts
    cursor.execute("""
        SELECT * FROM contacts
        ORDER BY is_read ASC, created_at DESC
        LIMIT %s OFFSET %s
    """, (per_page, (page - 1) * per_page))
    contacts = cursor.fetchall()

    cursor.close()

    return render_template('admin/contacts.html',
                         contacts=contacts,
                         page=page,
                         total_pages=total_pages)

@app.route('/admin/contacts/<int:contact_id>/read', methods=['POST'])
@admin_required
def admin_contact_read(contact_id):
    """Mark contact as read"""
    cursor = mysql.connection.cursor()
    cursor.execute("UPDATE contacts SET is_read = 1 WHERE id = %s", (contact_id,))
    mysql.connection.commit()
    cursor.close()

    return jsonify({'success': True})

@app.route('/admin/contacts/<int:contact_id>/delete', methods=['POST'])
@admin_required
def admin_contact_delete(contact_id):
    """Delete contact"""
    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM contacts WHERE id = %s", (contact_id,))
    mysql.connection.commit()
    cursor.close()

    flash('Xabar o\'chirildi', 'success')
    return redirect(url_for('admin_contacts'))

# ============ ADMIN BLOG MANAGEMENT ============

@app.route('/admin/blog')
@admin_required
def admin_blog():
    """Blog boshqaruvi"""
    page = request.args.get('page', 1, type=int)
    per_page = 20

    cursor = mysql.connection.cursor()

    # Get total count
    cursor.execute("SELECT COUNT(*) FROM blog_posts")
    total = cursor.fetchone()[0]
    total_pages = (total + per_page - 1) // per_page

    # Get posts
    cursor.execute("""
        SELECT * FROM blog_posts
        ORDER BY created_at DESC
        LIMIT %s OFFSET %s
    """, (per_page, (page - 1) * per_page))
    posts = cursor.fetchall()

    cursor.close()

    return render_template('admin/blog.html',
                         posts=posts,
                         page=page,
                         total_pages=total_pages)

@app.route('/admin/blog/new', methods=['GET', 'POST'])
@admin_required
def admin_blog_new():
    """Yangi blog post"""
    if request.method == 'POST':
        title = request.form.get('title')
        excerpt = request.form.get('excerpt')
        content = request.form.get('content')
        category = request.form.get('category')
        tags = request.form.get('tags')
        author = request.form.get('author', 'BalansAI Team')
        is_published = 1 if request.form.get('is_published') else 0

        slug = generate_slug(title)

        cursor = mysql.connection.cursor()

        # Check if slug exists
        cursor.execute("SELECT id FROM blog_posts WHERE slug = %s", (slug,))
        if cursor.fetchone():
            slug = f"{slug}-{secrets.token_hex(4)}"

        cursor.execute("""
            INSERT INTO blog_posts
            (title, slug, excerpt, content, category, tags, author, is_published, published_at, created_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (title, slug, excerpt, content, category, tags, author, is_published,
              datetime.datetime.now() if is_published else None, datetime.datetime.now()))
        mysql.connection.commit()
        cursor.close()

        flash('Blog post yaratildi', 'success')
        return redirect(url_for('admin_blog'))

    return render_template('admin/blog_edit.html', post=None)

@app.route('/admin/blog/edit/<int:post_id>', methods=['GET', 'POST'])
@admin_required
def admin_blog_edit(post_id):
    """Blog post tahrirlash"""
    cursor = mysql.connection.cursor()

    if request.method == 'POST':
        title = request.form.get('title')
        excerpt = request.form.get('excerpt')
        content = request.form.get('content')
        category = request.form.get('category')
        tags = request.form.get('tags')
        author = request.form.get('author', 'BalansAI Team')
        is_published = 1 if request.form.get('is_published') else 0

        # Get current post
        cursor.execute("SELECT is_published FROM blog_posts WHERE id = %s", (post_id,))
        current = cursor.fetchone()

        # Update published_at if status changed
        published_at = None
        if is_published and not current[0]:
            published_at = datetime.datetime.now()

        if published_at:
            cursor.execute("""
                UPDATE blog_posts
                SET title = %s, excerpt = %s, content = %s, category = %s,
                    tags = %s, author = %s, is_published = %s, published_at = %s
                WHERE id = %s
            """, (title, excerpt, content, category, tags, author, is_published, published_at, post_id))
        else:
            cursor.execute("""
                UPDATE blog_posts
                SET title = %s, excerpt = %s, content = %s, category = %s,
                    tags = %s, author = %s, is_published = %s
                WHERE id = %s
            """, (title, excerpt, content, category, tags, author, is_published, post_id))

        mysql.connection.commit()
        cursor.close()

        flash('Blog post yangilandi', 'success')
        return redirect(url_for('admin_blog'))

    cursor.execute("SELECT * FROM blog_posts WHERE id = %s", (post_id,))
    post = cursor.fetchone()
    cursor.close()

    if not post:
        flash('Post topilmadi', 'error')
        return redirect(url_for('admin_blog'))

    return render_template('admin/blog_edit.html', post=post)

@app.route('/admin/blog/delete/<int:post_id>', methods=['POST'])
@admin_required
def admin_blog_delete(post_id):
    """Blog post o'chirish"""
    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM blog_posts WHERE id = %s", (post_id,))
    mysql.connection.commit()
    cursor.close()

    flash('Blog post o\'chirildi', 'success')
    return redirect(url_for('admin_blog'))

# ============ ADMIN TESTIMONIALS ============

@app.route('/admin/testimonials')
@admin_required
def admin_testimonials():
    """Testimonials boshqaruvi"""
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM testimonials ORDER BY display_order ASC, created_at DESC")
    testimonials = cursor.fetchall()
    cursor.close()

    return render_template('admin/testimonials.html', testimonials=testimonials)

@app.route('/admin/testimonials/new', methods=['GET', 'POST'])
@admin_required
def admin_testimonial_new():
    """Yangi testimonial"""
    if request.method == 'POST':
        name = request.form.get('name')
        position = request.form.get('position')
        company = request.form.get('company')
        content = request.form.get('content')
        rating = request.form.get('rating', 5, type=int)
        display_order = request.form.get('display_order', 0, type=int)
        is_active = 1 if request.form.get('is_active') else 0

        cursor = mysql.connection.cursor()
        cursor.execute("""
            INSERT INTO testimonials
            (name, position, company, content, rating, display_order, is_active, created_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (name, position, company, content, rating, display_order, is_active, datetime.datetime.now()))
        mysql.connection.commit()
        cursor.close()

        flash('Testimonial yaratildi', 'success')
        return redirect(url_for('admin_testimonials'))

    return render_template('admin/testimonial_edit.html', testimonial=None)

@app.route('/admin/testimonials/edit/<int:testimonial_id>', methods=['GET', 'POST'])
@admin_required
def admin_testimonial_edit(testimonial_id):
    """Testimonial tahrirlash"""
    cursor = mysql.connection.cursor()

    if request.method == 'POST':
        name = request.form.get('name')
        position = request.form.get('position')
        company = request.form.get('company')
        content = request.form.get('content')
        rating = request.form.get('rating', 5, type=int)
        display_order = request.form.get('display_order', 0, type=int)
        is_active = 1 if request.form.get('is_active') else 0

        cursor.execute("""
            UPDATE testimonials
            SET name = %s, position = %s, company = %s, content = %s,
                rating = %s, display_order = %s, is_active = %s
            WHERE id = %s
        """, (name, position, company, content, rating, display_order, is_active, testimonial_id))
        mysql.connection.commit()
        cursor.close()

        flash('Testimonial yangilandi', 'success')
        return redirect(url_for('admin_testimonials'))

    cursor.execute("SELECT * FROM testimonials WHERE id = %s", (testimonial_id,))
    testimonial = cursor.fetchone()
    cursor.close()

    if not testimonial:
        flash('Testimonial topilmadi', 'error')
        return redirect(url_for('admin_testimonials'))

    return render_template('admin/testimonial_edit.html', testimonial=testimonial)

@app.route('/admin/testimonials/delete/<int:testimonial_id>', methods=['POST'])
@admin_required
def admin_testimonial_delete(testimonial_id):
    """Testimonial o'chirish"""
    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM testimonials WHERE id = %s", (testimonial_id,))
    mysql.connection.commit()
    cursor.close()

    flash('Testimonial o\'chirildi', 'success')
    return redirect(url_for('admin_testimonials'))

# ============ ADMIN SETTINGS ============

@app.route('/admin/settings', methods=['GET', 'POST'])
@admin_required
def admin_settings():
    """Sozlamalar"""
    if request.method == 'POST':
        # Update settings
        cursor = mysql.connection.cursor()

        for key in request.form:
            value = request.form.get(key)
            cursor.execute(
                "UPDATE settings SET value = %s WHERE key_name = %s",
                (value, key)
            )

        mysql.connection.commit()
        cursor.close()

        flash('Sozlamalar yangilandi', 'success')
        return redirect(url_for('admin_settings'))

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM settings ORDER BY key_name")
    settings = cursor.fetchall()
    cursor.close()

    return render_template('admin/settings.html', settings=settings)

# ============ SEO ROUTES ============

@app.route('/sitemap.xml')
def sitemap():
    """Sitemap"""
    pages = []
    ten_days_ago = datetime.datetime.now() - datetime.timedelta(days=10)

    # Static pages
    for rule in app.url_map.iter_rules():
        if "GET" in rule.methods and len(rule.arguments) == 0:
            if not any(x in rule.rule for x in ['/admin', '/dashboard', '/profile', '/chat', '/logout']):
                pages.append({
                    'loc': url_for(rule.endpoint, _external=True),
                    'lastmod': ten_days_ago.strftime('%Y-%m-%d'),
                    'changefreq': 'weekly',
                    'priority': '0.8'
                })

    # Blog posts
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT slug, updated_at FROM blog_posts WHERE is_published = 1")
    posts = cursor.fetchall()
    for post in posts:
        pages.append({
            'loc': url_for('blog_post', slug=post[0], _external=True),
            'lastmod': post[1].strftime('%Y-%m-%d'),
            'changefreq': 'monthly',
            'priority': '0.7'
        })
    cursor.close()

    sitemap_xml = render_template('sitemap.xml', pages=pages)
    response = app.make_response(sitemap_xml)
    response.headers["Content-Type"] = "application/xml"

    return response

@app.route('/robots.txt')
def robots():
    """Robots.txt"""
    return """User-agent: *
Allow: /
Disallow: /admin/
Disallow: /dashboard/
Disallow: /profile/
Disallow: /chat/
Sitemap: {}/sitemap.xml
""".format(request.url_root.rstrip('/'))

# ============ ERROR HANDLERS ============

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('500.html'), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_ENV') != 'production'
    app.run(debug=debug, host='0.0.0.0', port=port)
