let username = sessionStorage.getItem('username')
let userid = sessionStorage.getItem('id')
const username_span = document.getElementById("username")
const loader_div = document.getElementById("loader")
const loading_msg_div = document.getElementById("loading-msg")

const socket = io('http://localhost:5000');

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

if (isnull(username) || isnull(userid)) {
    sessionStorage.clear()
    window.location.href = 'login.html'
}

if (!isnull(username)){
    username_span.textContent = username;
}

socket.on('data_processing_start', (data) => {
    if(data.success){
        loader_div.classList.add("loader-1");
        loader_div.classList.remove("hidden");
        loading_msg_div.textContent = "Pre-Processing your data."
    } else {
        console.log("Some Error occurred before data pre-processing")
    }
});

socket.on('inference_start', (data) => {
    if(data.success){
        loader_div.classList.remove("loader-1");
        loader_div.classList.add("loader-2");
        loading_msg_div.textContent = "Inferencing on your data."
    } else {
        console.log("Some Error occured during Data Processing Pipeline")
    }
    
});

socket.on('interpretation_start', (data) => {
    if(data.success){
        loader_div.classList.remove("loader-2");
        loader_div.classList.add("loader-3");
        loading_msg_div.textContent = "Interpreting your results."
    } else {
        console.log("Some Error occured during Inference Pipeline")
    }
});

socket.on('all_done', (data) => {
    if(data.success){
        loader_div.classList.remove("loader-3");
        loader_div.classList.add("hidden");
        loading_msg_div.textContent = "All done."
    } else {
        console.log("Some Error occured during Explanation Pipeline")
    }
});

async function run_pipeline() {
    try {
        const response = await fetch("http://127.0.0.1:5000/run_pipeline", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ userid: userid, username:username }),
        });
    
        // Handle the response from the server
        if (response.ok) {
            const data = await response.json();
            // Redirect or take an action based on server response
            if (data.success) {
                console.log(data)                    
                // window.location.href = "results.html"; // Replace with your target page
            } else {
                alert(`${data.message}`);
            }
        } else {
            alert("Server error. Please try again later.");
        }
    } catch (error) {
        console.error("Error during login request:", error);
        alert("An unexpected error occurred. Please try again later.");
    }
}