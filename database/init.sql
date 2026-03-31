-- Create Database
CREATE DATABASE IF NOT EXISTS devops_db;
USE devops_db;

-- Create Students Table
CREATE TABLE IF NOT EXISTS students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_name VARCHAR(100) NOT NULL,
    student_id VARCHAR(20) UNIQUE NOT NULL,
    class_name VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert sample data
INSERT INTO students (student_name, student_id, class_name) VALUES
('Nguyễn Văn A', '20230001', 'CNTT-01'),
('Trần Thị B', '20230002', 'CNTT-01'),
('Hoàng Văn C', '20230003', 'CNTT-02');
