# 📋 University Management System – Project Plan (Translated + Checkboxes)

---

## 1. 🎯 Project Goal
Create a complex university management system that includes:

- [ ] User authentication and registration for students and lecturers
- [ ] CRUD operations for modules (courses)
- [ ] Administration panel for managing users, modules, programs, groups, and relationships
- [ ] Database integration with migrations
- [ ] Extra functionality: image upload, input validation, security mechanisms, error handling

---

## 2. 🔐 User Authentication & Registration

### 2.1 Registration
- [ ] Registration available only to students and lecturers
- [ ] Select study program during registration
- [ ] Assign student group based on selected program
- [ ] Validate email and password using regex
- [ ] Upload profile picture (file type & size validation)
- [ ] Save image reference in DB and store image in a dedicated folder

### 2.2 Login
- [ ] Temporary block after 3 failed login attempts

### 2.3 Roles and Permissions
- [ ] **Students**:
  - [ ] View assigned modules
  - [ ] View academic info (program, group)
  - [ ] View personal schedule (lectures, exams, assignments)
- [ ] **Lecturers**:
  - [ ] Create/edit modules (semester, times, requirements)
  - [ ] Assign and manage assessments
  - [ ] Track student progress and attendance
- [ ] **Admins**:
  - [ ] Full control over users, modules, programs, and groups
  - [ ] Manage complex relationships (e.g., module ⇄ lecturer ⇄ program)

---

## 3. 📚 Module (Course) Management

### 3.1 CRUD
- [ ] Create module with name, description, credits, semester
- [ ] Set lecture times, assessment dates, exam dates (optional)
- [ ] Specify prerequisite modules (Bonus)
- [ ] Update module info and schedule
- [ ] View full module info, related lecturers, enrolled students
- [ ] Delete module with confirmation

### 3.2 Student Course Selection
- [ ] Students choose modules based on their program
- [ ] Add selected modules to personal calendar
- [ ] Check for prerequisites and schedule conflicts

### 3.3 Lecturer Assessment Management
- [ ] Set assessment dates integrated into calendar
- [ ] Edit or cancel scheduled assessments

---

## 4. 🧪 Extra Functionality: Tests (Bonus)
- [ ] Lecturers can create tests linked to modules/exams
- [ ] Students can take tests; results contribute to module grade
- [ ] Tests integrated into system with validation, security, error handling

---

## 5. 🛠️ Admin Management Panel

### 5.1 Dashboard
- [ ] Show system statistics (users, modules, programs, groups)
- [ ] All actions wrapped in try-except for error logging

### 5.2 User Administration
- [ ] Manage user roles and program assignments
- [ ] Deactivate/delete accounts
- [ ] Edit user relationships (e.g., group changes)

### 5.3 Module Administration
- [ ] Edit module info, semester, prerequisites, schedules
- [ ] Assign/change lecturers
- [ ] Link modules to study programs

---

## 6. 🧱 DB Integration & Migrations

### 6.1 SQLAlchemy Models
- [ ] Users (role, program, group)
- [ ] Modules (details, schedule, prerequisites)
- [ ] Groups (auto-assigned based on program)
- [ ] Assessments (dates, descriptions, linked module)
- [ ] Tests (Bonus: questions, answers, module/exam links)

### 6.2 Migrations
- [ ] Use Flask-Migrate for schema changes
- [ ] Preserve data during migration

### 6.3 Error Handling
- [ ] All DB operations wrapped in try-except

---

## 7. ➕ Additional Features

### 7.1 Image Uploads
- [ ] Profile pictures in user accounts
- [ ] Illustrations/images in module descriptions (Bonus)

### 7.2 Complex Relationships & Academic Structure
- [ ] Ensure each module is tied to a specific study program
- [ ] Introduce faculties; programs belong to faculties
- [ ] Students and modules belong to a faculty (Bonus)
- [ ] Support prerequisite modules (Bonus)
- [ ] Course registration based on program, semester, and schedule compatibility

---

## 8. ⚙️ Technical Requirements

### Try-Except Everywhere
- [ ] Use try-except in all parts (auth, registration, modules, tests, admin) with clear error messages

### Data Persistence
- [ ] All data must be stored in a persistent DB (any DB allowed)

### Project Structure
- [ ] Separate folders: `static`, `templates`, `controllers`, `services`, `crud`

### Validation Rules
- [ ] Cannot register to modules at overlapping times
- [ ] Module credits cannot be negative

### GitHub Workflow
- [ ] Use branches: `main`, `development`, `feature/*`
- [ ] At least 10 commits per team
- [ ] No direct commits to main (simulate protection)
- [ ] Create pull requests for merges

### Task Management
- [ ] Use platforms like JIRA for tracking tasks

### Migration Usage
- [ ] Use `Flask-Migrate` to safely evolve DB schema

---

## 9. 🧾 Group Code Structure Explanation (e.g., IFIN-18-A)
- **IFIN** – Abbreviation for the study program (e.g., Informatics)
- **18** – Year of admission or course number
- **A** – Group identifier (A, B, C, etc.)