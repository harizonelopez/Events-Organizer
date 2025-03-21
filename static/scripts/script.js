// Elements handles
const container = document.getElementById("container");
const registerBtn = document.getElementById("register");
const loginBtn = document.getElementById("login");

// Toggle between sign-up and sign-in forms [cros-over]
if (registerBtn) {
    registerBtn.addEventListener("click", () => {
        container.classList.add("active");
    });
}

if (loginBtn) {
    loginBtn.addEventListener("click", () => {
        container.classList.remove("active");
    });
}

// Handle sign-up button click (trigger form submission)
const signUpBtn = document.getElementById("Up");
if (signUpBtn) {
    signUpBtn.addEventListener("click", () => {
        const form = document.getElementById("sign-up-form");
        form.submit();  // Submit form normally
    });
}