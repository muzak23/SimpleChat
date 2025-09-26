let chatStream;
/**
 * Once the DOM is loaded, get the chat stream element and add an event
 * listener to the message send button
 * @param evt  The DOMContentLoaded event
 */
function onDOMContentLoaded(evt) {
    chatStream = document.getElementById('messages');
    document.getElementById('messageForm').addEventListener('submit', onMessageSubmit, false);
    attemptConnect();
}

document.addEventListener('DOMContentLoaded', onDOMContentLoaded, false);

/**
 * On scroll, if the user is at the top or bottom of the chat history, load more.
 * If a limit is reached, stop loading more.
 * @param evt  The scroll event
 */
function onScroll(evt) {
    if (chatStream.scrollTop === 0 && chatStream.children[0].id !== 'loading' && chatStream.children[0].id !== 'limit') {
        $('#messages').prepend('<div class="spinner-border text-primary" role="status" id="loading"><span class="visually-hidden">Loading...</span></div>');
        showHistory(chatStream.getElementsByTagName('message')[0].getAttribute('data-timestamp'));
        $('#loading').remove();

    }
}

/**
 * Attempts to connect to the server, and if successful, shows the chat history
 */
function attemptConnect() {
    socket.connect();
    console.log('attempting to connect')
    showHistory();

}

function scrollToBottom() {
    const out = document.getElementById("messages");
    out.scrollTop = out.scrollHeight - out.clientHeight;
}

let currentRoom = '';
function sameDay(date1, date2) {
    return date1.getFullYear() === date2.getFullYear() &&
    date1.getMonth() === date2.getMonth() &&
    date1.getDate() === date2.getDate();
}

/**
 * Formats epoch time into a string
 * @param epoch The epoch time
 * @returns {string} The formatted time
 */
function formatTime(epoch) {
    let message_date = new Date(epoch * 1000);
    let today = new Date();

    // is it today
    let isToday = sameDay(message_date, today);

    // is it yesterday
    let yesterday = new Date(message_date);
    yesterday.setDate(yesterday.getDate() + 1);
    let isYesterday = sameDay(yesterday, today);

    // Format example:   1:12 PM
    let time = message_date.getHours() % 12 + ":" + String(message_date.getMinutes()).padStart(2, "0") + " " + (message_date.getHours() >= 12 ? "PM" : "AM");

    if (isToday) {
        return "Today at " + time;
    } else if (isYesterday) {
        return "Yesterday at " + time;
    } else {
        return (message_date.getMonth() + 1) + "/" + message_date.getDate() + "/" + message_date.getFullYear() + " at " + time;
    }
}

/**
 * Creates an HTML element for a message
 * @param msg The formatted message data
 * @param isSelf If the message is written by the current user
 * @returns {HTMLDivElement} The HTML element for the message
 */
function createMessageHTML(msg, isSelf = false) {
    //     <div className="d-flex flex-row justify-content-start">
    //       <img src="https://www.gravatar.com/avatar/205e460b479e2e5b48aec07710c08d50"
    //         alt="avatar 1" style="width: 45px; height: 100%;" class="rounded">
    //       <div>
    //         <p class="small p-2 ms-3 mb-1 rounded-3" style="background-color: #d7d7d7;">Hi</p>
    //         <p class="small ms-3 mb-3 rounded-3 text-muted">23:58</p>
    //         </div>
    //     </div>

    let html = document.createElement('message');
    html.className = 'd-flex flex-row justify-content-start';
    html.setAttribute('data-timestamp', msg['timestamp'])

    let img = document.createElement('img');
    img.src = 'https://www.gravatar.com/avatar/205e460b479e2e5b48aec07710c08d50';
    img.alt = 'User Avatar';
    img.style = 'width: 52px; height: 100%; margin-top: 6px;';
    img.className = 'rounded';
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
    let p2 = document.createElement('p');
    p2.className = 'small ms-3 mb-3 rounded-3 text-muted';
    p2.textContent = formatTime(msg['timestamp']);
    div.appendChild(p2);

    html.appendChild(div);

    return html;
}

/**
 * Formats the message data into HTML and adds it to the 'messages' div
 * @param msg The message data
 * @param atTop Whether to add the message to the top of the chat history
 */
function showMsg(msg, atTop = false) {
    let messages = document.getElementById('messages');
    if (atTop) {
        let scrollTop = messages.scrollTop;
        messages.prepend(createMessageHTML(msg));
        messages.scrollTop = scrollTop + messages.children[0].getBoundingClientRect().height;
        return;
    }
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

function onMessageSubmit(evt) {
    if (document.getElementById('message').value === '') {
        evt.preventDefault();
        return;
    }
    let message_data = {
        'message': document.getElementById('message').value,
        'room': currentRoom
    };
    let full_message = {
        'username': localStorage.getItem('username'),
        'text': message_data['message'],
        'timestamp': Date.now() / 1000
    }
    let messages = document.getElementById('messages');
    let new_message = createMessageHTML(full_message, true);
    messages.appendChild(new_message);
    document.getElementById('message').value = '';
    // prevent default
    evt.preventDefault();

    scrollToBottom();
    socket.timeout(5000).emit('message', message_data, function (err, callback) {
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
}

/**
 * Adds an element that lets us know we have reached the limit of the chat history
 * @param top
 * @param remove
 */
function reachedLimit(top=false, remove=false) {
    console.log('reached limit')
    let messages = document.getElementById('messages');
    if (remove) {
        let limit = document.getElementById('limit');
        messages.removeChild(limit);
        return;
    }
    if (top) {
        let limit = document.createElement('div');
        limit.className = 'text-center';
        limit.id = 'limit';

        limit.textContent = 'This is the beginning of ' + currentRoom + '.';
        messages.prepend(limit);
    } else {
        messages.appendChild(limit);
    }
}

/**
 * Requests chat history from a current time and then creates HTML elements for each message in the correct place
 * @param before The time to get messages before
 * @param after The time to get messages after
 */
function showHistory(before=undefined, after=undefined) {
    socket.emit('getHistory', currentRoom, before, after, function (data) {
        if (before === undefined && after === undefined) {
            for (const msg of data.reverse()) {
                showMsg(msg)
            }
            if (data.length < 20) {
                reachedLimit(true);
            }
        } else if (before !== undefined) {
            console.log('gothistory of before', before, data)
            for (const msg of data) {
                showMsg(msg, true)
            }
            if (data.length < 20) {
                console.log('got history then reached top limit')
                reachedLimit(true);
            }
        } else if (after !== undefined) {
            for (const msg of data.reverse()) {
                showMsg(msg)
            }
        }
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
    localStorage.removeItem('username');
    socket.disconnect();
    const loginModal = new bootstrap.Modal(document.getElementById('loginModal'));
    loginModal.show();
}
