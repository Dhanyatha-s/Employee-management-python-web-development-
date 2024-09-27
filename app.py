from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3

app = Flask(__name__, template_folder='tempalets')
app.secret_key = 'your_secret_key'

# Database setup: Connect and create the employee table if it doesn't exist
def init_db():
    conn = sqlite3.connect('employee.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Route to display all employees
@app.route('/')
def index():
    conn = sqlite3.connect('employee.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM employees')
    employees = cursor.fetchall()
    conn.close()
    return render_template('index.html', employees=employees)

# Route to add a new employee
@app.route('/add', methods=['POST'])
def add_employee():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']

        conn = sqlite3.connect('employee.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO employees (name, email, phone) VALUES (?, ?, ?)', (name, email, phone))
        conn.commit()
        conn.close()
        flash('Employee Added Successfully!')

        return redirect(url_for('index'))

# Route to update employee details
@app.route('/update', methods=['POST'])
def update_employee():
    if request.method == 'POST':
        id = request.form['id']
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']

        conn = sqlite3.connect('employee.db')
        cursor = conn.cursor()
        cursor.execute('UPDATE employees SET name = ?, email = ?, phone = ? WHERE id = ?', (name, email, phone, id))
        conn.commit()
        conn.close()
        flash('Employee Updated Successfully!')

        return redirect(url_for('index'))

# Route to delete an employee
@app.route('/delete/<int:id>', methods=['GET'])
def delete_employee(id):
    conn = sqlite3.connect('employee.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM employees WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('Employee Deleted Successfully!')

    return redirect(url_for('index'))

# Initialize the database and run the app
if __name__ == '__main__':
    init_db()
    app.run(debug=True)
