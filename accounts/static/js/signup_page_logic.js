import {
    validateFirstName,
    validateLastName,
    validateEmail,
    validateUsername,
    validatePassword,
    validateConfirmPassword,
    validateTerms,
} from './signup_page_scripts/signup_page_validation.js';

import {
    form,
    firstNameInput,
    lastNameInput,
    usernameInput,
    emailInput,
    passwordInput,
    confirmPasswordInput,
    agreeCheckbox,
    firstNameError,
    lastNameError,
    emailError,
    usernameError,
    passwordError,
    confirmPasswordError,
    termsError,
} from './signup_page_scripts/signup_page_elements.js';

document.addEventListener('DOMContentLoaded', function () {

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

    // Real-time validation
    firstNameInput.addEventListener('input', () => validateFirstName(firstNameInput, firstNameError));
    lastNameInput.addEventListener('input', () => validateLastName(lastNameInput, lastNameError));
    emailInput.addEventListener('input', () => validateEmail(emailInput, emailError));
    usernameInput.addEventListener('input', () => validateUsername(usernameInput, usernameError));
    passwordInput.addEventListener('input', () => validatePassword(passwordInput, passwordError));
    confirmPasswordInput.addEventListener('input', () =>
        validateConfirmPassword(passwordInput, confirmPasswordInput, confirmPasswordError)
    );
    agreeCheckbox.addEventListener('change', () => validateTerms(agreeCheckbox, termsError));

    // Password input also affects confirm password validation
    passwordInput.addEventListener('input', function () {
        if (confirmPasswordInput.value !== '') {
            validateConfirmPassword(passwordInput, confirmPasswordInput, confirmPasswordError);
        }
    });

    // Form submission
    form.addEventListener('submit', async function (e) {
        e.preventDefault();

        // Validate all fields
        const isFirstNameValid = validateFirstName(firstNameInput, firstNameError);
        const isLastNameValid = validateLastName(lastNameInput, lastNameError);
        const isEmailValid = validateEmail(emailInput, emailError);
        const isUsernameValid = validateUsername(usernameInput, usernameError);
        const isPasswordValid = validatePassword(passwordInput, passwordError);
        const isConfirmPasswordValid = validateConfirmPassword(passwordInput, confirmPasswordInput, confirmPasswordError);
        const isTermsAgreed = validateTerms(agreeCheckbox, termsError);

        if (
            isFirstNameValid &&
            isLastNameValid &&
            isEmailValid &&
            isUsernameValid &&
            isPasswordValid &&
            isConfirmPasswordValid &&
            isTermsAgreed
        ) {
            const firstname = firstNameInput.value;
            const lastname = lastNameInput.value;
            const username = usernameInput.value;
            const email = emailInput.value;
            const password = passwordInput.value;
            const password2 = confirmPasswordInput.value;

            try {
                // 1. Register user
                const registerRes = await fetch('http://127.0.0.1:8000/accounts/api/signup/', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ username, first_name: firstname, last_name: lastname, email, password, password2 }),
                });

                const registerData = await registerRes.json();

                if (registerRes.ok) {
                    // 2. Auto-login after successful signup
                    const loginRes = await fetch('http://127.0.0.1:8000/accounts/api/signin/', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ email, password }),
                    });

                    const loginData = await loginRes.json();

                    if (loginRes.ok) {
                        // 3. Store tokens and user info
                        localStorage.setItem('access_token', loginData.access);
                        localStorage.setItem('refresh_token', loginData.refresh);
                        localStorage.setItem('user', JSON.stringify(registerData.user));

                        // 4. Redirect to dashboard
                        window.location.href = '/dashboard/';
                    } else {
                        message.innerText = loginData.detail || 'Auto login failed. Please log in manually.';
                    }
                } else {
                    const errMsg = Object.values(registerData).join(', ') || 'Registration failed';
                    message.innerText = errMsg;
                }
            } catch (error) {
            }
        }
    });
});