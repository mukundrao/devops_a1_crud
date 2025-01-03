from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# SQLite database connection
DATABASE = 'employee.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    return conn

# Initialize the database
def init_db():
    with app.app_context():
        conn = get_db()
        conn.execute('''CREATE TABLE IF NOT EXISTS employees (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT)''')
        conn.commit()

@app.route('/')
def index():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM employees')
    employees = cursor.fetchall()
    conn.close()
    return render_template('list_employees.html', employees=employees)

@app.route('/create', methods=['GET', 'POST'])
def create_employee():
    if request.method == 'POST':
        name = request.form['name']
        conn = get_db()
        conn.execute('INSERT INTO employees (name) VALUES (?)', (name,))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('create_employee.html')

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update_employee(id):
    conn = get_db()
    if request.method == 'POST':
        name = request.form['name']
        conn.execute('UPDATE employees SET name = ? WHERE id = ?', (name, id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM employees WHERE id = ?', (id,))
    employee = cursor.fetchone()
    conn.close()
    return render_template('update_employee.html', employee=employee)

@app.route('/delete/<int:id>', methods=['POST'])
def delete_employee(id):
    conn = get_db()
    conn.execute('DELETE FROM employees WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)
