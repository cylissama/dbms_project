# Online Library System 📚

This project is a web-based database system for managing books in an online library. The application allows users to register, log in, search for books, return books, and add new books to the database.

---

## Features 🚀

- User Registration and Login
- Search for Books
- Add New Books to the Database (restricted to authenticated users)
- Mark Books as Returned
- User-friendly Interface

---

## Setup Instructions ⚙️

### 1. Clone the Repository
Clone the project to your local machine:
```bash
git clone https://github.com/your-username/online-library-system.git
cd online-library-system
```

### 2. Create an Enviornment

Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

Mac/Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. To install the requirements in the env:

Windows:
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

Mac/Linux:
```bash
Apply migrations:
python manage.py makemigrations
python manage.py migrate
```

### 4. Run the Server
```bash
python manage.py runserver
```

### Optional - creates the database - create superuser (admin)
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```


