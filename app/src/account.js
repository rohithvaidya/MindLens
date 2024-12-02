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

logout_user.addEventListener("click", (e)=>{
    sessionStorage.clear()

    window.location.href = "index.html"
})