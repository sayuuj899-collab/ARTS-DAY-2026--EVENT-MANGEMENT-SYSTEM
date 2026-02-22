from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this'

# Database initialization
def init_db():
    conn = sqlite3.connect('instance/artsday.db')
    c = conn.cursor()
    
    # Create tables
    c.execute('''CREATE TABLE IF NOT EXISTS admins (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        department TEXT NOT NULL,
        phone TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT,
        category TEXT NOT NULL CHECK(category IN ('onstage', 'offstage')),
        max_participants INTEGER DEFAULT 1,
        registration_deadline TIMESTAMP,
        event_date TIMESTAMP,
        venue TEXT,
        created_by INTEGER,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (created_by) REFERENCES admins (id)
    )''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS registrations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER,
        event_id INTEGER,
        registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        status TEXT DEFAULT 'registered',
        FOREIGN KEY (student_id) REFERENCES students (id),
        FOREIGN KEY (event_id) REFERENCES events (id),
        UNIQUE(student_id, event_id)
    )''')
    
    # Create default admin if not exists
    c.execute("SELECT * FROM admins WHERE username = 'admin'")
    if not c.fetchone():
        hashed_password = generate_password_hash('admin123')
        c.execute("INSERT INTO admins (username, password) VALUES (?, ?)", 
                 ('admin', hashed_password))
    
    conn.commit()
    conn.close()

# Landing Page
@app.route('/')
def landing():
    return render_template('landing.html')

# Student Portal Routes
@app.route('/student')
def student_portal():
    return render_template('student_portal.html')

@app.route('/student/register', methods=['GET', 'POST'])
def student_register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        department = request.form['department']
        phone = request.form['phone']
        
        conn = sqlite3.connect('instance/artsday.db')
        c = conn.cursor()
        
        try:
            c.execute("INSERT INTO students (name, email, department, phone) VALUES (?, ?, ?, ?)",
                     (name, email, department, phone))
            student_id = c.lastrowid
            session['student_id'] = student_id
            session['student_name'] = name
            conn.commit()
            flash('Registration successful! You can now register for events.', 'success')
            return redirect(url_for('student_dashboard'))
        except sqlite3.IntegrityError:
            flash('Email already registered!', 'error')
        finally:
            conn.close()
    
    return render_template('student_register.html')

@app.route('/student/login', methods=['GET', 'POST'])
def student_login():
    if request.method == 'POST':
        email = request.form['email']
        
        conn = sqlite3.connect('instance/artsday.db')
        c = conn.cursor()
        c.execute("SELECT id, name FROM students WHERE email = ?", (email,))
        student = c.fetchone()
        conn.close()
        
        if student:
            session['student_id'] = student[0]
            session['student_name'] = student[1]
            return redirect(url_for('student_dashboard'))
        else:
            flash('Student not found!', 'error')
    
    return render_template('student_login.html')

@app.route('/student/dashboard')
def student_dashboard():
    if 'student_id' not in session:
        return redirect(url_for('student_login'))
    
    conn = sqlite3.connect('instance/artsday.db')
    c = conn.cursor()
    
    # Get available events
    c.execute("""SELECT e.*, 
                        (SELECT COUNT(*) FROM registrations r WHERE r.event_id = e.id) as registered_count
                 FROM events e 
                 WHERE e.registration_deadline > datetime('now')
                 ORDER BY e.event_date""")
    events = c.fetchall()
    
    # Get student's registrations
    c.execute("""SELECT e.name, e.category, e.event_date, e.venue, r.registration_date
                 FROM registrations r
                 JOIN events e ON r.event_id = e.id
                 WHERE r.student_id = ?
                 ORDER BY e.event_date""", (session['student_id'],))
    my_events = c.fetchall()
    
    conn.close()
    
    return render_template('student_dashboard.html', events=events, my_events=my_events)

@app.route('/student/register-event/<int:event_id>')
def register_for_event(event_id):
    if 'student_id' not in session:
        return redirect(url_for('student_login'))
    
    conn = sqlite3.connect('instance/artsday.db')
    c = conn.cursor()
    
    try:
        c.execute("INSERT INTO registrations (student_id, event_id) VALUES (?, ?)",
                 (session['student_id'], event_id))
        conn.commit()
        flash('Successfully registered for the event!', 'success')
    except sqlite3.IntegrityError:
        flash('You are already registered for this event!', 'error')
    finally:
        conn.close()
    
    return redirect(url_for('student_dashboard'))

# Admin Portal Routes
@app.route('/admin')
def admin_portal():
    return render_template('admin_portal.html')

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = sqlite3.connect('instance/artsday.db')
        c = conn.cursor()
        c.execute("SELECT id, password FROM admins WHERE username = ?", (username,))
        admin = c.fetchone()
        conn.close()
        
        if admin and check_password_hash(admin[1], password):
            session['admin_id'] = admin[0]
            session['admin_username'] = username
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid credentials!', 'error')
    
    return render_template('admin_login.html')

@app.route('/admin/dashboard')
def admin_dashboard():
    if 'admin_id' not in session:
        return redirect(url_for('admin_login'))
    
    return render_template('admin_dashboard.html')

@app.route('/admin/create-event', methods=['GET', 'POST'])
def create_event():
    if 'admin_id' not in session:
        return redirect(url_for('admin_login'))
    
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        category = request.form['category']
        max_participants = request.form['max_participants']
        registration_deadline = request.form['registration_deadline']
        event_date = request.form['event_date']
        venue = request.form['venue']
        
        conn = sqlite3.connect('instance/artsday.db')
        c = conn.cursor()
        c.execute("""INSERT INTO events 
                     (name, description, category, max_participants, registration_deadline, event_date, venue, created_by)
                     VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                 (name, description, category, max_participants, registration_deadline, event_date, venue, session['admin_id']))
        conn.commit()
        conn.close()
        
        flash('Event created successfully!', 'success')
        return redirect(url_for('admin_dashboard'))
    
    return render_template('create_event.html')

@app.route('/admin/events')
def admin_events():
    if 'admin_id' not in session:
        return redirect(url_for('admin_login'))
    
    conn = sqlite3.connect('instance/artsday.db')
    c = conn.cursor()
    c.execute("""SELECT e.*, 
                        (SELECT COUNT(*) FROM registrations r WHERE r.event_id = e.id) as registered_count
                 FROM events e 
                 ORDER BY e.created_at DESC""")
    events = c.fetchall()
    conn.close()
    
    return render_template('admin_events.html', events=events)

@app.route('/admin/onstage')
def onstage_participants():
    if 'admin_id' not in session:
        return redirect(url_for('admin_login'))
    
    conn = sqlite3.connect('instance/artsday.db')
    c = conn.cursor()
    c.execute("""SELECT e.name as event_name, s.name as student_name, s.department, s.phone, r.registration_date
                 FROM registrations r
                 JOIN events e ON r.event_id = e.id
                 JOIN students s ON r.student_id = s.id
                 WHERE e.category = 'onstage'
                 ORDER BY e.name, s.name""")
    participants = c.fetchall()
    conn.close()
    
    return render_template('onstage_participants.html', participants=participants)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('landing'))

if __name__ == '__main__':
    # Ensure instance directory exists
    os.makedirs('instance', exist_ok=True)
    init_db()
    app.run(debug=True)