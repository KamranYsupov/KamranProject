const userId = JSON.parse(document.getElementById('user_id').textContent)

const webSocketProtocol = window.location.protocol === 'https:' ? 'wss' : 'ws';

const notificationSocket = new WebSocket(
  `${webSocketProtocol}://${window.location.host}/ws/notifications/${userId}/`
)


notificationSocket.onopen = function(e) {
     console.log('notification websocket is opened1');
     console.log(`${webSocketProtocol}://${window.location.host}/ws/notifications/${userId}/`)
}

notificationSocket.onclose = function(e) {
     console.log('notification websocket is closed');
}

notificationSocket.onmessage = function(e) {
     document.querySelector("#notifications-traker").classList.remove("hidden")
     const data = JSON.parse(e.data);
     console.log(document.querySelector("#notifications-traker"))

     var notification_span = document.createElement('span');
     notification_span.innerHTML = `<p>${ data.user_from_username } - <b>${ data.event_type }</p>`;

     document.querySelector("#notifications-div").appendChild(notification_span);
};
