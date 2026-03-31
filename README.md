# DevOps Mini Project

## Mô Tả

Đây là một ứng dụng Full Stack bao gồm:
- **Backend**: Flask API (Python)
- **Frontend**: HTML/CSS/JavaScript
- **Database**: MySQL
- **Orchestration**: Docker & Docker Compose

## Cấu Trúc Project

```
.
├── backend/          # Ứng dụng Flask
│   ├── app.py       # Código chính
│   ├── requirements.txt
│   ├── .env
│   ├── .env.example
│   └── Dockerfile
├── frontend/        # Ứng dụng web
│   ├── index.html
│   ├── styles.css
│   ├── script.js
│   └── Dockerfile
├── database/        # Scripts MySQL
│   └── init.sql
└── docker-compose.yml
```

## Yêu Cầu

- Docker
- Docker Compose

## Cài Đặt & Chạy

### 1. Clone Repository
```bash
git clone <repository-url>
cd Kiemtragiuaki
```

### 2. Khởi Động Hệ Thống
```bash
docker-compose up -d
```

### 3. Truy Cập Ứng Dụng

- **Frontend**: http://localhost:8080
- **Backend API**: http://localhost:5000
- **Health Check**: http://localhost:5000/health
- **Thông Tin Cá Nhân**: http://localhost:5000/about

## API Endpoints

### Health Check
```
GET /health
Response: { "status": "ok" }
```

### Thông Tin Cá Nhân
```
GET /about
Response: {
  "student_name": "Nguyễn Văn A",
  "student_id": "20230001",
  "class": "CNTT-01",
  "app_name": "DevOps Mini Project"
}
```

### Danh Sách Sinh Viên
```
GET /api/students
```

### Thêm Sinh Viên
```
POST /api/students
Content-Type: application/json

{
  "student_name": "Tên sinh viên",
  "student_id": "Mã số",
  "class_name": "Lớp"
}
```

### Cập Nhật Sinh Viên
```
PUT /api/students/<id>
Content-Type: application/json

{
  "student_name": "Tên mới",
  "class_name": "Lớp mới"
}
```

### Xóa Sinh Viên
```
DELETE /api/students/<id>
```

## Biến Môi Trường

File `.env` trong backend:

```
PORT=5000
DB_HOST=db
DB_USER=root
DB_PASSWORD=root123
DB_NAME=devops_db
APP_NAME=DevOps Mini Project
```

## Dừng Hệ Thống

```bash
docker-compose down
```

## Xóa Dữ Liệu

```bash
docker-compose down -v
```

## Thông Tin Sinh Viên

- **Họ Tên**: Nguyễn Văn A
- **Mã Số**: 20230001
- **Lớp**: CNTT-01
