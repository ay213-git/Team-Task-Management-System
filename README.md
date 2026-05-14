Team Task Management System
A robust Full-Stack web application built with Django, designed to streamline task allocation and management within professional teams. This system ensures complete data isolation and secure workflow management.

 Overview
The system allows users to register, join specific teams, and manage tasks based on their roles. It is built to provide a secure and organized environment for collaborative work, ensuring that each team operates in its own isolated space.

Tech Stack
Backend: Python, Django Web Framework

Database: PostgreSQL (Production) / SQLite (Development)

Frontend: HTML5, CSS3, Bootstrap

Authentication: Django Built-in Auth System

User Roles & Permissions
Every user defines their Team and Role (Manager or Employee) within their profile.

Manager Role
Full Visibility: View all tasks within their specific team.

Task Creation: Add new tasks with title, description, and deadlines.

Maintenance: Edit or delete tasks that haven't been assigned yet.

Employee Role
Team Insight: View all available tasks in their team.

Self-Assignment: Claim unassigned tasks (status changes from "New" to "In Progress").

Status Management: Update the progress of assigned tasks.

Key Features
Data Isolation: Strict separation between teams; users only see their own team's data.

Advanced Filtering: Dashboard with filters for Task Status and Assigned Employees.

Automated Workflow: Logic-driven status changes based on user actions.
<img width="1911" height="920" alt="image" src="https://github.com/user-attachments/assets/cef54085-0aad-410a-8c78-5e132f1f34ef" />
<img width="1901" height="894" alt="image" src="https://github.com/user-attachments/assets/f81c9faf-c90f-4eea-bd5c-da32497cf433" />



Clean Code & DRY: Implemented with a focus on modular architecture and code
<img width="1913" height="940" alt="image" src="https://github.com/user-attachments/assets/f2d9d174-f81a-4649-b70d-89b97ada742c" />
