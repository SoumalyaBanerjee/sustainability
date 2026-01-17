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

## � Understanding the Complete Flow

### Overview
This section explains how data flows from the frontend through the backend to the database for every user action. Follow along to understand how the authentication system works end-to-end.

### 1️⃣ Registration Flow

**User Action**: User enters email, password, and clicks "Register"

```
FRONTEND (index.html)
    ↓
    └─→ app.js validates password strength
        ├─ Check: 8+ chars, uppercase, lowercase, digit, special char
        └─ If invalid → Show error, stop
        
        If valid → Sends POST to /api/auth/register with:
        {
          "email": "user@example.com",
          "password": "SecurePass123!"
        }
        
BACKEND (routes/auth.py)
    ↓
    └─→ Receives registration request
        ├─ Validates input using utils/validators.py
        ├─ Checks if email already exists in db.users
        └─ If exists → Return error "Email already registered"
        
        If new email:
        ├─ Hash password using utils/password.py (bcrypt, 12 rounds)
        │  Result: $2b$12$...(hashed)
        ├─ Call services/auth_service.py → register_user()
        └─ Create user in MongoDB:
            {
              email: "user@example.com",
              password: "$2b$12$...",
              is_active: true,
              is_verified: false,        ← NOT YET VERIFIED
              two_factor_enabled: false,
              created_at: 2026-01-18T...
            }
        
DATABASE (MongoDB Atlas)
    ↓
    └─→ User inserted into db.users collection
        
        CREATE VERIFICATION TOKEN:
        ├─ Generate 32-byte secure token
        ├─ Set expiry to 24 hours
        └─ Insert into db.email_verifications:
            {
              email: "user@example.com",
              token: "secure_token_here",
              is_verified: false,
              expires_at: 2026-01-19T...  ← TTL index auto-deletes
            }
        
SEND EMAIL:
    └─→ utils/email.py → send_verification_email()
        ├─ Connect to SMTP server
        └─ Send link: http://localhost:8000?verify=secure_token_here

FRONTEND (receives response)
    └─→ Display: "Check your email to verify!"
        └─ User receives email and clicks link
```

### 2️⃣ Email Verification Flow

**User Action**: User clicks verification link in email

```
FRONTEND (index.html)
    ↓
    └─→ app.js detects URL parameter ?token=secure_token_here
        ├─ Extracts token
        └─ Sends POST to /api/auth/verify-email with:
            { "token": "secure_token_here" }

BACKEND (routes/auth.py)
    ↓
    └─→ Receives verification request
        ├─ Query: db.email_verifications.findOne({token: "..."})
        ├─ If not found or expired → Return error
        ├─ If valid → Call services/auth_service.py → verify_email()
        │
        └─→ UPDATE USER:
            ├─ Query: db.users.findOne({email: "user@example.com"})
            ├─ Update: db.users.updateOne(
            │     {_id: user_id},
            │     {$set: {is_verified: true}}
            │   )
            │
            └─→ MARK TOKEN AS VERIFIED:
                └─ db.email_verifications.updateOne(
                     {token: "..."},
                     {$set: {is_verified: true}}
                   )

FRONTEND (receives response)
    └─→ Display: "Email verified! You can now login."
        └─ User proceeds to login
```

### 3️⃣ Login Flow

**User Action**: User enters email, password, and clicks "Login"

```
FRONTEND (index.html)
    ↓
    └─→ app.js → login()
        └─ Sends POST to /api/auth/login with:
            {
              "email": "user@example.com",
              "password": "SecurePass123!"
            }

BACKEND (routes/auth.py)
    ↓
    └─→ Receives login request
        ├─ Call services/auth_service.py → authenticate_user()
        │
        └─→ FIND USER:
            ├─ Query: db.users.findOne({email: "user@example.com"})
            ├─ If not found → Return error "Invalid credentials"
            │
            └─→ CHECK EMAIL VERIFICATION:
                ├─ If is_verified === false
                │  → Return error "Please verify email first"
                │
                └─→ VERIFY PASSWORD:
                    ├─ Compare hashed password using utils/password.py
                    ├─ If not match → Return error "Invalid credentials"
                    │
                    └─→ CHECK 2FA STATUS:
                        ├─ Query: db.two_factor_auth.findOne({user_id: ...})
                        ├─ If two_factor_enabled === true
                        │  → Generate TEMPORARY JWT token
                        │  → Return requires_2fa: true
                        │
                        └─→ GENERATE JWT TOKEN:
                            ├─ Use Flask-JWT-Extended
                            ├─ Include: {user_id, email}
                            ├─ Expire in: 1 hour
                            └─ Return: {
                                 success: true,
                                 access_token: "eyJhbGc...",
                                 user: {user_id, email},
                                 requires_2fa: false
                               }

FRONTEND (receives response)
    ↓
    └─→ Check if requires_2fa === true
        ├─ YES → Show 2FA verification form
        └─ NO → Store JWT and show dashboard
            ├─ localStorage.setItem('authToken', token)
            ├─ localStorage.setItem('user', JSON.stringify(user))
            └─ User is now logged in!
```

