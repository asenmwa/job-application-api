import os
from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
from dotenv import load_dotenv
import uuid
from datetime import datetime

load_dotenv()

app = Flask(__name__)

# MySQL Configuration
app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST')
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD')
app.config['MYSQL_DB'] = os.getenv('MYSQL_DB')
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

@app.route('/apply', methods=['POST'])
def apply():
    if 'full_name' not in request.form or not request.form['full_name']:
        return jsonify({'error': 'Full Name is required'}), 400
    if 'email' not in request.form or not request.form['email']:
        return jsonify({'error': 'Email Address is required'}), 400
    if 'phone_number' not in request.form or not request.form['phone_number']:
        return jsonify({'error': 'Phone Number is required'}), 400

    full_name = request.form['full_name']
    email = request.form['email']
    phone_number = request.form['phone_number']
    additional_fields = {k: v for k, v in request.form.items() if k not in ['full_name', 'email', 'phone_number']}
    files = request.files.to_dict(flat=False)

    # Basic email and phone number validation (can be improved)
    if '@' not in email:
        return jsonify({'error': 'Invalid email format'}), 400
    if not phone_number.isdigit():
        return jsonify({'error': 'Invalid phone number format'}), 400

    # File validation
    for file_list in files.values():
        for file in file_list:
            if file.filename.endswith('.pdf') is False:
                return jsonify({'error': 'Only PDF files are allowed'}), 400
            if len(file.read()) > 5 * 1024 * 1024:
                return jsonify({'error': 'File size exceeds 5 MB'}), 400
            file.seek(0)  # Reset file pointer

    # Generate unique token
    application_token = str(uuid.uuid4())

    # Get current timestamp
    submission_time = datetime.now()

    # Save to database
    try:
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO applications (application_token, full_name, email, phone_number, additional_fields, submission_time) VALUES (%s, %s, %s, %s, %s, %s)",
                    (application_token, full_name, email, phone_number, str(additional_fields), submission_time))
        application_id = mysql.connection.insert_id()
        for file_list in files.values():
            for file in file_list:
                cur.execute("INSERT INTO attachments (application_id, filename, data) VALUES (%s, %s, %s)",
                            (application_id, file.filename, file.read()))
        mysql.connection.commit()
        cur.close()
    except Exception as e:
        return jsonify({'error': f'Database error: {str(e)}'}), 500

    return jsonify({'message': 'Application submitted successfully', 'application_token': application_token}), 201

if __name__ == '__main__':
    app.run(debug=True)
