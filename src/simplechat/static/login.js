function onDOMContentLoaded(evt) {
    document.getElementById('loginForm').addEventListener('submit', onLoginSubmit, false);

    const myModal = new bootstrap.Modal('#onload');
    myModal.show();
}
document.addEventListener('DOMContentLoaded', onDOMContentLoaded, false);


function onLoginSubmit(evt) {
    login(document.getElementById('loginUsername').value);
    // prevent default
    evt.preventDefault();
    return false;
}

function login(username) {
    // socket.emit('login', username, function (data) {
    //     console.log('login returns', data)
    //     if (data) {
    //         document.getElementById('loginUsername').value = username
    //         const myModal = new bootstrap.Modal('#onload');
    //         myModal.hide();
    //     }
    // });
    $.ajax({
        type:'POST',
        url:'/login',
        data:{
          username:username
        },
        success:function(data)
        {
            console.log('login returns', data)
            if (data === '-1') {
                let error = document.getElementById('error')
                error.hidden = false
                error.innerHTML = '<strong>Invalid username</strong> Please choose a different username'
            } else if (data === '-2') {
                let error = document.getElementById('error')
                error.hidden = false
                error.innerHTML = '<strong>Username already taken</strong> Please choose a different username'
            } else if (data === '1') {
                $('#onload').modal('hide');
                localStorage.setItem("username", username);
                reconnect();
            }
        }
      })

}

function generateRandomName() {
    socket.emit('generateRandomName', function (data) {
        document.getElementById('loginUsername').value = data
    })
}
