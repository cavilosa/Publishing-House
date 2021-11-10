document.addEventListener('DOMContentLoaded', function () {
    console.log("DOM loaded")
});

// Storing current html into variables

let editorHtml = document.querySelector(".editor").innerHTML
let coordinatorHtml = document.querySelector(".coordinator").innerHTML
let readerHtml = document.querySelector(".reader").innerHTML

// Adding eventListeners to elements

document.querySelector(".reader").addEventListener("mouseover", reader)
document.querySelector(".reader").addEventListener("mouseleave", readerLeave)

document.querySelector(".coordinator").addEventListener("mouseover", coordinator)
document.querySelector(".coordinator").addEventListener("mouseleave", coordinatorLeave)

document.querySelector(".editor").addEventListener("mouseover", editor)
document.querySelector(".editor").addEventListener("mouseleave", editorLeave)


// Functions to change elements' inner html with additional info on mouse hover.
// On mouse leave event html will get initial value.

async function reader(event) {
    event.preventDefault();
    console.log('mouse over triggered');
    let reader = document.querySelector(".reader")
    reader.innerHTML = "A <b>Reader</b> can access a list of books and authors. Permissions - get:authors, get:books."
}
async function readerLeave(event){
    event.preventDefault();
    console.log("mouse leave triggered")
    let reader = document.querySelector(".reader")
    reader.innerHTML = readerHtml
}

async function coordinator(event) {
    event.preventDefault();
    console.log('mouse over triggered');
    let coordinator = document.querySelector(".coordinator")
    coordinator.innerHTML = "A <b>Coordinator</b> can see the details of books and authors, including a permission to modify and create new entries. Permissions - reader + patch:author, patch:book, post:author, post:book."
}
async function coordinatorLeave(event){
    event.preventDefault();
    console.log("mouse leave triggered")
    let coordinator = document.querySelector(".coordinator")
    coordinator.innerHTML = coordinatorHtml
}

async function editor(event) {
    event.preventDefault();
    console.log('mouse over triggered');
    let editor = document.querySelector(".editor")
    editor.innerHTML = "An <b>Editor</b> has the major access to all the data with the coordinator access plus permissions to delete books and authors. Permissions - coordinator + delete:author, delete:book."
}
async function editorLeave(event){
    event.preventDefault();
    console.log("mouse leave triggered")
    let editor = document.querySelector(".editor")
    editor.innerHTML = editorHtml
}