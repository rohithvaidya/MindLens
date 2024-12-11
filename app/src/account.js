let username = sessionStorage.getItem('username')
let id = sessionStorage.getItem('id')

function isnull(key){
    if (key === null || 
        key == null || 
        key === undefined || 
        key == undefined || 
        key === 'undefined' ||
        key == 'undefined'){
            return true
        }
    else return false
}

if (isnull(username) || isnull(id)) {
    sessionStorage.clear()
    window.location.href = 'login.html'
}
const user_span = document.getElementById("username")
user_span.textContent = username

const logout_user = document.getElementById("logout")
const rtfButton = document.getElementById("rtf");

logout_user.addEventListener("click", (e)=>{
    sessionStorage.clear()

    window.location.href = "index.html"
})

rtfButton.addEventListener("click", async (e) => {
    let id = sessionStorage.getItem('id')
    
    alert("We have received your request to delete your personal information. Please note that the changes will be reflected after some time.");

    if (id) {
        try {
            // Send POST request to the server with the id as the payload
            const response = await fetch("http://127.0.0.1:5000/right_to_erase", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",  // Send JSON data
                },
                body: JSON.stringify({ id: id })  // Include the id in the body
            });

            // Check if the response is successful (status 200-299)
            if (response.ok) {
                const data = await response.json();  // Parse the JSON response
                console.log("Response from server:", data);  // Log the response data
            } else {
                console.error("Error response from server:", response.statusText);
                alert("Error: Could not process the request.");
            }
        } catch (error) {
            console.error("Error during the POST request:", error);
            alert("An unexpected error occurred. Please try again later.");
        }
    } else {
        alert("ID is missing in session storage. Please log in again.");
    }
});



