# Sustainability Project

A full-stack user authentication system with segregated frontend, backend, and MongoDB integration. Built with Flask, JavaScript, and MongoDB Atlas.

## 🎯 Project Overview

This project implements a complete authentication system featuring:
- **User Registration** with password strength validation
- **User Login** with JWT token-based authentication
- **Password Reset** using OTP (One-Time Password) via email
- **Segregated Architecture** with independent frontend and backend

## 📁 Project Structure

```
sustainability/
├── frontend/                # Frontend UI (HTML/CSS/JS)
│   ├── public/
│   │   ├── index.html       # Login, Register, Password Reset forms
│   │   ├── styles.css       # Responsive styling
│   │   ├── api.js           # API client
│   │   └── app.js           # Frontend logic
│   └── README.md
│
├── backend/                 # REST API Server (Flask/Python)
│   ├── app/
│   │   ├── routes/          # API endpoints (auth, user)
│   │   ├── models/          # MongoDB models (users, OTPs)
│   │   ├── services/        # Business logic
│   │   ├── utils/           # Utilities (password, email, validators)
│   │   ├── db/              # Database connection
│   │   ├── __init__.py      # Flask app factory
│   │   └── config.py        # Configuration
│   ├── run.py               # Backend entry point
│   ├── requirements.txt     # Dependencies
│   ├── .env.example        # Environment template
│   └── README.md
│
├── tests/                   # Testing & utilities
│   ├── check_mongodb.py     # MongoDB connection test
│   └── test_core.py
│
├── docs/                    # Documentation
├── scripts/                 # Utility scripts
├── config/                  # Configuration files
├── SETUP_GUIDE.md          # Complete setup guide
├── requirements.txt         # Root dependencies
├── pyproject.toml          # Python project config
└── README.md               # This file
```

## ✨ Key Features

### Authentication System
- ✅ **User Registration** - Email-based signup with password strength validation
- ✅ **User Login** - JWT token generation and session management
- ✅ **Password Reset** - Two-step OTP verification process
- ✅ **Password Hashing** - Bcrypt with 12 rounds of salting
- ✅ **Email OTP Delivery** - Automated OTP sending via SMTP

### Frontend Features
- ✅ **Responsive Design** - Mobile-friendly UI
- ✅ **Real-time Validation** - Live password requirement feedback
- ✅ **Local Storage** - JWT token persistence
- ✅ **Error Handling** - User-friendly error messages
- ✅ **Form Switching** - Smooth transitions between login/register/reset forms
- ✅ **Dashboard** - Post-login user information display

### Backend Features
- ✅ **RESTful API** - Clean endpoint design
- ✅ **JWT Authentication** - Secure token-based auth
- ✅ **CORS Enabled** - Frontend-backend communication
- ✅ **MongoDB Integration** - Cloud Atlas support
- ✅ **Input Validation** - Email, password, OTP validation
- ✅ **Error Handling** - Consistent error responses
- ✅ **Logging** - Detailed application logs

### Database (MongoDB)
- ✅ **Collections** - Separate users and OTP records
- ✅ **TTL Indexes** - Automatic OTP expiration
- ✅ **Unique Constraints** - Email uniqueness enforcement
- ✅ **Cloud Hosted** - MongoDB Atlas integration

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- MongoDB Atlas account (free)
- Modern web browser

### Backend Setup
```bash
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1        # Windows
# source venv/bin/activate          # Mac/Linux

pip install -r requirements.txt
cp .env.example .env
# Edit .env with your MongoDB URI and SMTP config

python run.py                       # Runs on http://localhost:5000
```

### Frontend Setup
```bash
cd frontend/public
python -m http.server 8000          # Runs on http://localhost:8000
```

**Open browser to: http://localhost:8000**

## 📊 API Endpoints

### Authentication Routes
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `POST /api/auth/request-password-reset` - Request OTP
- `POST /api/auth/reset-password` - Reset password with OTP
- `GET /api/auth/me` - Get current user (JWT required)
- `GET /api/auth/health` - Health check

### User Routes
- `GET /api/user/profile` - Get user profile (JWT required)

## 🔧 Testing

### Check MongoDB Users
```bash
python tests/check_mongodb.py
```

### Test API Endpoints
Use Postman or the frontend application to test all endpoints.

## 📚 Documentation

- **Complete Setup**: See [SETUP_GUIDE.md](SETUP_GUIDE.md)
- **Backend Docs**: See [backend/README.md](backend/README.md)
- **Frontend Docs**: See [frontend/README.md](frontend/README.md)

## 🔐 Security Features

- ✅ Bcrypt password hashing (12 rounds)
- ✅ JWT token authentication
- ✅ CORS protection
- ✅ Input validation & sanitization
- ✅ OTP-based password recovery
- ✅ Password strength requirements
- ✅ HTTPS ready for production

## 🛠️ Technologies Used

- **Backend**: Flask, Python, PyMongo
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Database**: MongoDB Atlas
- **Security**: bcrypt, JWT, CORS
- **Email**: SMTP (Gmail compatible)

## 🎓 Password Requirements

- Minimum 8 characters
- At least one uppercase letter (A-Z)
- At least one lowercase letter (a-z)
- At least one digit (0-9)
- At least one special character (!@#$%^&*)

## 📋 Environment Variables

### Backend (.env)
```env
# MongoDB
MONGODB_URI=mongodb+srv://user:pass@cluster.mongodb.net/db
MONGODB_DB_NAME=sustainability_db

# Flask
FLASK_ENV=development
SECRET_KEY=your-secret-key

# JWT
JWT_SECRET_KEY=your-jwt-secret-key

# Email
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_EMAIL=your-email@gmail.com
SMTP_PASSWORD=your-app-password
```

## 🧪 Development

### Running Tests

```bash
pytest
pytest --cov=src/sustainability  # With coverage
```

### Code Quality

```bash
# Format code
black src/ tests/

# Sort imports
isort src/ tests/

# Lint code
flake8 src/ tests/
pylint src/

# Type checking
mypy src/
```

### MongoDB Tests

```bash
python tests/check_mongodb.py
```

## 📚 Documentation

- [SETUP_GUIDE.md](SETUP_GUIDE.md) - Complete setup instructions
- [backend/README.md](backend/README.md) - Backend API documentation
- [frontend/README.md](frontend/README.md) - Frontend documentation

## 🤝 Contributing

1. Create a feature branch (`git checkout -b feature/amazing-feature`)
2. Commit changes (`git commit -m 'Add amazing feature'`)
3. Push to branch (`git push origin feature/amazing-feature`)
4. Open a Pull Request

## 📝 License

MIT License - See [LICENSE](LICENSE) file for details

## 🎯 Next Steps

- [ ] Add email verification on registration
- [ ] Implement 2FA (two-factor authentication)
- [ ] Add refresh tokens for session management
- [ ] Build admin dashboard
- [ ] Add role-based access control (RBAC)
- [ ] Implement rate limiting
- [ ] Add API documentation (Swagger/OpenAPI)

## 📞 Support

For issues and questions, please open an issue on GitHub.

---

**Created**: January 18, 2026  
**Status**: ✅ Authentication system ready for deployment  
**Version**: 1.0.0
