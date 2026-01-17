// Local Storage Keys
const STORAGE_KEYS = {
    TOKEN: 'auth_token',
    USER: 'user_info',
    FORGOT_EMAIL: 'forgot_email'
};

// Password validation patterns
const PASSWORD_PATTERNS = {
    length: /.{8,}/,
    lowercase: /[a-z]/,
    uppercase: /[A-Z]/,
    number: /[0-9]/,
    special: /[!@#$%^&*(),.?":{}|<>]/
};

// Utility Functions
function showMessage(elementId, message, type = 'error') {
    const element = document.getElementById(elementId);
    if (element) {
        element.textContent = message;
        element.className = `message show ${type}`;
    }
}

function hideMessage(elementId) {
    const element = document.getElementById(elementId);
    if (element) {
        element.className = 'message';
    }
}

function showError(elementId, message) {
    const element = document.getElementById(elementId);
    if (element) {
        element.textContent = message;
        element.classList.add('show');
    }
}

function hideError(elementId) {
    const element = document.getElementById(elementId);
    if (element) {
        element.textContent = '';
        element.classList.remove('show');
    }
}

function switchForm(formId) {
    // Hide all forms
    document.querySelectorAll('.form-section').forEach(form => {
        form.classList.remove('active');
    });
    // Show selected form
    document.getElementById(formId).classList.add('active');
}

function clearForm(formId) {
    const form = document.getElementById(formId);
    if (form) {
        form.reset();
    }
}

function setToken(token) {
    localStorage.setItem(STORAGE_KEYS.TOKEN, token);
}

function getToken() {
    return localStorage.getItem(STORAGE_KEYS.TOKEN);
}

function setUserInfo(user) {
    localStorage.setItem(STORAGE_KEYS.USER, JSON.stringify(user));
}

function getUserInfo() {
    const user = localStorage.getItem(STORAGE_KEYS.USER);
    return user ? JSON.parse(user) : null;
}

function logout() {
    localStorage.removeItem(STORAGE_KEYS.TOKEN);
    localStorage.removeItem(STORAGE_KEYS.USER);
    // Call logout API
    fetch('http://localhost:5000/api/session/logout', {
        method: 'POST',
        headers: {
            'Authorization': `Bearer ${getToken()}`,
            'Content-Type': 'application/json'
        }
    }).catch(err => console.log('Logout API call completed'));
    
    switchForm('loginForm');
    clearForm('loginFormElement');
    hideMessage('loginMessage');
}

// Password Validation
function validatePassword(password) {
    const requirements = {
        length: PASSWORD_PATTERNS.length.test(password),
        lowercase: PASSWORD_PATTERNS.lowercase.test(password),
        uppercase: PASSWORD_PATTERNS.uppercase.test(password),
        number: PASSWORD_PATTERNS.number.test(password),
        special: PASSWORD_PATTERNS.special.test(password)
    };
    return requirements;
}

function updatePasswordRequirements() {
    const password = document.getElementById('registerPassword').value;
    const requirements = validatePassword(password);
    
    const reqs = [
        { id: 'req-length', met: requirements.length },
        { id: 'req-lowercase', met: requirements.lowercase },
        { id: 'req-uppercase', met: requirements.uppercase },
        { id: 'req-number', met: requirements.number },
        { id: 'req-special', met: requirements.special }
    ];
    
    reqs.forEach(req => {
        const element = document.getElementById(req.id);
        if (element) {
            if (req.met) {
                element.classList.add('met');
            } else {
                element.classList.remove('met');
            }
        }
    });
}

// Event Listeners
document.addEventListener('DOMContentLoaded', function() {
    // Login Form
    const loginForm = document.getElementById('loginFormElement');
    if (loginForm) {
        loginForm.addEventListener('submit', handleLogin);
    }

    // Register Form
    const registerForm = document.getElementById('registerFormElement');
    if (registerForm) {
        registerForm.addEventListener('submit', handleRegister);
    }

    // Password field for requirements
    const registerPassword = document.getElementById('registerPassword');
    if (registerPassword) {
        registerPassword.addEventListener('input', updatePasswordRequirements);
    }

    // Forgot Password Step 1
    const forgotPasswordStep1 = document.getElementById('forgotPasswordFormStep1');
    if (forgotPasswordStep1) {
        forgotPasswordStep1.addEventListener('submit', handleForgotPasswordStep1);
    }

    // Forgot Password Step 2
    const forgotPasswordStep2 = document.getElementById('forgotPasswordFormStep2');
    if (forgotPasswordStep2) {
        forgotPasswordStep2.addEventListener('submit', handleForgotPasswordStep2);
    }

    // OTP input - only allow digits
    const otpInput = document.getElementById('resetOTP');
    if (otpInput) {
        otpInput.addEventListener('input', function() {
            this.value = this.value.replace(/[^0-9]/g, '');
        });
    }
});

// Form Handlers
async function handleLogin(e) {
    e.preventDefault();
    hideMessage('loginMessage');
    
    const email = document.getElementById('loginEmail').value.trim();
    const password = document.getElementById('loginPassword').value;

    // Validation
    let hasError = false;
    if (!email) {
        showError('loginEmailError', 'Email is required');
        hasError = true;
    } else {
        hideError('loginEmailError');
    }

    if (!password) {
        showError('loginPasswordError', 'Password is required');
        hasError = true;
    } else {
        hideError('loginPasswordError');
    }

    if (hasError) return;

    // API call
    const result = await AuthAPI.login(email, password);
    
    if (result.success) {
        setToken(result.access_token);
        setUserInfo(result.user);
        showMessage('loginMessage', 'Login successful!', 'success');
        
        // Show dashboard
        setTimeout(() => {
            showDashboard(result.user);
        }, 1000);
    } else {
        showMessage('loginMessage', result.message, 'error');
    }
}

async function handleRegister(e) {
    e.preventDefault();
    hideMessage('registerMessage');
    
    const email = document.getElementById('registerEmail').value.trim();
    const password = document.getElementById('registerPassword').value;
    const passwordConfirm = document.getElementById('registerPasswordConfirm').value;

    // Validation
    let hasError = false;
    
    if (!email) {
        showError('registerEmailError', 'Email is required');
        hasError = true;
    } else {
        hideError('registerEmailError');
    }

    if (!password) {
        showError('registerPasswordError', 'Password is required');
        hasError = true;
    } else if (password !== passwordConfirm) {
        showError('registerConfirmError', 'Passwords do not match');
        hasError = true;
    } else {
        hideError('registerPasswordError');
        hideError('registerConfirmError');
    }

    if (hasError) return;

    // API call
    const result = await AuthAPI.register(email, password);
    
    if (result.success) {
        showMessage('registerMessage', 'Registration successful! Please login.', 'success');
        
        setTimeout(() => {
            switchForm('loginForm');
            clearForm('registerFormElement');
        }, 2000);
    } else {
        showMessage('registerMessage', result.message, 'error');
    }
}

async function handleForgotPasswordStep1(e) {
    e.preventDefault();
    hideMessage('forgotPasswordStep1Message');
    
    const email = document.getElementById('forgotEmail').value.trim();

    if (!email) {
        showError('forgotEmailError', 'Email is required');
        return;
    }
    hideError('forgotEmailError');

    // API call
    const result = await AuthAPI.requestPasswordReset(email);
    
    if (result.success) {
        localStorage.setItem(STORAGE_KEYS.FORGOT_EMAIL, email);
        showMessage('forgotPasswordStep1Message', result.message, 'success');
        
        // Show step 2 after 1 second
        setTimeout(() => {
            document.getElementById('forgotPasswordStep1').classList.remove('active');
            document.getElementById('forgotPasswordStep2').classList.add('active');
        }, 1500);
    } else {
        showMessage('forgotPasswordStep1Message', result.message, 'error');
    }
}

async function handleForgotPasswordStep2(e) {
    e.preventDefault();
    hideMessage('forgotPasswordStep2Message');
    
    const email = localStorage.getItem(STORAGE_KEYS.FORGOT_EMAIL);
    const otp = document.getElementById('resetOTP').value.trim();
    const newPassword = document.getElementById('resetPassword').value;
    const passwordConfirm = document.getElementById('resetPasswordConfirm').value;

    // Validation
    let hasError = false;

    if (!otp || otp.length !== 6) {
        showError('otpError', 'OTP must be 6 digits');
        hasError = true;
    } else {
        hideError('otpError');
    }

    if (!newPassword) {
        showError('resetPasswordError', 'New password is required');
        hasError = true;
    } else if (newPassword !== passwordConfirm) {
        showError('resetConfirmError', 'Passwords do not match');
        hasError = true;
    } else {
        hideError('resetPasswordError');
        hideError('resetConfirmError');
    }

    if (hasError) return;

    // API call
    const result = await AuthAPI.resetPassword(email, otp, newPassword);
    
    if (result.success) {
        showMessage('forgotPasswordStep2Message', result.message, 'success');
        
        setTimeout(() => {
            resetForgotForm();
            switchForm('loginForm');
        }, 2000);
    } else {
        showMessage('forgotPasswordStep2Message', result.message, 'error');
    }
}

function resetForgotForm() {
    document.getElementById('forgotPasswordStep1').classList.add('active');
    document.getElementById('forgotPasswordStep2').classList.remove('active');
    clearForm('forgotPasswordFormStep1');
    clearForm('forgotPasswordFormStep2');
    localStorage.removeItem(STORAGE_KEYS.FORGOT_EMAIL);
}

function showDashboard(user) {
    switchForm('dashboard');
    document.getElementById('dashboardEmail').textContent = user.email;
    if (user.created_at) {
        const date = new Date(user.created_at);
        document.getElementById('dashboardCreatedAt').textContent = date.toLocaleDateString();
    }
}

// Check if user is already logged in on page load
window.addEventListener('load', function() {
    const token = getToken();
    const user = getUserInfo();
    
    if (token && user) {
        showDashboard(user);
    }
});
