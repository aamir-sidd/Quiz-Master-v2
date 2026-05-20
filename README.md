# QuizMaster v2

QuizMaster v2 is a high-performance, full-stack quiz management and attempt platform. The application is built using a modern decoupled architecture, featuring a reactive frontend powered by **Vue 3** and **Vite**, and a scalable RESTful backend powered by **Flask** and **SQLAlchemy**. Additionally, it integrates **Redis** for high-efficiency caching and **Celery** for asynchronous and scheduled background tasks.

---

## 🚀 Key Features

### 👤 Role-Based Portals (Admin & Student)
*   **Admin (Master) Panel**: Full CRUD control to manage courses, add sub-chapters, configure custom time-bound quizzes, and build randomized multiple-choice questions (MCQs).
*   **Student Dashboard**: A dynamic portal where students can search and view available quizzes, attempt time-bound quizzes in real-time, and view their comprehensive quiz history.

### ⚡ Real-Time Grading & Feedback
*   Automatic percentage grading and evaluation upon quiz submission.
*   Comprehensive answer breakdowns displaying student selection vs. correct answer.

### 💨 High-Performance Caching
*   Integrated **Redis Caching** (`Flask-Caching`) utilizing key-value memoization for heavy database reads (e.g., listing courses, chapters, and past attempts).
*   Automatic cache invalidation triggers on mutation requests (POST/PUT/DELETE) to ensure data integrity.

### 📬 Asynchronous Tasks & Cron Automation
*   **Celery & Redis Broker**: Offloads intensive report generation and notification flows to background workers.
*   **Daily Engagement Reminders**: Automated emails sent to students prompting them to check out new quizzes.
*   **Monthly Performance Analytics**: Dynamically generated Jinja2 HTML reports compile student performance analytics and email them automatically on the 1st of every month.

---

## 🛠️ Tech Stack

*   **Frontend**: Vue 3 (Options API), Vue Router, Bootstrap 5 (Styling & Grid System), Vite (Build Tool).
*   **Backend**: Flask, Flask-RESTful (REST API Architecture), Flask-SQLAlchemy (ORM), Flask-JWT-Extended (Token-based Auth).
*   **Database**: SQLite (Development-ready relational storage).
*   **Asynchronous Pipeline**: Celery (Worker Queue), Celery Beat (Cron Scheduler).
*   **Caching & Broker**: Redis.

---

## 📁 Project Directory Structure

```text
QuizMaster/
│
├── applications/             # Core Flask backend applications
│   ├── auth.py               # User registration and JWT login APIs
│   ├── master.py             # Admin CRUD APIs (Courses, Chapters, Quizzes, Questions)
│   ├── models.py             # SQLAlchemy models (User, Course, Chapter, Quiz, Question, Score)
│   ├── student.py            # Student quiz viewing, taking, and history APIs
│   ├── task.py               # Celery asynchronous tasks (Daily reminders, Monthly HTML reports)
│   ├── worker.py             # Celery application initialization
│   └── report/
│       └── report.html       # Jinja2 template for monthly performance emails
│
├── src/                      # Vue 3 Frontend Source
│   ├── components/           # Reusable Vue components (Navbar, management modals)
│   ├── views/                # Full page views (Login, Registration, Admin and Student Dashboards)
│   ├── router/               # Vue Router configuration
│   ├── App.vue               # Main entry view container
│   └── main.js               # Frontend entry script
│
├── instance/                 # Local database storage directory
├── main.py                   # Backend entrypoint (runs Flask server)
├── package.json              # Frontend npm dependencies and scripts
├── vite.config.js            # Vite bundler configuration
└── README.md                 # Project documentation
```

---

## 🔧 Installation & Setup

Follow these steps to run the application locally on your machine.

### Prerequisites
*   **Python 3.8+**
*   **Node.js 16+** & **npm**
*   **Redis Server** (Installed and running on `localhost:6379`)
*   **Local SMTP Server** (e.g., MailHog or python smtp debugging server running on port `1025`) for email testing.

---

### Step 1: Start Redis Server
Ensure Redis is running locally:
```bash
redis-server
```

---

### Step 2: Set Up Backend (Flask)

1. **Navigate to the workspace root** and create a Python virtual environment:
   ```bash
   python -m venv venv
   ```
2. **Activate the virtual environment**:
   *   **Windows**: `venv\Scripts\activate`
   *   **macOS/Linux**: `source venv/bin/activate`
3. **Install Backend Dependencies**:
   Create a local backend dependencies list or run the following:
   ```bash
   pip install Flask flask-restful flask-sqlalchemy flask-jwt-extended flask-cors flask-caching celery redis jinja2
   ```
4. **Start local SMTP Debugging Server** (to intercept and read generated emails):
   ```bash
   python -m smtpd -c DebuggingServer -n localhost:1025
   ```
5. **Initialize Database and Start Flask Server**:
   ```bash
   python main.py
   ```
   *Note: On first boot, the system automatically initializes `quiz_master.db` and generates a default Admin credential:*
   *   **Email**: `admin@gmail.com`
   *   **Password**: `admin`

---

### Step 3: Run Celery Workers & Beat Scheduler

Keep your virtual environment active and open two new terminal windows:

*   **Terminal 1 (Celery Workers)**:
    ```bash
    celery -A main.celery worker --loglevel=info
    ```
*   **Terminal 2 (Celery Beat Scheduler)**:
    ```bash
    celery -A main.celery beat --loglevel=info
    ```

---

### Step 4: Set Up Frontend (Vue 3 + Vite)

1. Open a new terminal in the workspace root.
2. **Install Frontend Dependencies**:
   ```bash
   npm install
   ```
3. **Run Development Server**:
   ```bash
   npm run dev
   ```
4. Open the displayed URL (usually `http://localhost:5173`) in your browser to access the portal!

---

## 🔒 API Endpoints Reference

| Category | Endpoint | Method | Role | Description |
| :--- | :--- | :--- | :--- | :--- |
| **Auth** | `/auth/register` | `POST` | Public | Registers a new student account |
| **Auth** | `/auth/login` | `POST` | Public | Authenticates credentials and returns a JWT |
| **Admin** | `/admin/courses` | `GET` / `POST` | Admin | Retrieve all courses (cached) or create a new course |
| **Admin** | `/admin/courses/<id>`| `GET` / `PUT` / `DELETE` | Admin | Manage individual course details |
| **Admin** | `/admin/chapters` | `GET` | Admin | Retrieve all chapters across courses |
| **Admin** | `/admin/chapter/<id>`| `POST`/`PUT`/`DELETE` | Admin | Create/Update/Delete chapters |
| **Admin** | `/admin/quiz/<id>` | `POST`/`PUT`/`DELETE` | Admin | Manage quizzes assigned to chapters |
| **Admin** | `/admin/question/<id>`| `POST`/`PUT`/`DELETE`| Admin | Create/Update/Delete quiz questions |
| **Student**| `/student/quizzes` | `GET` | Student | Lists all available quizzes |
| **Student**| `/student/quiz/<id>` | `GET` / `POST` | Student | Fetch questions / Submit completed attempts |
| **Student**| `/student/quiz-history`| `GET` | Student | Fetch student score history logs |

---

## 📝 License
This project is open-source and available under the MIT License.
