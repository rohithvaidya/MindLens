const takeSurveyButton = document.getElementById("take-survey")

// Event listener for the "Take the Survey" button
takeSurveyButton.addEventListener("click", () => {
    // Check if the necessary cookies are present
    const username = sessionStorage.getItem('username')
    const id = sessionStorage.getItem('id')

    if (username && id) {
        // Redirect to page1 if cookies are available
        window.location.href = "account.html";
    } else {
        // Redirect to page2 if cookies are not available
        window.location.href = "login.html";
    }
});