const createDivClose = document.querySelector('#close-create-div')
const createDivOpen = document.querySelector('#open-create-div')
const createDiv = document.querySelector('#create-div')

createDivOpen.onclick = function(e) {
    e.preventDefault()

    createDivOpen.classList.add('hidden')
    createDivClose.classList.remove('hidden')
    createDiv.classList.remove('hidden')

    console.log('create-div is opened')

    return false
}


createDivClose.onclick = function(e) {
    e.preventDefault()

    createDivClose.classList.add('hidden')
    createDiv.classList.add('hidden')
    createDivOpen.classList.remove('hidden')

    console.log('create-div is closed')

    return false
}
