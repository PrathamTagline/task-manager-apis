import { emailInput, passwordInput, emailError, passwordError } from './signin_page_elements.js';
import { REGEX, ERROR_MESSAGES } from '../constants.js';

export function validateEmail() {
    const emailValue = emailInput.value.trim();

    if (emailValue === '') {
        emailError.textContent = ERROR_MESSAGES.emailRequired;
        emailInput.classList.add('error');
        return false;
    } else if (!REGEX.email.test(emailValue)) {
        emailError.textContent = ERROR_MESSAGES.invalidEmail;
        emailInput.classList.add('error');
        return false;
    } else {
        emailError.textContent = '';
        emailInput.classList.remove('error');
        return true;
    }
}

export function validatePassword() {
    const passwordValue = passwordInput.value.trim();

    if (passwordValue === '') {
        passwordError.textContent = ERROR_MESSAGES.passwordRequired;
        passwordInput.classList.add('error');
        return false;
    } else if (passwordValue.length < 6) {
        passwordError.textContent = ERROR_MESSAGES.passwordLength;
        passwordInput.classList.add('error');
        return false;
    } else {
        passwordError.textContent = '';
        passwordInput.classList.remove('error');
        return true;
    }
}