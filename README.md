<div dir="rtl">

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/FastAPI-0.111+-009688?style=for-the-badge&logo=fastapi&logoColor=white"/>
  <img src="https://img.shields.io/badge/Pydantic-v2-E92063?style=for-the-badge&logo=pydantic&logoColor=white"/>
  <img src="https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge"/>
</p>

<h1 align="center">🎓 سامانه مدیریت دانشجویان</h1>
<p align="center">یک REST API کامل برای مدیریت اطلاعات دانشجویان — ساخته‌شده با Python و FastAPI</p>

<p align="center">
  <a href="#-معرفی">معرفی</a> •
  <a href="#-امکانات">امکانات</a> •
  <a href="#-نصب-و-راه‌اندازی">نصب</a> •
  <a href="#-endpointها">Endpoints</a> •
  <a href="#-ساختار-پروژه">ساختار</a> •
  <a href="#english-version">English</a>
</p>

---

## 📌 معرفی

این پروژه یک **Student Management System** است که با فریم‌ورک **FastAPI** پیاده‌سازی شده.  
تمام اطلاعات دانشجویان در یک فایل JSON ذخیره می‌شود و از طریق API قابل مدیریت کامل است.

> پروژه‌ای مناسب برای یادگیری ساختار RESTful API، اعتبارسنجی داده با Pydantic و معماری ماژولار در Python.

---

## ✨ امکانات

| قابلیت | توضیح |
|--------|--------|
| 🔁 عملیات CRUD کامل | ایجاد، خواندن، ویرایش و حذف دانشجو |
| 🔍 جستجوی هوشمند | جستجو بر اساس نام (case-insensitive) |
| 📄 صفحه‌بندی | pagination کامل با page و page_size |
| ↕️ مرتب‌سازی | sort بر اساس id، name یا gpa |
| ✅ اعتبارسنجی | validation کامل با Pydantic v2 |
| 📧 اعتبارسنجی ایمیل | فرمت ایمیل بررسی می‌شود |
| 📝 لاگ‌گیری | ثبت تمام درخواست‌ها با زمان پاسخ |
| 💾 بکاپ خودکار | ایجاد نسخه پشتیبان از داده‌ها |
| 📚 مستندات خودکار | Swagger UI و ReDoc |

---

## 🚀 نصب و راه‌اندازی

### پیش‌نیازها
- Python 3.10 یا بالاتر
- pip

### مراحل

```bash
# ۱. کلون کردن پروژه
git clone https://github.com/YOUR_USERNAME/student-manager-api.git
cd student-manager-api

# ۲. ساخت محیط مجازی (توصیه می‌شود)
python -m venv venv
source venv/bin/activate        # Linux/Mac
venv\Scripts\activate           # Windows

# ۳. نصب وابستگی‌ها
pip install -r requirements.txt

# ۴. اجرای سرور
uvicorn main:app --reload
```

سرور روی `http://127.0.0.1:8000` اجرا می‌شود.

---

## 📖 Endpointها

| Method | Endpoint | توضیح |
|--------|----------|--------|
| `GET` | `/` | پیام خوشامد |
| `GET` | `/students/` | لیست همه دانشجویان |
| `GET` | `/students/{id}` | دریافت دانشجو با شناسه |
| `GET` | `/search/?q=...` | جستجو بر اساس نام |
| `POST` | `/students/` | افزودن دانشجوی جدید |
| `PUT` | `/students/{id}` | ویرایش اطلاعات دانشجو |
| `DELETE` | `/students/{id}` | حذف دانشجو |
| `POST` | `/backup/` | ایجاد نسخه پشتیبان |

### پارامترهای GET /students/

```
?page=1&page_size=10&sort_by=gpa&order=desc
```

---

## 📦 مدل داده

```json
{
  "id": 1,
  "name": "Ali Ahmadi",
  "major": "Computer Engineering",
  "gpa": 17.5,
  "email": "ali@gmail.com"
}
```

