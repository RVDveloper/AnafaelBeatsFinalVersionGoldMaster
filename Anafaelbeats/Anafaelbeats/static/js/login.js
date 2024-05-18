document.addEventListener('DOMContentLoaded', function() {
    const ageInput = document.querySelector('input[name="age"]');
    const emailInput = document.querySelector('input[name="email"]');
    const genderInput = document.querySelector('input[name="gender"]');
    const ageErrorMessage = document.querySelector('.error-message-age');
    const emailErrorMessage = document.querySelector('.error-message-email');
    const genderErrorMessage = document.querySelector('.error-message-gender');
  
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

    genderInput.addEventListener('input', function() {
      const gender = genderInput.value.trim().toLowerCase();
      if (gender !== 'male' && gender !== 'female') {
        genderInput.classList.add('error');
        genderErrorMessage.classList.add('error');
        genderErrorMessage.textContent = 'Please enter either "Male" or "Female"';
      } else {
        genderInput.classList.remove('error');
        genderErrorMessage.classList.remove('error');
        genderErrorMessage.textContent = '';
      }
    });
});

