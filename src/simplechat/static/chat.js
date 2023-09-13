function onDOMContentLoaded(evt) {
    chatStream = document.getElementById('messages');
    document.getElementById('messageForm').addEventListener('submit', onMessageSubmit, false);
    attemptConnect();
}

function attemptConnect() {
    socket.connect();
    showHistory();

}

document.addEventListener('DOMContentLoaded', onDOMContentLoaded, false);

function scrollToBottom() {
    const out = document.getElementById("messages");
    // messages.scrollTop = messages.scrollHeight - messages.getBoundingClientRect().height;
    out.scrollTop = out.scrollHeight - out.clientHeight;
}


currentRoom = '';

function createMessageHTML(msg, isSelf = false) {
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
    p1.style.backgroundColor = '#d7d7d7';
    if (isSelf) {
        p1.style.color = '#878787';
    }
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
    let messages = document.getElementById('messages');
    let isAtBottom = messages.scrollHeight - messages.clientHeight <= messages.scrollTop + 1;
    messages.appendChild(createMessageHTML(msg));
    if (isAtBottom) {
        scrollToBottom();
    } else {
        console.log('not at bottom')
    }
}

const socket = io();

socket.on('messageReceived', function() {
    console.log('messageReceived');
});

socket.on('newMessage', function(data) {
    console.log('newMessage', data);
    showMsg(data);
});

// function sendMessage(message) {
//     socket.emit('message', message);
// }

function onMessageSubmit(evt) {
    let message = document.getElementById('message').value;
    let full_message = {
        'username': localStorage.getItem('username'),
        'text': message
    }
    let messages = document.getElementById('messages');
    let new_message = createMessageHTML(full_message, true);
    messages.appendChild(new_message);
    document.getElementById('message').value = '';
    // prevent default
    evt.preventDefault();

    scrollToBottom();
    socket.timeout(5000).emit('message', message, function (err, callback) {
        if (err || callback === 'invalidMessage') {
            console.log('message error', err, callback);
            new_message.children[1].children[1].children[0].style.color = 'red';
        } else if (callback === 'notAuthenticated') {
            new_message.children[1].children[1].children[0].style.color = 'red';
            const loginModal = new bootstrap.Modal(document.getElementById('loginModal'));
            loginModal.show();
        }
        else {
            console.log('message returns', callback);
            new_message.children[1].children[1].children[0].style.color = 'black';
        }
    });
    return false;
}

function showHistory() {
    socket.emit('getHistory', function (data) {
        for (const msg of data.reverse()) {
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

function join(room) {
    currentRoom = room;
    socket.emit('join', room , function (data) {
        console.log('join returns', data)
    });
}

socket.on('connected', function(data) {
    console.log('connected with data:', data);
    localStorage.setItem('username', data['username']);
});

socket.on('disconnect', (data) => {
    if (data === 'notAuthenticated') {
        const loginModal = new bootstrap.Modal(document.getElementById('loginModal'));
        loginModal.show();
    }
    console.log('disconnect because = ', data);
    // Disconnect socket
    socket.disconnect();
});

function reconnect() {
    socket.emit('reconnect', function (data) {
        console.log('reconnect returns', data)
    });
}

function logout() {
    socket.emit('logout', function (data) {
        console.log('logout returns', data)
    });
}
