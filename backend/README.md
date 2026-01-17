<!-- Backend Documentation -->
# Backend API Documentation

## Overview
Flask-based REST API for user authentication with MongoDB integration.

## Architecture

```
backend/
├── app/
│   ├── routes/          # API endpoints
│   │   ├── auth.py      # Authentication routes
│   │   └── user.py      # User profile routes
│   ├── models/          # MongoDB models
│   │   ├── user.py      # User model
│   │   └── otp.py       # OTP model
│   ├── services/        # Business logic
│   │   └── auth_service.py
│   ├── utils/           # Utility functions
│   │   ├── password.py      # Password hashing/verification
│   │   ├── email.py         # Email sending
│   │   ├── validators.py    # Input validation
│   │   └── otp_generator.py # OTP generation
│   ├── db/              # Database connection
│   │   └── mongo.py     # MongoDB connection management
│   ├── __init__.py      # Flask app factory
│   └── config.py        # Configuration
├── run.py               # Entry point
└── requirements.txt     # Dependencies
```

## Installation & Setup

### Prerequisites
- Python 3.9+
- MongoDB (local or remote)
- Virtual environment

### 1. Create Virtual Environment
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Environment
```bash
cp .env.example .env
# Edit .env with your configuration
```

**Required Configuration:**
```env
# MongoDB
MONGODB_URI=mongodb://localhost:27017
MONGODB_DB_NAME=sustainability_db

# Flask
FLASK_ENV=development
SECRET_KEY=your-secret-key

# JWT
JWT_SECRET_KEY=your-jwt-secret-key

# Email (for OTP)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_EMAIL=your-email@gmail.com
SMTP_PASSWORD=your-app-specific-password
```

### 4. Run the Server
```bash
python run.py
```

Server will start on `http://localhost:5000`

## API Endpoints

### Authentication Routes

#### Register User
```
POST /api/auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "SecurePass123!"
}

Response:
{
  "success": true,
  "message": "User registered successfully",
  "user_id": "...",
  "email": "user@example.com"
}
```

#### Login User
```
POST /api/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "SecurePass123!"
}

Response:
{
  "success": true,
  "message": "Login successful",
  "access_token": "eyJ0eXAiOiJKV1QiLC...",
  "user": {
    "id": "...",
    "email": "user@example.com",
    "is_active": true,
    "created_at": "2026-01-17T...",
    "updated_at": "2026-01-17T..."
  }
}
```

#### Request Password Reset
```
POST /api/auth/request-password-reset
Content-Type: application/json

{
  "email": "user@example.com"
}

Response:
{
  "success": true,
  "message": "If the email exists, an OTP will be sent"
}
```

#### Reset Password with OTP
```
POST /api/auth/reset-password
Content-Type: application/json

{
  "email": "user@example.com",
  "otp": "123456",
  "new_password": "NewSecurePass123!"
}

Response:
{
  "success": true,
  "message": "Password reset successfully"
}
```

#### Get Current User (Requires JWT)
```
GET /api/auth/me
Authorization: Bearer <token>

Response:
{
  "success": true,
  "user": {
    "id": "...",
    "email": "user@example.com",
    "is_active": true,
    "created_at": "2026-01-17T...",
    "updated_at": "2026-01-17T..."
  }
}
```

#### Get User Profile (Requires JWT)
```
GET /api/user/profile
Authorization: Bearer <token>

Response:
{
  "success": true,
  "user": {...}
}
```

### Health Check
```
GET /api/auth/health

Response:
{
  "status": "healthy",
  "service": "auth-service"
}
```

## Password Requirements
Passwords must contain:
- At least 8 characters
- At least one lowercase letter
- At least one uppercase letter
- At least one digit
- At least one special character (!@#$%^&*)

## OTP Configuration
- OTP Length: 6 digits
- OTP Expiry: 10 minutes (configurable)
- OTP Delivery: Email

## Security Features
- Password hashing with bcrypt (12 rounds)
- JWT token authentication
- OTP-based password reset
- CORS enabled for frontend communication
- Input validation and sanitization
- Password strength validation

## MongoDB Collections

### Users Collection
```javascript
{
  "_id": ObjectId,
  "email": String (unique),
  "password": String (hashed),
  "is_active": Boolean,
  "created_at": Date,
  "updated_at": Date
}
```

### OTPs Collection
```javascript
{
  "_id": ObjectId,
  "email": String,
  "code": String (6 digits),
  "is_used": Boolean,
  "created_at": Date,
  "expires_at": Date (TTL index)
}
```

## Error Handling
All responses include a `success` boolean field and `message` field.

## Development Notes
- The app uses Flask blueprints for modular routes
- MongoDB connection is managed as a singleton
- Services contain business logic separate from routes
- Utilities are organized by functionality
- Configuration is environment-based

## Testing
To test endpoints, use:
- Postman
- cURL
- Frontend application

Example with cURL:
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"Pass123!"}'
```
