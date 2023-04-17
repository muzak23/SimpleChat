function onDOMContentLoaded(evt) {
    chatStream = document.getElementById('messages');
    document.getElementById('messageForm').addEventListener('submit', onMessageSubmit, false);

    showHistory();
}
document.addEventListener('DOMContentLoaded', onDOMContentLoaded, false);



function createMessageHTML(msg) {
    //     <div className="d-flex flex-row justify-content-start">
    //       <img src="https://www.gravatar.com/avatar/205e460b479e2e5b48aec07710c08d50"
    //         alt="avatar 1" style="width: 45px; height: 100%;" class="rounded">
    //       <div>
    //         <p class="small p-2 ms-3 mb-1 rounded-3" style="background-color: #d7d7d7;">Hi</p>
    //         <p class="small ms-3 mb-3 rounded-3 text-muted">23:58</p>
    //         </div>
    //     </div>

    let html = document.createElement('div');
    html.className = 'd-flex flex-row justify-content-start';

    let img = document.createElement('img');
    img.src = 'https://www.gravatar.com/avatar/205e460b479e2e5b48aec07710c08d50';
    img.alt = 'User Avatar';
    img.style = 'width: 45px; height: 100%;';
    img.className = 'rounded align-self-center';
    html.appendChild(img);

    let div = document.createElement('div');

    let p0 = document.createElement('p');
    p0.className = 'small ms-3 mb-0 rounded-3 text-muted';
    p0.textContent = msg['username'];
    div.appendChild(p0);

    let div2 = document.createElement('div');
    div2.className = 'd-inline-flex flex-row';

    let p1 = document.createElement('p');
    p1.className = 'small p-2 ms-3 mb-1 rounded-3 text-wrap';
    p1.style = 'background-color: #d7d7d7;';
    p1.textContent = msg['text'];
    div2.appendChild(p1);

    div.appendChild(div2)

    // let p2 = document.createElement('p');
    // p2.className = 'small ms-3 mb-3 rounded-3 text-muted';
    // p2.textContent = msg['time'];
    // div.appendChild(p2);

    html.appendChild(div);

    return html;
}

function showMsg(msg) {
    document.getElementById('messages').appendChild(createMessageHTML(msg));
}

const socket = io();
socket.on('connect', function(data) {
    console.log('connected with data:', data);
    socket.emit('my event', {data: "I'm connected!"});
});

socket.on('messageReceived', function() {
    console.log('messageReceived');
});

socket.on('newMessage', function(data) {
    showMsg(data);
});

function sendMessage(message) {
    socket.emit('message', message);
}

function onMessageSubmit(evt) {
    sendMessage(document.getElementById('message').value);
    document.getElementById('message').value = '';
    // prevent default
    evt.preventDefault();
    return false;
}

function showHistory() {
    socket.emit('getHistory', function (data) {
        for (const msg of data) {
            chatStream.insertBefore(createMessageHTML(msg), chatStream.firstChild);
    }})
}

function getUsername(id) {
    console.log('getting user', id)
    socket.emit('getUsername', id, function (data) {
        console.log('getUsername returns', data)
        return data
    })
}