### 4️⃣ 2FA Setup Flow (Optional)

**User Action**: User clicks "Enable 2FA" in settings

```
FRONTEND (index.html)
    ↓
    └─→ app.js → setup2FA()
        └─ Sends POST to /api/auth/2fa/setup with:
            Header: Authorization: Bearer eyJhbGc...

BACKEND (routes/auth.py)
    ↓
    └─→ Receives 2FA setup request
        ├─ Extract user_id from JWT token
        └─ Call models/two_factor_auth.py → TwoFactorAuth.generate_secret()
            │
            ├─ Use pyotp library to generate secret:
            │  Result: "JBSWY3DPEBLW64TMMQ======"
            │
            ├─ Create QR provisioning URI:
            │  "otpauth://totp/user@example.com?secret=JBSWY3D..."
            │
            └─ Generate 10 backup codes:
               Each: "BACKUP-CODE-123456"
               
        └─ Return:
            {
              success: true,
              secret: "JBSWY3DPEBLW64TMMQ======",
              provisioning_uri: "otpauth://...",
              backup_codes: ["BACKUP-1", "BACKUP-2", ...]
            }

FRONTEND (receives response)
    ↓
    └─→ Display QR code from provisioning_uri
        ├─ User scans with authenticator app (Google Auth, Authy, etc.)
        ├─ User saves backup codes securely
        └─ User enters 6-digit code from authenticator
            └─ Sends POST to /api/auth/2fa/verify with:
                {
                  "secret": "JBSWY3DPEBLW64TMMQ======",
                  "code": "123456",
                  "backup_codes": ["BACKUP-1", ...]
                }

BACKEND (routes/auth.py)
    ↓
    └─→ Receives 2FA verification request
        ├─ Extract user_id from JWT token
        ├─ Verify 6-digit code using models/two_factor_auth.py
        │  → pyotp.verify_totp(secret, code)
        │  → Check with 30-second time window
        │  ├─ If match → Code valid
        │  └─ If not match → Return error
        │
        └─→ IF VALID:
            ├─ INSERT into db.two_factor_auth:
            │  {
            │    user_id: ObjectId(...),
            │    secret: "JBSWY3DPEBLW64TMMQ======",
            │    is_enabled: true,
            │    backup_codes: [hashed_code1, hashed_code2, ...],
            │    used_backup_codes: [],
            │    created_at: 2026-01-18T...
            │  }
            │
            └─→ UPDATE db.users:
                {
                  _id: user_id,
                  two_factor_enabled: true
                }

FRONTEND (receives response)
    └─→ Display: "2FA enabled successfully!"
        └─ Backup codes available for download
```

### 5️⃣ Login WITH 2FA Enabled

**Same as Step 3️⃣ LOGIN, but with 2FA check:**

```
After password verified:

BACKEND checks:
    └─→ Query db.two_factor_auth for user
        ├─ If two_factor_enabled === true
        ├─ Generate TEMPORARY JWT token (limited scope)
        └─ Return: {
             success: true,
             access_token: "temporary_jwt_token",
             requires_2fa: true
           }

FRONTEND:
    └─→ Show 2FA code input form
        ├─ User enters 6-digit code from authenticator
        │  OR enters one of backup codes
        └─ Sends POST to /api/auth/2fa/verify-code with:
            {
              "access_token": "temporary_jwt_token",
              "code": "123456",
              "use_backup": false
            }

BACKEND:
    ↓
    └─→ Verify code using models/two_factor_auth.py
        ├─ pyotp.verify_totp(secret, code)
        │  OR check backup code list
        ├─ If backup code used → Move to used_backup_codes
        └─ If valid:
            └─→ Generate FULL JWT token (unrestricted)
                └─ Return: {
                     success: true,
                     access_token: "full_jwt_token",
                     user: {user_id, email}
                   }

FRONTEND:
    └─→ Store token in localStorage
        ├─ localStorage.setItem('authToken', full_token)
        └─ Show dashboard - User fully logged in!
```

