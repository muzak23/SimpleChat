function onDOMContentLoaded(evt) {
    document.getElementById('loginForm').addEventListener('submit', onLoginSubmit, false);

}
document.addEventListener('DOMContentLoaded', onDOMContentLoaded, false);


function onLoginSubmit(evt) {
    login(document.getElementById('loginUsername').value);
    // prevent default
    evt.preventDefault();
    return false;
}

function login(username) {
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
            } else if (data === '1' || data === '0') {
                $('#loginModal').modal('hide');
                localStorage.setItem("username", username);
                attemptConnect();
            }
        }
      })

}

function generateRandomName() {
    $.ajax({
        type:'GET',
        url:'/generateRandomName',
        success:function(data) {
            console.log('generateRandomName returns', data)
            document.getElementById('loginUsername').value = data
        }
    })
}
