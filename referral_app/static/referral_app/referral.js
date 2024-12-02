document.addEventListener('DOMContentLoaded', function() {
    CheckInviteCode();
  
});
  

function CheckInviteCode() {

    const submit = document.querySelector("#submit");
    submit.disabled = true;

    document.querySelector('#invite-code-input').addEventListener('input', function() {
        const inviteCode = this.value;
        const token = document.querySelector('[name=csrfmiddlewaretoken]').value

        fetch('/api/check-invite-code/', {
            method: 'POST',
            headers: {
                "Content-Type": "application/json",
                'X-CSRFToken': token,

            },
            body: JSON.stringify({
              invite_code: inviteCode
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.valid) {
                console.log("Invite code is valid!");
                submit.disabled = false;
            } else {
                console.log("Invite code is invalid!");
                submit.disabled = true;
            }
        })
        .catch(error => {
            console.log('Error:', error);
        });
    })

}
