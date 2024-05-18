document.addEventListener('DOMContentLoaded', function() {
    const ageInput = document.querySelector('input[name="NewAge"]');
    const emailInput = document.querySelector('input[name="NewEmail"]');
    const ageErrorMessage = document.querySelector('.error-message-age');
    const emailErrorMessage = document.querySelector('.error-message-email');

    ageInput.addEventListener('input', function() {
        const age = parseInt(ageInput.value);
        if (age < 18) {
            ageInput.classList.add('error');
            ageErrorMessage.classList.add('error');
            ageErrorMessage.textContent = 'Age must be 18 or older';
        } else {
            ageInput.classList.remove('error');
            ageErrorMessage.classList.remove('error');
            ageErrorMessage.textContent = '';
        }
    });

    emailInput.addEventListener('input', function() {
        const email = emailInput.value.trim();
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(email)) {
            emailInput.classList.add('error');
            emailErrorMessage.classList.add('error');
            emailErrorMessage.textContent = 'Please enter a valid email address';
        } else {
            emailInput.classList.remove('error');
            emailErrorMessage.classList.remove('error');
            emailErrorMessage.textContent = '';
        }
    });
});
