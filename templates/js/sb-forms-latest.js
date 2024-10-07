// Wait for the DOM to fully load before running the script
window.addEventListener('DOMContentLoaded', event => {

    // Only proceed if there is a form on the page
    var form = document.querySelector('form');
    
    if (form) {
        // Add a submit event listener to the form
        form.addEventListener('submit', function(event) {
            var passwordInput = form.querySelector('input[name="password"]');
            
            if (passwordInput) {
                var password = passwordInput.value;
                
                // Disallow dangerous special characters: ', -, =
                var regex = /[\'\-=\;]/;
                if (regex.test(password)) {
                    alert("Invalid characters in password! The characters ', -, and = are not allowed.");
                    event.preventDefault(); // Prevent form submission if invalid characters are detected
                    return false;
                }
            }
        });
    }

     // Check if the URL has an error parameter (for incorrect password)
     var urlParams = new URLSearchParams(window.location.search);
     if (urlParams.has('error')) {
         // Display a pop-up alert for incorrect password
         alert("Incorrect password. Please try again.");
         event.preventDefault(); // Prevent form submission if invalid passwords are detected
   }

});


