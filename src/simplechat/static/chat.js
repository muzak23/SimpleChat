function onDOMContentLoaded(evt) {
    domStream = document.getElementById('messages');
    document.getElementById('inputForm').addEventListener('submit', onSubmit, false);
    showHistory();
}
document.addEventListener('DOMContentLoaded', onDOMContentLoaded, false);



function createMessageDOM(msg) {
    let html = document.createElement('div');
    html.className = 'message';

    let img = document.createElement('img');
    img.src = 'https://www.gravatar.com/avatar/205e460b479e2e5b48aec07710c08d50';
    img.alt = 'User Avatar';
    html.appendChild(img);

    let h3 = document.createElement('h3');
    h3.className = 'message-author';
    debug = msg['username']
    console.log(debug)
    h3.innerHTML = debug

    html.appendChild(h3);

    let p = document.createElement('p');
    p.className = 'message_text';
    p.innerHTML = msg['text'];
    html.appendChild(p);

    return html;
}

function showMsg(msg) {
    domStream.insertBefore(createMessageDOM(msg), domStream.firstChild);
}

const socket = io();
socket.on('connect', function() {
    socket.emit('my event', {data: "I'm connected!"});
});

socket.on('messageReceived', function() {
    console.log('messageReceived');
});

socket.on('newMessage', function(data) {
    document.getElementById('messages').appendChild(createMessageDOM(data));
});

function sendMessage(message) {
    socket.emit('message', message);
}

function onSubmit(evt) {
    sendMessage(document.getElementById('message').value);
    document.getElementById('message').value = '';
    // prevent default
    evt.preventDefault();
    return false;
}

function showHistory() {
    socket.emit('getHistory', function (data) {
        for (const msg of data) {
            showMsg(msg)
    }})
}

function getUsername(id) {
    console.log('getting user', id)
    socket.emit('getUsername', id, function (data) {
        console.log('getUsername returns', data)
        return data
    })
}


