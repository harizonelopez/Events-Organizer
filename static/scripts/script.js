// API Base URL for Flask
const apiUrl = "http://127.0.0.1:5000/"; 

// Elements
const container = document.getElementById("container");
const registerBtn = document.getElementById("register");
const loginBtn = document.getElementById("login");

// Toggle between sign-up and sign-in
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


// Handle sign-in functionality
const loginForm = document.querySelector(".sign-in form");
if (loginForm) {
    loginForm.addEventListener("submit", (event) => {
        event.preventDefault();

        const username = document.getElementById("username").value.trim();
        const password = document.getElementById("password").value.trim();

        if (!username || !password) {
            alert("Please enter both username and password.");
            return;
        }

        console.log("Logging in with:", { username, password });

        fetch("http://127.0.0.1:5000/login", {  // ✅ Explicit full URL
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ username, password }),
        })        
        .then((response) => response.json())  // ✅ Ensure JSON response
        .then((data) => {
            if (data.token) {
                localStorage.setItem("token", data.token);
                alert("Login successful!");
                window.location.href = "/register";  // ✅ Change this to your dashboard route
            } else {
                throw new Error(data.error || "Invalid login");
            }
        })
        .catch((error) => {
            console.error("Login failed:", error);
            alert(error.message || "Invalid username or password. Try again.");
        });
    });
};



// Handle sign-up functionality
const signUpUser = () => {
    const username = document.getElementById("sign-up-user").value.trim();
    const password = document.getElementById("sign-up-pass").value.trim();
    const confirmPassword = document.getElementById("sign-up-ConPass").value.trim();

    if (!username || !password || !confirmPassword) {
        alert("Please fill out all fields.");
        return;
    }

    if (password !== confirmPassword) {
        alert("Passwords do not match!");
        return;
    }

    console.log("Registering user:", { username, password });

    fetch("http://127.0.0.1:5000/register", {  // ✅ Explicit full URL
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password }),
    })    
    .then((response) => response.json())
    .then((data) => {
        alert(data.message || "User registered successfully!");
        container.classList.remove("active"); // ✅ Switch to login form
    })
    .catch((error) => {
        console.error("Registration failed:", error);
        alert(error.message || "An error occurred while creating the user.");
    });
};


const signUpBtn = document.getElementById("Up");
if (signUpBtn) {
    signUpBtn.addEventListener("click", signUpUser);
}

setTimeout(() => {
    const flashMessages = document.getElementById('flash-messages');
    if (flashMessages) {
        flashMessages.style.transition = "opacity 0.5s ease-out";
        flashMessages.style.opacity = 0; // Fade out
        setTimeout(() => flashMessages.remove(), 500); // Remove after fade-out
    }
}, 5000); // 5 seconds timer for the flash messages to fade out


// Debugging 
console.log("Sending login data:", { username, password });
console.log("API URL:", apiUrl);
