const openReplyButton = document.querySelector('#open_reply_button')
const closeReplyButton = document.querySelector('#close_reply_button')

const replyDiv = document.querySelector('#reply_div')
const replyForm = document.querySelector('#reply_form')

const commentsCount = document.getElementsByClassName('reply_div')

let elem = document.body

openReplyButton.onclick = function(e) {
  e.preventDefault()

  openReplyButton.classList.add('hidden')
  closeReplyButton.classList.remove('hidden')

  replyDiv.classList.remove('hidden')

  console.log('replies are opened!')
  console.log(commentsCount)

  return false
}

closeReplyButton.onclick = function(e) {
  e.preventDefault()

  openReplyButton.classList.remove('hidden')
  closeReplyButton.classList.add('hidden')

  replyDiv.classList.add('hidden')

  console.log('replies are closed!')

  return false
}




