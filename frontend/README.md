<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Frontend Documentation</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            max-width: 1000px;
            margin: 0 auto;
            padding: 20px;
            background: #f4f4f4;
        }
        h1, h2, h3 { color: #333; }
        code { background: #f0f0f0; padding: 2px 5px; border-radius: 3px; }
        pre { background: #f0f0f0; padding: 10px; border-radius: 5px; overflow-x: auto; }
        .endpoint { background: #e3f2fd; padding: 10px; margin: 10px 0; border-left: 4px solid #2196F3; }
    </style>
</head>
<body>
    <h1>Frontend Documentation</h1>
    
    <h2>Overview</h2>
    <p>The frontend is a standalone HTML/CSS/JavaScript application that communicates with the backend API.</p>
    
    <h2>File Structure</h2>
    <ul>
        <li><code>index.html</code> - Main HTML structure</li>
        <li><code>styles.css</code> - All styling</li>
        <li><code>api.js</code> - API communication layer</li>
        <li><code>app.js</code> - Application logic and event handling</li>
    </ul>
    
    <h2>Features</h2>
    <ul>
        <li>User Login</li>
        <li>User Registration with password strength validation</li>
        <li>Password Reset via OTP</li>
        <li>JWT token management</li>
        <li>Local storage for user session</li>
    </ul>
    
    <h2>How to Use</h2>
    <ol>
        <li>Open <code>index.html</code> in a web browser</li>
        <li>The default form shown is the login form</li>
        <li>Click "Register here" to switch to registration</li>
        <li>Click "Forgot your password?" to access password reset</li>
    </ol>
    
    <h2>Configuration</h2>
    <p>Update <code>API_BASE_URL</code> in <code>api.js</code> to point to your backend server:</p>
    <pre>const API_BASE_URL = 'http://localhost:5000/api';</pre>
    
    <h2>Local Storage</h2>
    <p>The app stores the following in browser local storage:</p>
    <ul>
        <li><code>auth_token</code> - JWT token</li>
        <li><code>user_info</code> - User object</li>
        <li><code>forgot_email</code> - Temporary storage during password reset</li>
    </ul>
</body>
</html>
