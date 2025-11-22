@echo off
echo Creating folder structure...

REM ===== Create folders =====
mkdir components
mkdir pages
mkdir styles
mkdir api

REM ===== Create component files =====
type nul > components\Navbar.jsx
type nul > components\Sidebar.jsx
type nul > components\CodeEditor.jsx

REM ===== Create pages =====
type nul > pages\Login.jsx
type nul > pages\Register.jsx
type nul > pages\AdminDashboard.jsx
type nul > pages\CreateAssignment.jsx
type nul > pages\EmployeeDashboard.jsx
type nul > pages\EditorPage.jsx

REM ===== Create styles =====
type nul > styles\global.css
type nul > styles\auth.css
type nul > styles\dashboard.css
type nul > styles\editor.css

REM ===== Create API files =====
type nul > api\auth.js
type nul > api\assignments.js
type nul > api\submissions.js

REM ===== Create main App file =====
type nul > App.jsx

echo Done! Folder + file structure created successfully.
pause
