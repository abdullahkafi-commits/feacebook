from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('messages.db')
    cursor = conn.cursor()
    # তারিখ ও সময় সেভ করার জন্য created_at কলাম যোগ করা হয়েছে
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contact_messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            message TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    user_name = request.form.get('user_name')
    user_message = request.form.get('user_message')
    
    if user_name and user_message:
        conn = sqlite3.connect('messages.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO contact_messages (name, message) VALUES (?, ?)', (user_name, user_message))
        conn.commit()
        conn.close()
        
    # ডাটা সেভ হওয়ার পর নতুন লিংকে রিডাইরেক্ট করবে
    return redirect("https://example.com") 

@app.route('/view-messages-xyz123')
def view_messages():
    conn = sqlite3.connect('messages.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, name, message, created_at FROM contact_messages')
    rows = cursor.fetchall()
    conn.close()
    
    # সুন্দর করে সিরিয়ালি সাজানোর জন্য HTML তৈরি
    html_output = "<h2>Submitted Messages:</h2><hr>"
    for row in rows:
        msg_id, name, message, timestamp = row
        html_output += f"<b>ID:</b> {msg_id}<br>"
        html_output += f"<b>Name:</b> {name}<br>"
        html_output += f"<b>Message:</b> {message}<br>"
        html_output += f"<b>Date/Time:</b> {timestamp}<br><hr>"
        
    return html_output

if __name__ == '__main__':
    app.run(debug=True)