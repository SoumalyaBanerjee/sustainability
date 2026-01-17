# Sustainability Project - Complete Setup Guide

## Project Overview

This is a full-stack authentication system with:
- **Frontend**: HTML/CSS/JavaScript single-page application
- **Backend**: Python Flask REST API
- **Database**: MongoDB for user data and OTP storage
- **Security**: JWT authentication, bcrypt password hashing, OTP-based password reset

## Project Structure

```
sustainability/
├── frontend/                    # Frontend application
│   ├── public/
│   │   ├── index.html          # Main HTML
│   │   ├── styles.css          # Styling
│   │   ├── api.js              # API communication
│   │   └── app.js              # Application logic
│   └── README.md               # Frontend docs
│
├── backend/                     # Backend API
│   ├── app/
│   │   ├── routes/             # API endpoints
│   │   ├── models/             # MongoDB models
│   │   ├── services/           # Business logic
│   │   ├── utils/              # Utilities
│   │   ├── db/                 # Database
│   │   ├── __init__.py         # App factory
│   │   └── config.py           # Configuration
│   ├── run.py                  # Entry point
│   ├── requirements.txt        # Dependencies
│   ├── .env.example           # Environment template
│   └── README.md              # Backend docs
│
├── config/                     # Project configuration
├── docs/                       # Documentation
├── scripts/                    # Utility scripts
├── tests/                      # Tests
├── src/                        # Main package
├── README.md                   # This file
├── LICENSE                     # MIT License
└── .gitignore                 # Git exclusions
```

## Prerequisites

- Python 3.9 or higher
- Node.js (optional, for any frontend build tools)
- MongoDB (local installation or MongoDB Atlas account)
- Git

## Quick Start

### 1. Backend Setup

#### Install Backend Dependencies
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

#### Configure Environment
```bash
cp .env.example .env
```

Edit `.env` with your configuration:
```env
MONGODB_URI=mongodb://localhost:27017
MONGODB_DB_NAME=sustainability_db
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-key-here
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_EMAIL=your-email@gmail.com
SMTP_PASSWORD=your-app-password
```

#### Start Backend Server
```bash
python run.py
```

Backend will be available at: `http://localhost:5000`

### 2. Frontend Setup

#### Open Frontend in Browser
Simply open `frontend/public/index.html` in your web browser, or serve it with a local server:

```bash
# Using Python
cd frontend/public
python -m http.server 8000

# Or using Node.js http-server
npx http-server
```

Frontend will be available at: `http://localhost:8000` (or as configured)

## Features

### User Registration
- Email-based registration
- Password strength validation:
  - Minimum 8 characters
  - At least one uppercase letter
  - At least one lowercase letter
  - At least one digit
  - At least one special character
- Real-time password requirement feedback

### User Login
- Email and password authentication
- JWT token generation
- Session persistence in local storage
- Automatic redirect to dashboard on login

### Password Reset
- Two-step process:
  1. Request OTP to registered email
  2. Verify OTP and set new password
- 6-digit OTP with 10-minute expiry
- Password strength validation on reset

## API Endpoints Summary

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login and get JWT token
- `POST /api/auth/request-password-reset` - Request password reset OTP
- `POST /api/auth/reset-password` - Reset password with OTP
- `GET /api/auth/me` - Get current user info (requires JWT)
- `GET /api/auth/health` - Health check

### User
- `GET /api/user/profile` - Get user profile (requires JWT)

## Database Configuration

### MongoDB Setup (Local)

#### Windows
```powershell
# Download from: https://www.mongodb.com/try/download/community
# Install MongoDB Community Edition
# Start MongoDB service
net start MongoDB
```

#### Mac
```bash
brew tap mongodb/brew
brew install mongodb-community
brew services start mongodb-community
```

#### Linux
```bash
sudo apt-get install -y mongodb
sudo systemctl start mongodb
```

### MongoDB Atlas (Cloud)

1. Go to https://www.mongodb.com/cloud/atlas
2. Create account and cluster
3. Get connection string
4. Update `MONGODB_URI` in `.env`

## Email Configuration

### Gmail Setup (for OTP emails)

1. Enable 2-factor authentication on your Google account
2. Generate app-specific password: https://myaccount.google.com/apppasswords
3. Use the app password in `.env`:
   ```env
   SMTP_EMAIL=your-email@gmail.com
   SMTP_PASSWORD=your-app-specific-password
   ```

## Folder Segregation Explanation

### Frontend (`/frontend`)
- Contains all user interface code
- Independent of backend
- Can be hosted separately
- Uses CORS to communicate with backend

### Backend (`/backend`)
- REST API for all operations
- Handles authentication and business logic
- MongoDB integration
- Can serve multiple frontend applications

### Database (`MongoDB`)
- Stores user accounts
- Stores OTP records
- Automatic OTP cleanup via TTL indexes

## Development Workflow

1. **Start MongoDB** (if running locally)
2. **Start Backend**: `cd backend && python run.py`
3. **Open Frontend**: Open `frontend/public/index.html` in browser or serve locally
4. **Test API**: Use Postman or the frontend application

## Testing

### Using the Frontend
1. Register a new account
2. Login with your credentials
3. Test password reset (check console for OTP simulation messages)

### Using Postman
Import and test API endpoints directly:
```
POST http://localhost:5000/api/auth/register
POST http://localhost:5000/api/auth/login
POST http://localhost:5000/api/auth/request-password-reset
POST http://localhost:5000/api/auth/reset-password
```

## Security Considerations

✅ **Implemented:**
- Bcrypt password hashing (12 rounds)
- JWT token authentication
- CORS enabled
- Input validation
- OTP-based password recovery
- Password strength requirements
- Rate limiting (can be added)
- HTTPS recommended for production

⚠️ **For Production:**
- Change all SECRET_KEYS to strong random values
- Use HTTPS only
- Implement rate limiting
- Add request validation middleware
- Enable CORS for specific domains
- Use environment-specific configurations
- Add logging and monitoring

## Troubleshooting

### MongoDB Connection Error
```
Error: Failed to connect to MongoDB
```
**Solution**: Ensure MongoDB is running on `localhost:27017` or update `MONGODB_URI` in `.env`

### CORS Error in Frontend
```
Access to XMLHttpRequest blocked by CORS
```
**Solution**: Ensure backend is running and `API_BASE_URL` in `frontend/public/api.js` is correct

### Email OTP Not Received
```
Failed to send OTP email
```
**Solution**: Check SMTP configuration in `.env`, ensure 2FA and app passwords are correctly set

### Port Already in Use
```
Port 5000 is already in use
```
**Solution**: Change port in environment or kill existing process

## Next Steps

1. ✅ User authentication system is ready
2. Extend with additional user features (profile, preferences)
3. Add role-based access control (RBAC)
4. Implement refresh tokens for session management
5. Add 2FA (two-factor authentication)
6. Build admin dashboard
7. Add email verification on registration

## Support & Documentation

- Backend API docs: See `backend/README.md`
- Frontend docs: See `frontend/README.md`
- Configuration: See `.env.example` files
- Postman collection: (To be created)

## License

MIT License - See LICENSE file for details

---

**Created**: January 17, 2026
**Status**: Initial authentication system ready for deployment
