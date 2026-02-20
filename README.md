# Hotel Management API 🏨

A robust, secure backend built with **FastAPI** for managing hotel operations. This API implements industry-standard security practices, including password hashing and JWT-based authentication.

## ✨ Features
- **FastAPI**: Modern, high-performance web framework for building APIs.
- **SQLAlchemy**: Powerful SQL toolkit and Object Relational Mapper (ORM).
- **JWT Authentication**: Secure user sessions using `python-jose`.
- **Password Hashing**: Uses `bcrypt` for secure credential storage.
- **Environment Management**: Configuration handled via `.env` files for security.

---

## 🛠️ Setup & Installation

### 1. Clone the repository
git clone [https://github.com/firesoul46/PRODIGY_BWD_05.git]
cd PRODIGY_BWD_05
2. Create a Virtual Environment
python -m venv venv
# Activate on Windows:
venv\Scripts\activate
# Activate on Mac/Linux:
source venv/bin/activate
3. Install Dependencies
python -m pip install fastapi uvicorn sqlalchemy python-jose[cryptography] bcrypt python-dotenv
4. Configure Environment Variables
Create a file named .env in the root directory and add your secret key:Code snippetSECRET_KEY=your_super_secret_key_here
(Note: Never commit your real .env file to GitHub!)
🚦 UsageStart the ServerBashpython -m uvicorn main:app --reload
API DocumentationOnce the server is running, you can access the interactive API docs at:Swagger UI: http://127.0.0.1:8000/docsReDoc: http://127.0.0.1:8000/redoc🔒 EndpointsMethodEndpointDescriptionPOST/registerCreate a new user account with a hashed password.POST/loginAuthenticate user and receive a JWT access token.GET/Root health check.
📁 Project StructurePlaintexthotel_api/
├── venv/             # Virtual environment
├── .env              # Private secrets (ignored by git)
├── .gitignore        # Files to exclude from GitHub
├── main.py           # API routes and application logic
├── auth.py           # Security and JWT logic
├── models.py         # SQLAlchemy database models
├── database.py       # Database connection setup
├── README.md         # Project documentation
└── hotel.db          # Local SQLite database
🛡️ Security
This project follows security best practices:No Secrets in Code: All sensitive data is stored in environment variables.Secure Hashing: Passwords are never stored in plain text; they are salted and hashed using bcrypt.Integrity: Database ensures unique email constraints to prevent duplicate accounts.
