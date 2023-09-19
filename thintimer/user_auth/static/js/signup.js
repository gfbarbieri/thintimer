// In summary, this JavaScript code adds an event listener to a form's submit
// event. When the form is submitted, it prevents the default form submission,
// gathers user input data, sends it as JSON to a server endpoint for user
// signup, and based on the response, either redirects the user to a login
// page or displays an error message.

// This event listener ensures that the code inside it runs after the HTML document has been fully loaded.
document.addEventListener("DOMContentLoaded", function() {

    // Here, we're adding an event listener to the "submit" event of a form element with the id "signupForm."
    document.getElementById("signupForm").addEventListener("submit", function(event) {
        
        // Prevent the default form submission behavior, which would refresh the page.
        event.preventDefault();

        // Get values entered by the user in the form fields for username, email, and password.
        const username = document.getElementById("username").value;
        const email = document.getElementById("email").value;
        const password = document.getElementById("password").value;
        const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

        // Use the fetch function to send a POST request to the server's "/api/signup/" endpoint.
        fetch("/api/signup/", {
            method: "POST", // Specify the HTTP method as POST.
            headers: {
                "Content-Type": "application/json", // Set the request header for JSON data.
                'X-CSRFToken': csrftoken
            },
            body: JSON.stringify({ username, email, password }), // Convert user data to JSON and send it in the request body.
        })
        .then(response => response.json()) // Parse the response as JSON.
        .then(data => {
            // Check the response data to determine if the user was successfully created.
            if (data.status === "User created") {
                // Redirect the user to the login page ("/api/login/") if the user was created successfully.
                window.location.href = "/api/login/";
            } else {
                // If there was an error during user creation, display an alert to the user.
                alert("Could not create user.");
            }
        });
    });
});
