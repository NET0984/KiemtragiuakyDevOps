-- Create Database with UTF-8 charset
CREATE DATABASE IF NOT EXISTS devops_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE devops_db;

-- Create Students Table with UTF-8 charset
CREATE TABLE IF NOT EXISTS students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_name VARCHAR(100) NOT NULL,
    student_id VARCHAR(20) UNIQUE NOT NULL,
    class_name VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Insert sample data
INSERT INTO students (student_name, student_id, class_name) VALUES
('Nguyễn Thanh Phước', '2251220061', '22CT2'),
('Nguyễn Hồng Phúc', '2251220062', '22CT2'),
('Nguyễn Quang Sáng', '2251220063', '22CT2');
