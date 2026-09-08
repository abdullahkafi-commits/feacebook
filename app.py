from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('messages.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contact_messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            message TEXT NOT NULL
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
        
    return "Data saved successfully!"

# ডাটাবেসের মেসেজ দেখার জন্য নতুন রুট (এখানে যুক্ত করা হয়েছে)
@app.route('/view-messages-xyz123')
def view_messages():
    conn = sqlite3.connect('messages.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM contact_messages')
    data = cursor.fetchall()
    conn.close()
    return f"Messages: {data}"

if __name__ == '__main__':
    app.run(debug=True)