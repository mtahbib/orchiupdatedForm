from flask import Flask, render_template, request, redirect, url_for, jsonify
import mysql.connector

app = Flask(__name__)

# Replace these with your MySQL database credentials
db_host = 'localhost'
db_user = 'root'
db_password = ''
db_name = 'mybook'

# Create a MySQL connection
connection = mysql.connector.connect(
    host=db_host,
    user=db_user,
    password=db_password,
    database=db_name
)

cursor = connection.cursor()

# Create the 'project_data' table if it doesn't exist
create_table_query = '''
CREATE TABLE IF NOT EXISTS project_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    emp_id INT,
    designation VARCHAR(255),
    project_name VARCHAR(255),
    project_description TEXT,
    project_ownership VARCHAR(255)
)
'''
cursor.execute(create_table_query)

@app.route('/')
def index():
    # Fetch and display existing project data
    cursor.execute('SELECT id, name, emp_id, designation, project_name, project_description, project_ownership FROM project_data')
    data = cursor.fetchall()
    return render_template('index.html', employees=data)

@app.route('/save', methods=['POST'])
def save():
    data = {
        'name': request.form['name'],
        'emp_id': int(request.form['emp_id']),
        'designation': request.form['designation'],
        'project_name': request.form['project_name'],
        'project_description': request.form['project_description'],
        'project_ownership': request.form['project_ownership']
    }

    save_to_database(data)

    return redirect(url_for('index'))

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update_employee(id):
    if request.method == 'POST':
        # Update project data in the database
        name = request.form['name']
        emp_id = int(request.form['emp_id'])
        designation = request.form['designation']
        project_name = request.form['project_name']
        project_description = request.form['project_description']
        project_ownership = request.form['project_ownership']

        update_query = '''
        UPDATE project_data SET name=%s, emp_id=%s, designation=%s, project_name=%s, project_description=%s, project_ownership=%s WHERE id=%s
        '''
        cursor.execute(update_query, (name, emp_id, designation, project_name, project_description, project_ownership, id))
        connection.commit()

        return jsonify({'message': 'Employee updated successfully'})

    cursor.execute('SELECT * FROM project_data WHERE id=%s', (id,))
    employee_data = cursor.fetchone()

    return render_template('update.html', employee=employee_data)

@app.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete_employee(id):
    if request.method == 'POST':
        # Delete project data from the database
        delete_query = 'DELETE FROM project_data WHERE id=%s'
        cursor.execute(delete_query, (id,))
        connection.commit()

        return jsonify({'message': 'Employee deleted successfully'})

    return redirect(url_for('index'))

def save_to_database(data):
    insert_query = '''
    INSERT INTO project_data (name, emp_id, designation, project_name, project_description, project_ownership)
    VALUES (%s, %s, %s, %s, %s, %s)
    '''

    cursor.execute(insert_query, (
        data['name'],
        data['emp_id'],
        data['designation'],
        data['project_name'],
        data['project_description'],
        data['project_ownership']
    ))
    connection.commit()

if __name__ == '__main__':
    app.run(debug=True)
