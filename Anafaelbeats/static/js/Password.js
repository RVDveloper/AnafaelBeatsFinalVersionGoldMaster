function validatePassword() {
    var password = document.getElementById("password").value;
    var repeatPassword = document.getElementById("passwordRepeat").value;
    var errorMessage = document.getElementById("error-message");
    
    if (password !== repeatPassword) {
        errorMessage.innerHTML = "Passwords do not match";
        errorMessage.style.color = "red";
        return false;
    } else {
        errorMessage.innerHTML = "";
        return true;
    }
}