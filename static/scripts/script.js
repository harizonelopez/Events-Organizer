// Elements
const container = document.getElementById("container");
const registerBtn = document.getElementById("register");
const loginBtn = document.getElementById("login");

// Toggle between sign-up and sign-in forms
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
/*
function toggleEdit(taskId) {
    document.getElementById(`task-name-${taskId}`).style.display = 'none';
    document.getElementById(`edit-task-${taskId}`).style.display = 'inline-block';
    document.querySelector(`#task-${taskId} .edit-btn`).style.display = 'none';
    document.querySelector(`#task-${taskId} .save-btn`).style.display = 'inline-block';
}

function saveTask(taskId) {
    let newName = document.getElementById(`edit-task-${taskId}`).value;
*/

// Auto-hide flash messages function script
setTimeout(() => {
    const flashMessages = document.getElementById("flash-messages");
    if (flashMessages) {
        flashMessages.style.transition = "opacity 0.5s ease-out";
        flashMessages.style.opacity = 0; // Fade out
        setTimeout(() => flashMessages.remove(), 500); // Remove after fade-out
    }
}, 3000); // 3 seconds timer for the flash messages to fade out
