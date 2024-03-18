const createDivClose = document.querySelector('#close-create-div')
const createDivOpen = document.querySelector('#open-create-div')
const createDiv = document.querySelector('#create-div')

const profileMenuOpenSubmit = document.querySelector('#open-profile-menu-submit')
const profileMenuCloseSubmit = document.querySelector('#close-profile-menu-submit')
const profileMenuDiv = document.querySelector('#profile-menu-div')

const notificationsOpenSubmit = document.querySelector('#notifications-open-btn')
const notificationsCloseSubmit = document.querySelector('#notifications-close-btn')
const notificationsDiv = document.querySelector('#notifications-div')

createDivOpen.onclick = function(e) {
    e.preventDefault()

    createDivClose.classList.remove('hidden')
    createDiv.classList.remove('hidden')
    profileMenuDiv.classList.add('hidden')
    notificationsDiv.classList.add('hidden')

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

    profileMenuCloseSubmit.classList.remove('hidden')
    profileMenuDiv.classList.remove('hidden')
    createDiv.classList.add('hidden')
    notificationsDiv.classList.add('hidden')

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


notificationsOpenSubmit.onclick = function(e) {
    e.preventDefault()

    notificationsDiv.classList.remove('hidden')
    notificationsOpenSubmit.classList.add('hidden')
    notificationsCloseSubmit.classList.remove('hidden')
    profileMenuDiv.classList.add('hidden')
    createDiv.classList.add('hidden')

    console.log('notifications-div is opened!')

    return false

}

notificationsCloseSubmit.onclick = function(e) {
    e.preventDefault()

    notificationsDiv.classList.add('hidden')
    notificationsOpenSubmit.classList.remove('hidden')
    notificationsCloseSubmit.classList.add('hidden')

    console.log('notifications-dis is opened!')

    return false

}