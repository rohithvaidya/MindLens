const warningMsg = document.getElementById('warning-msg')
document.getElementById("login-form").addEventListener("submit", async function (event) {
    event.preventDefault(); // Prevent the default form submission

    // Get the user-entered ID from the form
    const userId = parseInt(document.getElementById("id").value);
    const userName = document.getElementById("name").value;

    // Send the ID to the server via a POST request
    try {
        const response = await fetch("http://127.0.0.1:5000/login", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ id: userId, name:userName }),
        });

        // Handle the response from the server
        if (response.ok) {
            const data = await response.json();
            // Redirect or take an action based on server response
            if (data.success) {
                // Set session variables
                sessionStorage.setItem('username', data.name)
                sessionStorage.setItem('id', data.id)
                
                window.location.href = "account.html"; // Replace with your target page
            } else {
                warningMsg.classList.remove('hidden')
                setTimeout(() => {
                    warningMsg.classList.add('hidden')
                }, 3000);
            }
        } else {
            alert("Server error. Please try again later.");
        }
    } catch (error) {
        console.error("Error during login request:", error);
        alert("An unexpected error occurred. Please try again later.");
    }
});