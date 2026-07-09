from flask import Flask, request, render_template_string
import os

app = Flask(__name__)

# 读取你写的 HTML 文件内容
def get_html_content():
    with open("index.html", "r", encoding="utf-8") as f:
        return f.read()

# 1. 首页路由：大家访问网址时，看到你的 HTML 页面
@app.route('/')
def index():
    return get_html_content()

# 2. 提交路由：大家点击提交按钮时，数据会发送到这里
@app.route('/submit', methods=['POST'])
def submit():
    # 获取输入框里 name="message" 的内容
    user_input = request.form.get('message')
    
    if user_input:
        # 把内容追加保存到 data.txt 文件中，每条占一行
        with open("data.txt", "a", encoding="utf-8") as f:
            f.write(user_input + "\n")
            
    return "<h3>提交成功！感谢你的输入。</h3><a href='/'>返回</a>"

if __name__ == '__main__':
    # 允许局域网内其他设备访问
    app.run(host='0.0.0.0', port=5000, debug=True)