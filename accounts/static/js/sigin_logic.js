import { validateEmail, validatePassword } from './signin_page_scripts/signin_page_validation.js';
import { emailInput, passwordInput, form, message } from './signin_page_scripts/signin_page_elements.js';

document.addEventListener('DOMContentLoaded', function () {
    // Real-time validation
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
                const response = await fetch('/accounts/api/token/', {
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