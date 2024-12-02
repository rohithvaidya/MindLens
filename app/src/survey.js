let username = sessionStorage.getItem('username')
let userid = sessionStorage.getItem('id')
const username_span = document.getElementById("username")

const ID_TO_COLUMN_MAP = {
    'CGPA': 'CGPA',
    'academic_pressure': 'Academic Pressure',
    'age': 'Age',
    'city': 'City',
    'degree': 'Degree',
    'diet': 'Dietary Habits',
    'family': 'Family History of Mental Illness',
    'financial_stress': 'Financial Stress',
    'gender': 'Gender',
    'job_satisfaction': 'Job Satisfaction',
    'profession': 'Profession',
    'sleep_duration': 'Sleep Duration',
    'study_satisfaction': 'Study Satisfaction',
    'suicidal': 'Have you ever had suicidal thoughts ?',
    'wps': 'Working Professional or Student',
    'wsh': 'Work/Study Hours',
    'work_pressure': 'Work Pressure'
}

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

document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("multi-page-form");
    const pages = document.querySelectorAll(".multi-page-form");
    let currentPage = 0;

    // Show the current page
    const showPage = (index) => {
        pages.forEach((page, i) => {
            page.classList.toggle("active", i === index);
        });
        currentPage = index;
    };

    // Validate fields in the current page
    const validatePage = () => {
        const currentInputs = pages[currentPage].querySelectorAll("input[required]");
        const dropdowns = pages[currentPage].querySelectorAll("select[required]");
        for (let dd of dropdowns) {
            console.log(dd)
            if (!dd.value.trim()) {
                alert(`Please fill out the required field: ${ID_TO_COLUMN_MAP[dd.name] || ID_TO_COLUMN_MAP[dd.id]}`);
                return false;
            }
        }
        for (let input of currentInputs) {
            if (!input.value.trim()) {
                alert(`Please fill out the required field: ${ID_TO_COLUMN_MAP[input.name] || ID_TO_COLUMN_MAP[input.id]}`);
                return false;
            }
        }
        return true;
    };

    // Navigation buttons
    for(let i=0; i < 8; i++){
        id = "next-" + i
        document.getElementById(id).addEventListener("click", () => {
            if (validatePage()) showPage(i+1)
        });
    }
    for(let i=1; i < 9; i++){
        id = "prev-" + i
        console.log(id)
        document.getElementById(id).addEventListener("click", () => showPage(i-1));
    }
    // Handle form submission
    form.addEventListener("submit", async (event) => {
        event.preventDefault(); // Prevent actual form submission
        if(!validatePage()) return false;

        // Collect all form data
        const formData = new FormData(form);
        const formObject = {};
        formData.forEach((value, key) => {
            formObject[ID_TO_COLUMN_MAP[key]] = value;
        });
        formObject['id'] = userid;
        formObject['Name'] = username;

        // Log the collected data or send it to the server
        console.log("Form submitted with data:", formObject);

        // Optionally redirect or display a success message
        // alert("Form submitted successfully!");

        try {
            const response = await fetch("http://127.0.0.1:5000/submit-survey", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(formObject),
            });
    
            // Handle the response from the server
            if (response.ok) {
                const data = await response.json();
                // Redirect or take an action based on server response
                if (data.success) {                    
                    // window.location.href = "account.html"; // Replace with your target page
                    console.log(data)
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
    });
});