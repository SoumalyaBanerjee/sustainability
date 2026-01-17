// API Configuration
const API_BASE_URL = 'http://localhost:5000/api';

class AuthAPI {
    static async register(email, password) {
        try {
            const response = await fetch(`${API_BASE_URL}/auth/register`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ email, password })
            });
            return await response.json();
        } catch (error) {
            console.error('Register error:', error);
            return { success: false, message: 'Network error' };
        }
    }

    static async login(email, password) {
        try {
            const response = await fetch(`${API_BASE_URL}/auth/login`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ email, password })
            });
            return await response.json();
        } catch (error) {
            console.error('Login error:', error);
            return { success: false, message: 'Network error' };
        }
    }

    static async requestPasswordReset(email) {
        try {
            const response = await fetch(`${API_BASE_URL}/auth/request-password-reset`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ email })
            });
            return await response.json();
        } catch (error) {
            console.error('Password reset request error:', error);
            return { success: false, message: 'Network error' };
        }
    }

    static async resetPassword(email, otp, newPassword) {
        try {
            const response = await fetch(`${API_BASE_URL}/auth/reset-password`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ 
                    email, 
                    otp, 
                    new_password: newPassword 
                })
            });
            return await response.json();
        } catch (error) {
            console.error('Password reset error:', error);
            return { success: false, message: 'Network error' };
        }
    }

    static async getCurrentUser(token) {
        try {
            const response = await fetch(`${API_BASE_URL}/auth/me`, {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json',
                }
            });
            return await response.json();
        } catch (error) {
            console.error('Get current user error:', error);
            return { success: false, message: 'Network error' };
        }
    }
}
