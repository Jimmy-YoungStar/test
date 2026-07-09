from flask import Flask, request, render_template_string
import os
import psycopg2  # 引入数据库驱动

app = Flask(__name__)

# 从环境变量中获取数据库连接地址，如果没有则使用你刚才复制的 URL（注意不要泄露给别人）
# 建议在本地测试时直接粘贴你的数据库 URL
DATABASE_URL = os.environ.get('DATABASE_URL', 'postgresql://testing_database_jvtm_user:B8CkEnGDjjrH1vUh5fGiDeiqcXYU8TQA@dpg-d97kj1vavr4c73d3eg30-a.singapore-postgres.render.com/testing_database_jvtm')

# 初始化数据库：如果表不存在，就创建一个名为 messages 的表
def init_db():
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    # 创建一个包含 id 和 content(内容) 的表
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
    user_input = request.form.get('message')
    
    if user_input:
        # 将数据插入到数据库中
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        cur.execute("INSERT INTO messages (content) VALUES (%s)", (user_input,))
        conn.commit()
        cur.close()
        conn.close()
            
    return "<h3>提交成功！感谢你的输入。</h3><a href='/'>返回</a>"

# 这是一个简易的“后台查看页面”，访问 你的网址/admin 就能看到所有数据
@app.route('/admin')
def admin():
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    cur.execute("SELECT content FROM messages;")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    
    # 把所有数据拼成列表显示出来
    display_text = "<h2>后台数据列表：</h2><ul>"
    for row in rows:
        display_text += f"<li>{row[0]}</li>"
    display_text += "</ul><a href='/'>返回首页</a>"
    
    return display_text

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
