document.addEventListener('DOMContentLoaded', function () {
    const usernameField = document.getElementById('id_username');
    const passwordField = document.getElementById('id_password1');
    const passwordConfirmField = document.getElementById('id_password2');
    const usernameError = document.createElement('div');
    const passwordError = document.createElement('div');
    const passwordConfirmError = document.createElement('div');

    usernameError.classList.add('text-red-500', 'text-sm');
    passwordError.classList.add('text-red-500', 'text-sm');
    passwordConfirmError.classList.add('text-red-500', 'text-sm');

    usernameField.parentNode.appendChild(usernameError);
    passwordField.parentNode.appendChild(passwordError);
    passwordConfirmField.parentNode.appendChild(passwordConfirmError);

    usernameField.addEventListener('input', function () {
        const username = usernameField.value;
        if (username.length < 5) {
            usernameError.textContent = 'Username must be at least 5 characters long.';
        } else if (!/^[\w.@+-]+$/.test(username)) {
            usernameError.textContent = 'Username can only contain letters, digits and @/./+/-/_ characters.';
        } else {
            usernameError.textContent = '';
        }
    });

    passwordField.addEventListener('input', function () {
        const password = passwordField.value;
        if (password.length < 8) {
            passwordError.textContent = 'Password must be at least 8 characters long.';
        } else if (!/(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}/.test(password)) {
            passwordError.textContent = 'Password must contain at least one uppercase letter, one lowercase letter, and one digit.';
        } else {
            passwordError.textContent = '';
        }
    });

    passwordConfirmField.addEventListener('input', function () {
        const password = passwordField.value;
        const confirmPassword = passwordConfirmField.value;
        if (password !== confirmPassword) {
            passwordConfirmError.textContent = 'Passwords do not match.';
        } else {
            passwordConfirmError.textContent = '';
        }
    });
});
