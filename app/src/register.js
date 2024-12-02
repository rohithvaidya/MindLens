document.getElementById("registration-form").addEventListener("submit", async function (event) {
    event.preventDefault(); // Prevent the default form submission

    // Get the user-entered ID from the form
    const userName = document.getElementById("name").value;

    // Send the ID to the server via a POST request
    try {
        const response = await fetch("http://127.0.0.1:5000/register", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ name : userName }),
        });

        // Handle the response from the server
        if (response.ok) {
            const data = await response.json();
            // Redirect or take an action based on server response
            console.log(data)
            if (data.success) {
                // Set session variables
                sessionStorage.setItem('username', data.name)
                sessionStorage.setItem('id', data.id)

                window.location.href = "account.html"; // Replace with your target page
            } else {
                alert(data.message || "Registration failed. Please try again.");
            }
        } else {
            alert("Server error. Please try again later.");
        }
    } catch (error) {
        console.error("Error during login request:", error);
        alert("An unexpected error occurred. Please try again later.");
    }
});