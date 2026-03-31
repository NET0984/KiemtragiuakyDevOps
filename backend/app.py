from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_mysqldb import MySQL
import os
from dotenv import load_dotenv
import MySQLdb.cursors

load_dotenv()

app = Flask(__name__)
CORS(app)

# Config MySQL
app.config['MYSQL_HOST'] = os.getenv('DB_HOST', 'localhost')
app.config['MYSQL_USER'] = os.getenv('DB_USER', 'root')
app.config['MYSQL_PASSWORD'] = os.getenv('DB_PASSWORD', '')
app.config['MYSQL_DB'] = os.getenv('DB_NAME', 'devops_db')

mysql = MySQL(app)

# Tạo bảng Students nếu chưa tồn tại
with app.app_context():
    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS students (
                id INT AUTO_INCREMENT PRIMARY KEY,
                student_name VARCHAR(100) NOT NULL,
                student_id VARCHAR(20) UNIQUE NOT NULL,
                class_name VARCHAR(50) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        mysql.connection.commit()
        cursor.close()
    except Exception as e:
        print(f"Error creating table: {e}")

# Health Check Endpoint
@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok"}), 200

# Thông tin cá nhân
@app.route('/about', methods=['GET'])
def about():
    return jsonify({
        "student_name": "Nguyễn Văn A",
        "student_id": "20230001",
        "class": "CNTT-01",
        "app_name": os.getenv('APP_NAME', 'DevOps Mini Project')
    }), 200

# API: Lấy danh sách sinh viên
@app.route('/api/students', methods=['GET'])
def get_students():
    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM students')
        students = cursor.fetchall()
        cursor.close()
        return jsonify(students), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# API: Thêm sinh viên mới
@app.route('/api/students', methods=['POST'])
def add_student():
    try:
        data = request.get_json()
        
        if not data or 'student_name' not in data or 'student_id' not in data or 'class_name' not in data:
            return jsonify({"error": "Missing required fields"}), 400
        
        cursor = mysql.connection.cursor()
        cursor.execute(
            'INSERT INTO students (student_name, student_id, class_name) VALUES (%s, %s, %s)',
            (data['student_name'], data['student_id'], data['class_name'])
        )
        mysql.connection.commit()
        cursor.close()
        
        return jsonify({"message": "Student added successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# API: Cập nhật sinh viên
@app.route('/api/students/<int:student_id>', methods=['PUT'])
def update_student(student_id):
    try:
        data = request.get_json()
        
        cursor = mysql.connection.cursor()
        cursor.execute(
            'UPDATE students SET student_name=%s, class_name=%s WHERE id=%s',
            (data.get('student_name'), data.get('class_name'), student_id)
        )
        mysql.connection.commit()
        cursor.close()
        
        return jsonify({"message": "Student updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# API: Xóa sinh viên
@app.route('/api/students/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    try:
        cursor = mysql.connection.cursor()
        cursor.execute('DELETE FROM students WHERE id=%s', (student_id,))
        mysql.connection.commit()
        cursor.close()
        
        return jsonify({"message": "Student deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
