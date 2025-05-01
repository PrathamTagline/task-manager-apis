import { validateEmail, validatePassword } from './signin_page_scripts/signin_page_validation.js';
import { emailInput, passwordInput, form, message } from './signin_page_scripts/signin_page_elements.js';

document.addEventListener('DOMContentLoaded', function () {
    // Real-time validation
    const accessToken = localStorage.getItem('access_token');

    if (accessToken) {
        fetch('/accounts/api/token/verify/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + accessToken
            },
            body: JSON.stringify({ token: accessToken })
        })
            .then(res => {
                if (res.ok) {
                    // Redirect to dashboard if token is valid
                    window.location.href = "/dashboard/";
                } else {
                    console.error("Token verification failed:", res.status);
                    // Stay on the home page if token is invalid
                }
            })
            .catch(err => {
                console.error("Error verifying token:", err);
                // Stay on the home page on error
            });
    } else {
        // Stay on the home page if no token is found
    }

    emailInput.addEventListener('input', validateEmail);
    passwordInput.addEventListener('input', validatePassword);

    // Form submission
    form.addEventListener('submit', async function (e) {
        e.preventDefault();

        const isEmailValid = validateEmail();
        const isPasswordValid = validatePassword();

        if (isEmailValid && isPasswordValid) {
            const email = emailInput.value;
            const password = passwordInput.value;

            try {
                const response = await fetch('http://127.0.0.1:8000/accounts/api/signin/', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ email, password }),
                });

                const data = await response.json();

                if (response.ok) {
                    localStorage.setItem('access_token', data.access);
                    localStorage.setItem('refresh_token', data.refresh);
                    window.location.href = '/dashboard/';
                } else {
                    message.innerText = data.detail || 'Login failed';
                }
            } catch (error) {
                console.error('Error:', error);
                message.innerText = 'An error occurred. Please try again.';
            }
        }
    });
});