from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

# جلب البيانات من قاعدة البيانات لعرضها في الموقع
def get_data():
    conn = sqlite3.connect('attacks.db')
    conn.row_factory = sqlite3.Row
    attacks = conn.execute("SELECT * FROM incidents ORDER BY id DESC").fetchall()
    conn.close()
    return attacks

@app.route('/')
def index():
    data = get_data()
    return render_template('index.html', attacks=data)

if __name__ == '__main__':
    # تشغيل الموقع على المنفذ 5000
    app.run(debug=True, port=5000)
