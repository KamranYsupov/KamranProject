const createDivClose = document.querySelector('#close-create-div')
const createDivOpen = document.querySelector('#open-create-div')
const createDiv = document.querySelector('#create-div')

const profileMenuOpenSubmit = document.querySelector('#open-profile-menu-submit')
const profileMenuCloseSubmit = document.querySelector('#close-profile-menu-submit')
const profileMenuDiv = document.querySelector('#profile-menu-div')


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

profileMenuOpenSubmit.onclick = function(e) {
    e.preventDefault()

    profileMenuOpenSubmit.classList.add('hidden')
    profileMenuCloseSubmit.classList.remove('hidden')
    profileMenuDiv.classList.remove('hidden')

    console.log('profile-menu is opened')

    return false
}


profileMenuCloseSubmit.onclick = function(e) {
    e.preventDefault()

    profileMenuCloseSubmit.classList.add('hidden')
    profileMenuOpenSubmit.classList.remove('hidden')
    profileMenuDiv.classList.add('hidden')

    console.log('profile-menu is closed')

    return false
}