**قوانین اعتبارسنجی:**
- `id` → عدد صحیح مثبت و یکتا
- `name` → حداقل ۲ کاراکتر
- `gpa` → بین ۰.۰ تا ۲۰.۰
- `email` → اختیاری، فرمت معتبر

---

## 🗂 ساختار پروژه

```
student_manager/
├── main.py                          # نقطه ورودی اپلیکیشن
├── requirements.txt
├── README.md
├── .gitignore
├── data/
│   └── students.json                # فایل ذخیره‌سازی داده
└── app/
    ├── logger.py                    # تنظیمات لاگ‌گیری
    ├── models/
    │   └── student.py               # مدل‌های Pydantic
    ├── services/
    │   └── student_service.py       # منطق کسب‌وکار
    └── routes/
        ├── students.py              # endpointهای CRUD
        └── search.py                # جستجو و بکاپ
```

---

## 🔧 مثال‌های کاربردی

```bash
# افزودن دانشجو
curl -X POST http://127.0.0.1:8000/students/ \
  -H "Content-Type: application/json" \
  -d '{"id": 6, "name": "Zahra Tehrani", "major": "AI", "gpa": 18.9}'

# جستجو
curl "http://127.0.0.1:8000/search/?q=ali"

# لیست مرتب‌شده بر اساس معدل
curl "http://127.0.0.1:8000/students/?sort_by=gpa&order=desc"
```

---

</div>

---

<h2 id="english-version" align="center">🇬🇧 English Version</h2>

<p align="center">
  A clean, modular <strong>Student Management REST API</strong> built with Python & FastAPI.<br/>
  Data is stored in a local JSON file — no database required.
</p>

---

## 📌 Overview

This project implements a full **CRUD Student Management System** using FastAPI.  
It's designed with a clean modular architecture (models / services / routes) and includes several production-grade features out of the box.

---

## ✨ Features

- ✅ Full CRUD operations (Create, Read, Update, Delete)
- 🔍 Case-insensitive name search
- 📄 Pagination with configurable page size
- ↕️ Sorting by `id`, `name`, or `gpa`
- 🛡️ Input validation with Pydantic v2
- 📧 Email format validation
- 📝 Rotating file logger + request timing middleware
- 💾 Data backup endpoint
- 📚 Auto-generated Swagger UI & ReDoc docs

---

## 🚀 Quick Start

```bash
git clone https://github.com/YOUR_USERNAME/student-manager-api.git
cd student-manager-api

python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

pip install -r requirements.txt
uvicorn main:app --reload
```

Open **http://127.0.0.1:8000/docs** for interactive Swagger documentation.

---

## 📖 API Endpoints

| Method | Endpoint | Description | Status Code |
|--------|----------|-------------|-------------|
| `GET` | `/` | Welcome message | 200 |
| `GET` | `/students/` | List all students (paginated) | 200 |
| `GET` | `/students/{id}` | Get student by ID | 200 / 404 |
| `GET` | `/search/?q=...` | Search by name | 200 / 404 |
| `POST` | `/students/` | Add new student | 201 / 400 |
| `PUT` | `/students/{id}` | Update student | 200 / 404 |
| `DELETE` | `/students/{id}` | Delete student | 200 / 404 |
| `POST` | `/backup/` | Create data backup | 200 |

---

## 📦 Data Model

```json
{
  "id": 1,
  "name": "Ali Ahmadi",
  "major": "Computer Engineering",
  "gpa": 17.5,
  "email": "ali@gmail.com"
}
```

---

## 🗂 Project Structure

```
student_manager/
├── main.py                    # App entry point + middleware
├── requirements.txt
├── README.md
├── .gitignore
├── data/
│   └── students.json          # JSON data store
└── app/
    ├── logger.py              # Logging setup
    ├── models/student.py      # Pydantic models & validators
    ├── services/              # Business logic & file I/O
    └── routes/                # API route handlers
```

---

## 📜 License

This project is licensed under the **MIT License** — free to use, modify, and distribute.

---

<p align="center">Made with ❤️ using <a href="https://fastapi.tiangolo.com">FastAPI</a></p>