### 6️⃣ Token Refresh Flow

**Automatically happens**: When token about to expire

```
FRONTEND (background timer)
    ↓
    └─→ app.js checks token expiry
        ├─ When 50 minutes have passed → Refresh
        └─ Sends POST to /api/session/refresh with:
            Header: Authorization: Bearer eyJhbGc...

BACKEND (routes/session.py)
    ↓
    └─→ Receives refresh request
        ├─ Extract user_id from current JWT token
        ├─ Verify token is still valid
        └─ Generate NEW JWT token with same user_id
            └─ Expire in: 1 hour from now
            └─ Return: {
                 success: true,
                 access_token: "new_jwt_token"
               }

FRONTEND:
    └─→ Update stored token
        ├─ localStorage.setItem('authToken', new_token)
        └─ User stays logged in without re-entering credentials!
```

### 7️⃣ Logout Flow

**User Action**: User clicks "Logout" button

```
FRONTEND (index.html)
    ↓
    └─→ app.js → logout()
        ├─ Get JWT token from localStorage
        ├─ Send POST to /api/session/logout (optional):
        │  Header: Authorization: Bearer eyJhbGc...
        │
        └─→ Clear all session data:
            ├─ localStorage.removeItem('authToken')
            ├─ localStorage.removeItem('user')
            ├─ localStorage.removeItem('tempToken')
            └─ Switch to login form

BACKEND (routes/session.py)
    ↓
    └─→ Receives logout request
        ├─ Extract user_id from JWT (optional logging)
        └─ Return: {success: true}
        
NOTE: JWT tokens are stateless - no server session to delete
      Old tokens still valid until expiry, but frontend cleared

USER STATE: ✅ Logged out
    └─→ Must login again to access dashboard
```

---

### 📊 Data Flow Diagram

```
┌─────────────┐         ┌──────────────────┐        ┌──────────────┐
│  FRONTEND   │         │     BACKEND      │        │  MONGODB     │
│ (Browser)   │         │  (Flask Server)  │        │  (Cloud)     │
└──────┬──────┘         └────────┬─────────┘        └──────┬───────┘
       │                         │                         │
       │─ Register ─────────────→│                         │
       │                         │─ Validate ──────────────│
       │                         │─ Create User ──────────→│
       │                         │                         │
       │ ← Response ─────────────│                         │
       │ (Email Verification)    │                         │
       │                         │─ Create Token ────────→│
       │                         │                         │
       │─ Click Email Link ─────→│                         │
       │                         │─ Verify Token ────────→│
       │                         │─ Update User ─────────→│
       │ ← Verification OK ──────│                         │
       │                         │                         │
       │─ Login ────────────────→│                         │
       │                         │─ Find User ───────────→│
       │                         │← User Data ───────────│
       │                         │─ Verify Password ─────→│
       │ ← JWT Token ───────────│ ← Password OK ────────|
       │ (Stored in Storage)     │                         │
       │                         │                         │
       │─ API Call + JWT ───────→│ (Authenticated)        │
       │ (All subsequent requests)                        │
       │                         │                         │
       │─ Logout ──────────────→│                         │
       │ (Clear LocalStorage)    │                         │
       │                         │                         │
```

---

### 🔐 Security in Each Step

| Step | Security Measure |
|------|-----------------|
| **Registration** | Password hashing (bcrypt), input validation, email uniqueness check |
| **Email Verification** | 32-byte secure token, 24-hour expiry, TTL index auto-deletion |
| **Password Storage** | bcrypt with 12 salt rounds |
| **Login** | Email verification check, password comparison, JWT generation |
| **JWT Tokens** | HMAC-SHA256 signing, 1-hour expiry, stateless design |
| **2FA** | TOTP time-based codes, 30-second window, backup codes (one-time use) |
| **Token Refresh** | Requires valid existing token, new token issued with new expiry |
| **Logout** | LocalStorage cleared, frontend session terminated |

---

## �📚 Documentation

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
