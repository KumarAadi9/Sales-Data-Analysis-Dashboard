import sqlite3
import bcrypt
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import streamlit as st

# Load hidden environment variables
load_dotenv()

def init_db():
    conn = sqlite3.connect('dashboard_enterprise.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            email TEXT PRIMARY KEY,
            password TEXT NOT NULL,
            saved_theme TEXT DEFAULT 'Neon Cyberpunk'
        )
    ''')
    conn.commit()
    conn.close()

# Initialize the database when this file is loaded
init_db()

def hash_password(password):
    # Generates a secure, salted bcrypt hash
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

def check_password(password, hashed_password):
    # Securely compares plain text to the bcrypt hash
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

def save_user(email_or_phone, password):
    try:
        conn = sqlite3.connect('dashboard_enterprise.db')
        c = conn.cursor()
        c.execute("INSERT INTO users (email, password) VALUES (?, ?)", 
                  (email_or_phone, hash_password(password)))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        return False

def authenticate(email_or_phone, password):
    conn = sqlite3.connect('dashboard_enterprise.db')
    c = conn.cursor()
    c.execute("SELECT password, saved_theme FROM users WHERE email=?", (email_or_phone,))
    result = c.fetchone()
    conn.close()
    
    if result and check_password(password, result[0]):
        st.session_state.theme = result[1] 
        return True
    return False

def reset_password(email_or_phone, new_password):
    conn = sqlite3.connect('dashboard_enterprise.db')
    c = conn.cursor()
    c.execute("UPDATE users SET password=? WHERE email=?", 
              (hash_password(new_password), email_or_phone))
    rows_affected = c.rowcount
    conn.commit()
    conn.close()
    return rows_affected > 0

def update_user_theme(email_or_phone, new_theme):
    if email_or_phone:
        conn = sqlite3.connect('dashboard_enterprise.db')
        c = conn.cursor()
        c.execute("UPDATE users SET saved_theme=? WHERE email=?", (new_theme, email_or_phone))
        conn.commit()
        conn.close()

def send_reset_email(target_email, otp_code):
    # Securely pulls email credentials from the .env file
    sender_email = st.secrets["EMAIL_SENDER"]
    sender_password = os.getenv("EMAIL_PASS")

    if not sender_email or not sender_password:
        print("Error: Email credentials not found in .env file.")
        return False

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = target_email
    msg['Subject'] = "AI Dashboard - Password Reset Code"
    body = f"Your secure password reset code is: {otp_code}\n\nIf you did not request this, please ignore this email."
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        print(f"Email failed: {e}")
        return False
    
def check_user_exists(email):
    # Securely checks if a user exists without leaking DB logic to the frontend
    conn = sqlite3.connect('dashboard_enterprise.db')
    c = conn.cursor()
    c.execute("SELECT email FROM users WHERE email=?", (email,))
    result = c.fetchone()
    conn.close()
    return result is not None        