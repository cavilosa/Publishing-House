document.addEventListener('DOMContentLoaded', function () {
    console.log("LOADED")
    let button = document.querySelector(".test")
    button.addEventListener("click", changeColor)
});

let sign_in = document.querySelector(".sign_in")
sign_in.addEventListener("click", signIn)

async function changeColor(e){
    button = document.querySelector(".test")
    if(button.style.color!="red"){
        button.style.color="red";  
    }else{
        button.style.color="black";
    }
}

async function signIn(e){
    e.preventDefault();
    console.log("SIGH IN")
        window.location.href = "https://korzhyk-app.us.auth0.com/authorize?audience=app&response_type=token&client_id=a0mzLPX0PZ6KPWVGo058FFCUUNwShqIN&redirect_uri=http://localhost:8080/login-results"; 
}