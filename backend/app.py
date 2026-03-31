from flask import Flask, jsonify, request
from flask_cors import CORS
import pymysql
import os
from dotenv import load_dotenv
import time

load_dotenv()

app = Flask(__name__)
CORS(app)

# Config
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_USER = os.getenv('DB_USER', 'root')
DB_PASSWORD = os.getenv('DB_PASSWORD', '')
DB_NAME = os.getenv('DB_NAME', 'devops_db')

def get_db_connection():
    """Tạo kết nối database"""
    try:
        connection = pymysql.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            cursorclass=pymysql.cursors.DictCursor
        )
        return connection
    except Exception as e:
        print(f"Database connection error: {e}")
        return None

def init_db():
    """Khởi tạo database"""
    max_retries = 5
    for attempt in range(max_retries):
        try:
            connection = pymysql.connect(
                host=DB_HOST,
                user=DB_USER,
                password=DB_PASSWORD
            )
            cursor = connection.cursor()
            
            # Tạo database
            cursor.execute(f'CREATE DATABASE IF NOT EXISTS {DB_NAME}')
            connection.select_db(DB_NAME)
            
            # Tạo bảng Students
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS students (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    student_name VARCHAR(100) NOT NULL,
                    student_id VARCHAR(20) UNIQUE NOT NULL,
                    class_name VARCHAR(50) NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            connection.commit()
            cursor.close()
            connection.close()
            print("✅ Database initialized successfully")
            return True
        except Exception as e:
            print(f"Attempt {attempt + 1}: Database init failed - {e}")
            if attempt < max_retries - 1:
                time.sleep(2)
    
    return False

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
        connection = get_db_connection()
        if not connection:
            return jsonify({"error": "Database connection failed"}), 500
        
        with connection.cursor() as cursor:
            cursor.execute('SELECT * FROM students')
            students = cursor.fetchall()
        
        connection.close()
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
        
        connection = get_db_connection()
        if not connection:
            return jsonify({"error": "Database connection failed"}), 500
        
        with connection.cursor() as cursor:
            cursor.execute(
                'INSERT INTO students (student_name, student_id, class_name) VALUES (%s, %s, %s)',
                (data['student_name'], data['student_id'], data['class_name'])
            )
            connection.commit()
        
        connection.close()
        return jsonify({"message": "Student added successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# API: Cập nhật sinh viên
@app.route('/api/students/<int:student_id>', methods=['PUT'])
def update_student(student_id):
    try:
        data = request.get_json()
        
        connection = get_db_connection()
        if not connection:
            return jsonify({"error": "Database connection failed"}), 500
        
        with connection.cursor() as cursor:
            cursor.execute(
                'UPDATE students SET student_name=%s, class_name=%s WHERE id=%s',
                (data.get('student_name'), data.get('class_name'), student_id)
            )
            connection.commit()
        
        connection.close()
        return jsonify({"message": "Student updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# API: Xóa sinh viên
@app.route('/api/students/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    try:
        connection = get_db_connection()
        if not connection:
            return jsonify({"error": "Database connection failed"}), 500
        
        with connection.cursor() as cursor:
            cursor.execute('DELETE FROM students WHERE id=%s', (student_id,))
            connection.commit()
        
        connection.close()
        return jsonify({"message": "Student deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Khởi tạo database
    init_db()
    
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
