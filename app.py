from flask import Flask, request
import sqlite3
import uuid

app = Flask(__name__)

# create database
conn = sqlite3.connect('messages.db')
c = conn.cursor()
c.execute('CREATE TABLE IF NOT EXISTS messages (id TEXT, content TEXT)')
conn.commit()
conn.close()

# home page
@app.route('/')
def home():
    return '''
    <h2>One-Time Secret Message</h2>
    <form action="/create" method="post">
        <textarea name="msg" placeholder="Enter your secret..." required></textarea><br><br>
        <button type="submit">Generate Link</button>
    </form>
    '''

# create message
@app.route('/create', methods=['POST'])
def create():
    msg = request.form['msg']
    uid = str(uuid.uuid4())

    conn = sqlite3.connect('messages.db')
    c = conn.cursor()
    c.execute('INSERT INTO messages VALUES (?, ?)', (uid, msg))
    conn.commit()
    conn.close()

    return f'''
    <h3>Share this link:</h3>
    <a href="/msg/{uid}">http://127.0.0.1:5000/msg/{uid}</a>
    <p>This message can be opened only once.</p>
    '''

# view message (only once)
@app.route('/msg/<id>')
def view(id):
    conn = sqlite3.connect('messages.db')
    c = conn.cursor()
    c.execute('SELECT content FROM messages WHERE id=?', (id,))
    data = c.fetchone()

    if data:
        msg = data[0]
        c.execute('DELETE FROM messages WHERE id=?', (id,))
        conn.commit()
        conn.close()
        return f"<h1>{msg}</h1>"
    else:
        return "<h1>Message expired or already opened</h1>"

if __name__ == '__main__':
    app.run(debug=True)
    