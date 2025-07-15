from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)

# Cấu hình kết nối MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'  
app.config['MYSQL_PASSWORD'] = '111111'
app.config['MYSQL_DB'] = 'todolist'

mysql = MySQL(app)

@app.route('/')
def index():
    """Hiển thị tất cả công việc (Read)"""
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, title, status FROM tasks ORDER BY id DESC")
    tasks = cur.fetchall()
    cur.close()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add_task():
    """Thêm công việc mới (Create)"""
    if request.method == 'POST':
        task_title = request.form['title']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO tasks (title, status) VALUES (%s, %s)", (task_title, False))
        mysql.connection.commit()
        cur.close()
    return redirect(url_for('index'))

@app.route('/update/<int:task_id>')
def update_task(task_id):
    """Cập nhật trạng thái công việc (Update)"""
    cur = mysql.connection.cursor()
    cur.execute("UPDATE tasks SET status = NOT status WHERE id = %s", (task_id,))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('index'))

@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    """Xóa một công việc (Delete)"""
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)