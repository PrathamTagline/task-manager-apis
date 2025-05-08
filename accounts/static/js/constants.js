
export const ERROR_MESSAGES = {
    firstNameRequired: 'First name is required',
    firstNameLength: 'First name must be at least 2 characters',
    lastNameRequired: 'Last name is required',
    lastNameLength: 'Last name must be at least 2 characters',
    emailRequired: 'Email is required',
    invalidEmail: 'Please enter a valid email address',
    usernameRequired: 'Username is required',
    usernameLength: 'Username must be at least 3 characters and can only contain letters, numbers, and underscores',
    passwordRequired: 'Password is required',
    passwordLength: 'Password must be at least 8 characters',
    passwordNumber: 'Password must include at least one number',
    passwordSpecial: 'Password must include at least one special character',
    confirmPasswordRequired: 'Please confirm your password',
    passwordsDontMatch: 'Passwords do not match',
    termsRequired: 'You must agree to the Terms of Service and Privacy Policy',
};

export const REGEX = {
    email: /^[^\s@]+@[^\s@]+\.[^\s@]+$/,
    username: /^[a-zA-Z0-9_]{3,}$/,
    hasNumber: /\d/,
    hasSpecialChar: /[!@#$%^&*(),.?":{}|<>]/,
};



export const ERROR_CLASS = 'error';

export const content = "This is the content variable for validation.";
