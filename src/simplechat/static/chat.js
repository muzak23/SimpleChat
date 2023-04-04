function onDOMContentLoaded(evt) {
    domStream = document.getElementById('messages');
    document.getElementById('inputForm').addEventListener('submit', onSubmit, false);


}
document.addEventListener('DOMContentLoaded', onDOMContentLoaded, false);


// Create a message in this format
// <div id="messages" className="chat_stream">
//     <div className="message ">
//         <img src="https://www.gravatar.com/avatar/205e460b479e2e5b48aec07710c08d50" alt="User Avatar">
//             <h3 className="message-author">Logan</h3>
//             <p className="message_text">{{ text['text'] }}</p>
//     </div>
// </div>

function createMessageDOM(text) {
let message = document.createElement('div');
    message.className = 'message';

    let img = document.createElement('img');
    img.src = 'https://www.gravatar.com/avatar/205e460b479e2e5b48aec07710c08d50';
    img.alt = 'User Avatar';
    message.appendChild(img);

    let h3 = document.createElement('h3');
    h3.className = 'message-author';
    h3.innerHTML = text['author'];
    message.appendChild(h3);

    let p = document.createElement('p');
    p.className = 'message_text';
    p.innerHTML = text['text'];
    message.appendChild(p);

    return message;
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

function sendMessage(message) {
    socket.emit('message', message);
}

socket.on('newMessage', function(data) {
    document.getElementById('messages').appendChild(createMessageDOM(data));
});

function onSubmit(evt) {
    sendMessage(document.getElementById('message').value);
    document.getElementById('message').value = '';
    // prevent default
    evt.preventDefault();

    return false;
}
