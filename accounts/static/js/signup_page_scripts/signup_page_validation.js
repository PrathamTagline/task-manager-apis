import { ERROR_MESSAGES, REGEX } from '../constants.js';

export function validateFirstName(input, errorEl) {
    const value = input.value.trim();
    if (value === '') {
        errorEl.textContent = ERROR_MESSAGES.firstNameRequired;
        input.classList.add('error');
        return false;
    } else if (value.length < 2) {
        errorEl.textContent = ERROR_MESSAGES.firstNameLength;
        input.classList.add('error');
        return false;
    } else {
        errorEl.textContent = '';
        input.classList.remove('error');
        return true;
    }
}

export function validateLastName(input, errorEl) {
    const value = input.value.trim();
    if (value === '') {
        errorEl.textContent = ERROR_MESSAGES.lastNameRequired;
        input.classList.add('error');
        return false;
    } else if (value.length < 2) {
        errorEl.textContent = ERROR_MESSAGES.lastNameLength;
        input.classList.add('error');
        return false;
    } else {
        errorEl.textContent = '';
        input.classList.remove('error');
        return true;
    }
}

export function validateEmail(input, errorEl) {
    const value = input.value.trim();
    if (value === '') {
        errorEl.textContent = ERROR_MESSAGES.emailRequired;
        input.classList.add('error');
        return false;
    } else if (!REGEX.email.test(value)) {
        errorEl.textContent = ERROR_MESSAGES.invalidEmail;
        input.classList.add('error');
        return false;
    } else {
        errorEl.textContent = '';
        input.classList.remove('error');
        return true;
    }
}

export function validateUsername(input, errorEl) {
    const value = input.value.trim();
    if (value === '') {
        errorEl.textContent = ERROR_MESSAGES.usernameRequired;
        input.classList.add('error');
        return false;
    } else if (!REGEX.username.test(value)) {
        errorEl.textContent = ERROR_MESSAGES.usernameLength;
        input.classList.add('error');
        return false;
    } else {
        errorEl.textContent = '';
        input.classList.remove('error');
        return true;
    }
}

export function validatePassword(input, errorEl) {
    const value = input.value;
    const hasNumber = /\d/.test(value);
    const hasSpecial = /[!@#$%^&*(),.?":{}|<>]/.test(value);

    if (value === '') {
        errorEl.textContent = ERROR_MESSAGES.passwordRequired;
        input.classList.add('error');
        return false;
    } else if (value.length < 8) {
        errorEl.textContent = ERROR_MESSAGES.passwordLength;
        input.classList.add('error');
        return false;
    } else if (!hasNumber) {
        errorEl.textContent = ERROR_MESSAGES.passwordNumber;
        input.classList.add('error');
        return false;
    } else if (!hasSpecial) {
        errorEl.textContent = ERROR_MESSAGES.passwordSpecial;
        input.classList.add('error');
        return false;
    } else {
        errorEl.textContent = '';
        input.classList.remove('error');
        return true;
    }
}

export function validateConfirmPassword(passwordInput, confirmInput, errorEl) {
    if (confirmInput.value === '') {
        errorEl.textContent = ERROR_MESSAGES.confirmPasswordRequired;
        confirmInput.classList.add('error');
        return false;
    } else if (confirmInput.value !== passwordInput.value) {
        errorEl.textContent = ERROR_MESSAGES.passwordsDontMatch;
        confirmInput.classList.add('error');
        return false;
    } else {
        errorEl.textContent = '';
        confirmInput.classList.remove('error');
        return true;
    }
}

export function validateTerms(checkbox, errorEl) {
    if (!checkbox.checked) {
        errorEl.textContent = ERROR_MESSAGES.termsRequired;
        return false;
    } else {
        errorEl.textContent = '';
        return true;
    }
}