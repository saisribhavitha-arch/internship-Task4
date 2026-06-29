# internship-Task4
# Secure Login Web Application

A lightweight, secure user authentication web application built using Python and the Flask framework. This project demonstrates essential web security best practices, including safe password storage, robust session management, and robust protection against common vulnerabilities like SQL Injection.

## Features

* **Secure User Registration & Login:** Enforces minimum credential standards and handles authentication logic safely.
* **Cryptographic Password Hashing:** Utilizes **bcrypt** to salt and hash user passwords before database storage, ensuring passwords are never saved in plaintext.
* **SQL Injection (SQLi) Protection:** Developed using **SQLAlchemy ORM** parameterized queries, natively neutralizing malicious SQL injection payloads.
* **Secure Session Management:** Implements securely signed Flask session state tracking with a functional **Logout** feature to explicitly destroy active sessions.
* **Modern UI:** Features a clean, single-file styled interface with responsive visual alert cues (flash messages) for success and error handling.

##  Tech Stack

* **Language:** Python 3.12+
* **Framework:** Flask
* **Database ORM:** Flask-SQLAlchemy (SQLite)
* **Security/Hashing:** Flask-Bcrypt


