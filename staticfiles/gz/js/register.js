const signupSubmit = document.querySelector("#signupSubmit");


signupSubmit.addEventListener("click", (event) => {
    event.preventDefault();
    $.ajax({
    
        type: 'POST',
        url:'/registerf/',
        data: {
            first_name: $('#registerFirstname').val(),
            last_name: $('#registerLastname').val(),
            username: $('#registerUsername').val(),
            email: $('#registerEmail').val(),
            password1: $('#registerPassword1').val(),
            password2: $('#registerPassword2').val(),
            tel: $('#registerTel').val(),
        },
    
        beforeSend: function(xhr, settings) {
          xhr.setRequestHeader('X-CSRFToken', getCookie("csrftoken"));
        },
    
        success: function(response) {
            if (response.success) {
                console.log(response); 
				window.location.href = "/"
            }
            else{
                console.log(response);
                // Display error in the error div
                const errorMessageDiv = document.getElementById("errorMessage");
                errorMessageDiv.textContent = "Please fill in all fields. ";
                errorMessageDiv.style.display = "flex";
            }
        },
    
        error: function(error) {
          console.log(error);
          const errorMessageDiv = document.getElementById("errorMessage");
            errorMessageDiv.textContent = "An error occurred while processing your request.";
        }
    });
})


function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}