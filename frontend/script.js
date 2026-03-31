const API_BASE_URL = 'http://localhost:5001';

// Load Health Check on page load
document.addEventListener('DOMContentLoaded', () => {
    checkHealth();
    loadHome();
});

// Check Health Status
async function checkHealth() {
    try {
        const response = await fetch(`${API_BASE_URL}/health`);
        const data = await response.json();
        if (data.status === 'ok') {
            document.getElementById('health-status').textContent = '✅ Backend hoạt động bình thường';
            document.getElementById('health-status').style.color = '#27ae60';
        }
    } catch (error) {
        document.getElementById('health-status').textContent = '❌ Không kết nối được Backend';
        document.getElementById('health-status').style.color = '#e74c3c';
    }
}

// Load Home Section
function loadHome() {
    showSection('home');
    checkHealth();
}

// Load Students Section
function loadStudents() {
    showSection('students');
    fetchStudents();
}

// Load About Section
function loadAbout() {
    showSection('about');
    fetchAbout();
}

// Show Section
function showSection(sectionId) {
    const sections = document.querySelectorAll('.section');
    sections.forEach(section => section.classList.remove('active'));
    document.getElementById(sectionId).classList.add('active');
}

// Fetch Students from Backend
async function fetchStudents() {
    try {
        const response = await fetch(`${API_BASE_URL}/api/students`);
        const students = await response.json();
        
        const studentList = document.getElementById('studentList');
        studentList.innerHTML = '';
        
        if (students.length === 0) {
            studentList.innerHTML = '<tr><td colspan="5">Chưa có sinh viên nào</td></tr>';
        } else {
            students.forEach(student => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${student['id']}</td>
                    <td style="cursor: pointer; color: #667eea; text-decoration: underline;" onclick="editStudentName(${student['id']}, '${student['student_name']}', '${student['class_name']}')">${student['student_name']}</td>
                    <td>${student['student_id']}</td>
                    <td>${student['class_name']}</td>
                    <td><button class="btn delete" onclick="deleteStudent(${student['id']})">Xóa</button></td>
                `;
                studentList.appendChild(row);
            });
        }
    } catch (error) {
        alert('Lỗi khi tải danh sách sinh viên: ' + error);
    }
}

// Add Student
async function addStudent() {
    const studentName = document.getElementById('studentName').value;
    const studentId = document.getElementById('studentId').value;
    const className = document.getElementById('className').value;
    
    if (!studentName || !studentId || !className) {
        alert('Vui lòng điền đầy đủ thông tin');
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE_URL}/api/students`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                student_name: studentName,
                student_id: studentId,
                class_name: className
            })
        });
        
        if (response.ok) {
            alert('Thêm sinh viên thành công');
            document.getElementById('studentName').value = '';
            document.getElementById('studentId').value = '';
            document.getElementById('className').value = '';
            fetchStudents();
        } else {
            alert('Lỗi khi thêm sinh viên');
        }
    } catch (error) {
        alert('Lỗi: ' + error);
    }
}

// Delete Student
async function deleteStudent(id) {
    if (!confirm('Bạn chắc chắn muốn xóa?')) return;
    
    try {
        const response = await fetch(`${API_BASE_URL}/api/students/${id}`, {
            method: 'DELETE'
        });
        
        if (response.ok) {
            alert('Xóa thành công');
            fetchStudents();
        } else {
            alert('Lỗi khi xóa');
        }
    } catch (error) {
        alert('Lỗi: ' + error);
    }
}

// Edit Student Name
async function editStudentName(id, currentName, className) {
    const newName = prompt(`Sửa tên sinh viên:\n(Tên hiện tại: ${currentName})`, currentName);
    
    if (newName === null || newName.trim() === '') {
        return;
    }
    
    if (newName === currentName) {
        alert('Tên không thay đổi');
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE_URL}/api/students/${id}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                student_name: newName.trim(),
                class_name: className
            })
        });
        
        if (response.ok) {
            alert('Cập nhật tên thành công');
            fetchStudents();
        } else {
            alert('Lỗi khi cập nhật');
        }
    } catch (error) {
        alert('Lỗi: ' + error);
    }
}

// Fetch About Info
async function fetchAbout() {
    try {
        const response = await fetch(`${API_BASE_URL}/about`);
        const data = await response.json();
        
        const aboutContent = document.getElementById('aboutContent');
        aboutContent.innerHTML = `
            <p><strong>📝 Họ Tên:</strong> ${data.student_name}</p>
            <p><strong>🆔 Mã Số Sinh Viên:</strong> ${data.student_id}</p>
            <p><strong>🎓 Lớp:</strong> ${data.class}</p>
            <p><strong>🚀 Ứng Dụng:</strong> ${data.app_name}</p>
        `;
    } catch (error) {
        document.getElementById('aboutContent').innerHTML = `<p style="color: red;">Lỗi khi tải thông tin: ${error}</p>`;
    }
}
