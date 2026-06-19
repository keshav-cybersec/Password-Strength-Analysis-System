from flask import Flask, render_template, request
import sqlite3
from datetime import datetime

app = Flask(__name__)

login_attempts = {}

def check_password_strength(password):
    score = 0

    if len(password) >= 8:
        score += 1
    if any(char.isupper() for char in password):
        score += 1
    if any(char.islower() for char in password):
        score += 1
    if any(char.isdigit() for char in password):
        score += 1
    if any(char in "!@#$%^&*()" for char in password):
        score += 1

    if score <= 2:
        return "Critical"
    elif score == 3:
        return "Medium"
    elif score == 4:
        return "High"
    else:
        return "Low"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():

    username = request.form['username']
    password = request.form['password']

    correct_username = "admin"
    correct_password = "Admin@123"

    if username not in login_attempts:
        login_attempts[username] = 0

    if username == correct_username and password == correct_password:
        login_attempts[username] = 0
        return "Login Successful"

    login_attempts[username] += 1
    attempts = login_attempts[username]

    if attempts >= 3:
        save_alert(username, "Multiple Failed Login Attempts")
        return f"Login Failed! Attempts: {attempts} (ALERT TRIGGERED)"

    return f"Login Failed! Attempts: {attempts}"

def save_alert(username, event):

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS alerts(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        event TEXT,
        time TEXT
    )
    """)

    cursor.execute(
        "INSERT INTO alerts(username,event,time) VALUES(?,?,?)",
        (username, event, str(datetime.now()))
    )

    conn.commit()
    conn.close()

if __name__ == '__main__':
    app.run(debug=True)
