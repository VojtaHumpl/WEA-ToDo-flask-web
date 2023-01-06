// constants
const TASK_CARD_HTML = "<div class=\"card\"> \
<h2 class=\"card_content\" contenteditable=\"true\"></h2> \
<p class=\"card_done\"> \
    <button class=\"card_done_button\">Done</button> \
</p> \
<p class=\"card_remove\"> \
    <button class=\"card_remove_button\">Remove</button> \
</p> \
</div>"

const TASK_COLOR = "radial-gradient(#1fe4f5, #3fbafe)"
const DONE_COLOR = "radial-gradient(#f588d8, #c0a3e5)"

const DEFAULT_CONTENT = "New Task"
const DEFAULT_STATUS = "todo"

/**
 * entry point adding listeners to menu buttons
 * and initializing tasks
 */
document.addEventListener('DOMContentLoaded', (event) => {
    let addBtn = document.getElementsByClassName("add_button")[0]
    addBtn.addEventListener("click", addBtnCallback)

    let filterDoneBtn = document.getElementById("btnFilterDone")
    filterDoneBtn.addEventListener("click", filterDoneBtnCallback)

    let filterTodoBtn = document.getElementById("btnFilterTodo")
    filterTodoBtn.addEventListener("click", filterTodoBtnCallback)

    let noFilterBtn = document.getElementById("btnNoFilter")
    noFilterBtn.addEventListener("click", noFilterBtnCallback)

    let logoutBtn = document.getElementById("btnLogout")
    logoutBtn.addEventListener("click", logoutBtnCallback)

    let jsonBtn = document.getElementById("btnJSON")
    jsonBtn.addEventListener("click", jsonBtnCallback)

    initTasks()
})

/**
 * Initializes task cards from database
 */
function initTasks() {
    // userTasks from backend
    const tasks = JSON.parse(userTasks)
    for (let task of tasks) {
        addCard(task.id, task.content, task.status)
    }
}

/**
 * Changes task(card) status from "done" to "todo" or the other way
 * @param {HTMLElement} card 
 */
function changeStatus(card) {
    let btn = card.getElementsByClassName("card_done_button")[0]

    if (btn.innerText == "Done") {     
        card.dataset.status = "done"
        card.style.background = DONE_COLOR
        card.firstElementChild.style.textDecoration = "line-through"
        btn.innerText = "Restore"
        return "done"
    } else {
        card.dataset.status = "todo"
        card.style.background = TASK_COLOR
        card.firstElementChild.style.textDecoration = "None"
        btn.innerText = "Done"
        return "todo"
    }
}

/**
 * Adds new card for a task into the cards div
 * @param {String} id 
 * @param {String} content 
 * @param {String} status (done/todo)
 * @returns 
 */
function addCard(id, content = DEFAULT_CONTENT, status = DEFAULT_STATUS) {
    let adderCard = document.getElementsByClassName("new_card")[0]

    let div = document.createElement("div")
    div.innerHTML = TASK_CARD_HTML.trim()
    let card = div.firstChild
    adderCard.parentNode.insertBefore(card, adderCard)

    card.dataset.id = id

    card.dataset.status = status
    if (status == "done")
        changeStatus(card)
    
    let contentEl = card.getElementsByClassName("card_content")[0]
    contentEl.innerHTML = content
    contentEl.addEventListener("blur", updateContentCallback) //blur = on lost focus

    let doneBtn = card.getElementsByClassName("card_done_button")[0]
    let removeBtn = card.getElementsByClassName("card_remove_button")[0]

    doneBtn.addEventListener("click", doneBtnCallback);
    removeBtn.addEventListener("click", removeBtnCallback);

    return card
}

/* ----------------------------------- */
/* CALLBACKS */
/* ----------------------------------- */

function updateContentCallback(event) {
    let card = event.target.parentElement
    let id = card.dataset.id
    let status = card.dataset.status
    let content = card.getElementsByClassName("card_content")[0].innerHTML
    const baseUrl = window.location.origin
    window.location = baseUrl + `/updateTask?id=${id}&status=${status}&content=${content}`
}

function addBtnCallback(event) {
    const baseUrl = window.location.origin
    window.location = baseUrl + `/addTask?status=${DEFAULT_STATUS}&content=${DEFAULT_CONTENT}`
}

function doneBtnCallback(event) {
    let card = event.target.parentElement.parentElement
    let id = card.dataset.id
    let status = changeStatus(card)

    const baseUrl = window.location.origin
    window.location = baseUrl + `/updateTask?id=${id}&status=${status}`
}

function removeBtnCallback(event) {
    let card = event.target.parentElement.parentElement
    let id = card.dataset.id
    card.remove()
    const baseUrl = window.location.origin
    window.location = baseUrl + `/removeTask?id=${id}`
}

function filterDoneBtnCallback(event) {
    let cards = document.getElementsByClassName("cards")[0].children
    for (let c of cards) {
        c.style.display = ""
        if (c.dataset.status != null && c.dataset.status != "done") {
            c.style.display = 'none' 
        }
    }
}

function filterTodoBtnCallback(event) {
    let cards = document.getElementsByClassName("cards")[0].children
    for (let c of cards) {
        c.style.display = ""
        if (c.dataset.status != null && c.dataset.status != "todo") {
            c.style.display = 'none' 
        }
    }
}

function noFilterBtnCallback(event) {
    let cards = document.getElementsByClassName("cards")[0].children
    for (let c of cards) {
        c.style.display = ""
    }
}

function logoutBtnCallback(event) {
    const baseUrl = window.location.origin
    window.location = baseUrl + "/logout"
}

function jsonBtnCallback(event) {
    const baseUrl = window.location.origin
    window.location = baseUrl + "/json"
}

