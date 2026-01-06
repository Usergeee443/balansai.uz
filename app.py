import os
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
from functools import wraps
import datetime

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

# Admin decorator
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_logged_in' not in session:
            flash('Iltimos, avval tizimga kiring', 'error')
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function

# ============ PUBLIC ROUTES ============

@app.route('/')
def index():
    """Bosh sahifa"""
    return render_template('pages/index.html')

@app.route('/about')
def about():
    """Balans AI haqida"""
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
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')

        # Save to database
        cursor = mysql.connection.cursor()
        cursor.execute(
            "INSERT INTO contacts (name, email, message, created_at) VALUES (%s, %s, %s, %s)",
            (name, email, message, datetime.datetime.now())
        )
        mysql.connection.commit()
        cursor.close()

        flash('Xabaringiz muvaffaqiyatli yuborildi!', 'success')
        return redirect(url_for('contact'))

    return render_template('pages/contact.html')

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

    cursor.close()

    stats = {
        'total_users': total_users,
        'active_users': active_users,
        'total_revenue': total_revenue,
        'unread_messages': unread_messages
    }

    return render_template('admin/dashboard.html', stats=stats)

@app.route('/admin/users')
@admin_required
def admin_users():
    """Foydalanuvchilar"""
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM users ORDER BY created_at DESC")
    users = cursor.fetchall()
    cursor.close()

    return render_template('admin/users.html', users=users)

@app.route('/admin/revenue')
@admin_required
def admin_revenue():
    """Daromadlar"""
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM payments ORDER BY created_at DESC")
    payments = cursor.fetchall()
    cursor.close()

    return render_template('admin/revenue.html', payments=payments)

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
    cursor.execute("SELECT * FROM settings")
    settings = cursor.fetchall()
    cursor.close()

    return render_template('admin/settings.html', settings=settings)

@app.route('/admin/contacts')
@admin_required
def admin_contacts():
    """Xabarlar"""
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM contacts ORDER BY created_at DESC")
    contacts = cursor.fetchall()
    cursor.close()

    return render_template('admin/contacts.html', contacts=contacts)

# ============ SEO ROUTES ============

@app.route('/sitemap.xml')
def sitemap():
    """Sitemap"""
    pages = []
    ten_days_ago = datetime.datetime.now() - datetime.timedelta(days=10)

    # Static pages
    for rule in app.url_map.iter_rules():
        if "GET" in rule.methods and len(rule.arguments) == 0:
            pages.append({
                'loc': url_for(rule.endpoint, _external=True),
                'lastmod': ten_days_ago.strftime('%Y-%m-%d'),
                'changefreq': 'weekly',
                'priority': '0.8'
            })

    sitemap_xml = render_template('sitemap.xml', pages=pages)
    response = app.make_response(sitemap_xml)
    response.headers["Content-Type"] = "application/xml"

    return response

@app.route('/robots.txt')
def robots():
    """Robots.txt"""
    return """User-agent: *
Allow: /
Sitemap: {}/sitemap.xml
""".format(request.url_root.rstrip('/'))

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
