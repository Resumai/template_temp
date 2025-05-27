# ✅ Project TODO Checklist – University Management System

## 1. User Authentication & Registration
- [ ] Create registration page for **students** and **lecturers** only
- [ ] Implement program selection during registration
- [ ] Auto-assign study group based on selected program
- [ ] Validate email and password using regex
- [ ] Allow profile picture upload with size/type validation
- [ ] Store picture paths in DB and images in folder
- [x] Create login page with:
  - [ ] 3-attempt limit → temporary account lock
- [ ] Hardcode initial admin
- [ ] Create admin registration page (accessible only to admins)

## 2. Role-Based Permissions
- [ ] **Student** can:
  - [ ] View assigned modules
  - [ ] See academic info (program, group)
  - [ ] See personal schedule (lectures, exams, tasks)
- [ ] **Lecturer** can:
  - [ ] Create/edit modules
  - [ ] Set semester, times, requirements
  - [ ] Manage assessments (lab deadlines, etc.)
  - [ ] Track attendance & grades
- [ ] **Admin** can:
  - [ ] Manage users, modules, programs, groups
  - [ ] Handle complex relationships (e.g., module ⇄ lecturer ⇄ program)

## 3. Module (Course) Management
- [ ] Implement CRUD for modules:
  - [ ] Create (name, desc, credits, semester, schedule, assessments)
  - [ ] Support prerequisites (Bonus)
  - [ ] Read (detailed view: schedule, lecturers, enrolled students)
  - [ ] Update
  - [ ] Delete (with confirmation)
- [ ] Student-side:
  - [ ] Select modules from their program
  - [ ] Check prerequisites & schedule conflicts
  - [ ] Add to personal calendar
- [ ] Lecturer-side:
  - [ ] Set/edit assessment dates
  - [ ] Integrate into calendar

## 4. BONUS: Testing System
- [ ] Lecturers create tests per module/exam
- [ ] Students solve tests
- [ ] Grade results and link to module
- [ ] Implement validation, security, error handling

## 5. Admin Dashboard
- [ ] Show system stats: user count, modules, groups, programs
- [ ] Add try-except logging for all admin actions
- [ ] Manage users:
  - [ ] Edit roles, deactivate/delete accounts, reassign groups
- [ ] Manage modules:
  - [ ] Update info, semester, schedule, prerequisites
  - [ ] Assign lecturers
  - [ ] Link to programs

## 6. Database Integration
- [ ] Create models:
  - [ ] User (role, program, group)
  - [ ] Module (with all details & prerequisites)
  - [ ] Group (auto-assigned via program)
  - [ ] Assessment (dates, descriptions, module FK)
  - [ ] Test (Bonus)
- [ ] Use `Flask-Migrate` for:
  - [ ] Schema evolution
  - [ ] Safe introduction of relationships
- [ ] Wrap all DB ops in `try-except`

## 7. Additional Features
- [ ] Image uploads:
  - [ ] Profile pictures
  - [ ] Module images (Bonus)
- [ ] Academic hierarchy:
  - [ ] Programs belong to faculties
  - [ ] Modules and students link to program/faculty
  - [ ] Group code generation logic (e.g., `IFIN-18-A`)
- [ ] Enforce prerequisites and program-semester compatibility
- [ ] Schedule conflict checks
- [ ] Validate credit count, avoid negatives

## 8. Project Structure & DevOps
- [ ] Separate folders: `static`, `templates`, `controllers`, `services`, `crud`
- [ ] Use GitHub:
  - [ ] Branches: `main`, `development`, `feature/*`
  - [ ] Protect `main` branch (simulate)
  - [ ] At least **10 commits**
  - [ ] Create **pull requests**
- [ ] Use **JIRA** (or Trello, GitHub Projects) for task tracking
- [ ] Implement all DB migrations with `Flask-Migrate`

-------- Keeping it in case anyone neeeds these below too --------
# Student Management System

Core Modules to Include:
* Authentication & Authorization: Admin, Faculty, Students
* Student Management: Enrollments, attendance, transcripts
* Course Management: Add/edit/delete courses, assign faculty
* Faculty Management: Assign courses, view student lists
* Timetable/Schedule Management
* Grades & Results
* Fees & Payments
* Notifications & Messaging
* Reports & Analytics (optional)

2. Plan the Data Model (Database Design)

Use an ER diagram to define entities and relationships. Example tables:
* Users: id, name, email, password, role
* Students: student_id, user_id, dob, department_id
* Faculty: faculty_id, user_id, department_id
* Departments: id, name
* Courses: id, name, credits, department_id
* Enrollments: id, student_id, course_id, semester
* Grades: id, enrollment_id, grade
* Schedules: id, course_id, faculty_id, day, time
* Payments: id, student_id, amount, status, date
* Use SQLite for development (or PostgreSQL/MySQL for deployment).

4. Setup the Project Structure

🛠️ 4. Tech Stack Setup

* Use Flask for the backend.
* Flask-SQLAlchemy for ORM
* Flask-Migrate for database migrations
* Jinja2 for templating
* Optional: Flask-Login for user authentication

🗂️ 5. Implement in Phases

📌 Phase 1: Setup

* Initialize Flask app and configure SQLAlchemy
* Create user login & role-based access

📌 Phase 2: Core Features

* Student CRUD
* Course CRUD
* Faculty CRUD
* Enrollment system
* Grade entry/view

📌 Phase 3:
* Scheduling & Timetables
* Course schedule creation
* Faculty & student views

📌 Phase 4:

* Fees & Payments
* Payment tracking
* Payment status views

📌 Phase 5:

* Reports
* Student transcripts
* Course-wise grade reports

🧪 6. Testing

* Unit testing using pytest
* Manual test cases for all forms, role-based access, and data flows

🚀 7. Deployment (Optional)

* Use Heroku or PythonAnywhere for deployment
* Include .env for secrets and config
* Use gunicorn + nginx if deploying on a VPS
