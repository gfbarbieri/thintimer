// Function to handle username updates.
// It performs an API call to '/api/update_username/' to update the username.
function updateUsername(form) {

  // Collects form data
  const formData = new FormData(form);

  // CSRF token for security
  const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
  
  // Fetch API for updating username.
  fetch('/api/update_username/', {
    method: 'POST',
    headers: {
      'X-CSRFToken': csrftoken // CSRF token attached to request header.
    },
    body: formData
  })
  .then(response => response.json())
  .then(data => {
    if (data.status === 'success') {
      // If update is successful, clear the form fields.
      const newUsername = document.getElementById('newUsername').value;
      document.getElementById('newUsername').value = '';
      
      // Optionally update the username displayed somewhere in the UI.
      document.getElementById('usernameDisplay').textContent = newUsername;
    }
    // Optionally, handle success message or update UI here.
  })
  .catch(error => {
    // Handle errors.
  });
}

// Attach submit event listener to 'updateUsernameForm'.
document.getElementById('updateUsernameForm').addEventListener('submit', function(event) {
  event.preventDefault(); // Prevent default form submission.
  updateUsername(event.target); // Call function to handle username update.
});

// Function to handle email updates.
// It performs an API call to '/api/update_email/' to update the email.
function updateEmail(form) {
  // Collects form data.
  const formData = new FormData(form);

  // CSRF token for security.
  const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

  // Fetch API for updating email.
  fetch('/api/update_email/', {
    method: 'POST',
    headers: {
      'X-CSRFToken': csrftoken // CSRF token attached to request header.
    },
    body: formData
  })
  .then(response => response.json())
  .then(data => {
    if (data.status === 'success') {
      // If update is successful, clear the form fields.
      document.getElementById('newEmail').value = '';
    }
    // Optionally, handle success message or update UI here.
  })
  .catch(error => {
    // Handle errors
  });
}

// Attach submit event listener to 'updateEmailForm'.
document.getElementById('updateEmailForm').addEventListener('submit', function(event) {
  event.preventDefault();
  updateEmail(event.target);
});

// Function to handle password updates.
// It performs an API call to '/api/reset_password/' to update the email.
function resetPassword(form) {
  // Collects form data.
  const formData = new FormData(form);

  // CSRF token for security.
  const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

  // Fetch API for resetting password.
  fetch('/api/reset_password/', {
    method: 'POST',
    headers: {
      'X-CSRFToken': csrftoken // CSRF token attached to request header.
    },
    body: formData
  })
  .then(response => response.json())
  .then(data => {
    if (data.status === 'success') {
      // If update is successful, clear the form fields.
      document.getElementById('oldPassword').value = '';
      document.getElementById('newPassword').value = '';
    }
    // Optionally, handle success message or update UI here.
  })
  .catch(error => {
    // Handle errors
  });
}

// Attach submit event listener to 'resetPasswordForm'.
document.getElementById('resetPasswordForm').addEventListener('submit', function(event) {
  event.preventDefault();
  resetPassword(event.target);
});

// Function to handle account deletion.
// It performs an API call to '/api/delete_account/' to delete the user's account.
function deleteAccount() {
  const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

  // Fetch API for deleting account
  fetch('/api/delete_account/', {
    method: 'POST',
    headers: {
      'X-CSRFToken': csrftoken // CSRF token attached to request header.
    },
  })
  .then(response => {
    if (response.ok) {
      // If deletion is successful, redirect to home page.
      window.location.href = '/';
    }
  })
  .catch(error => {
    // Handle errors
  });
}

// Attach submit event listener to 'deleteAccountForm'.
document.getElementById('deleteAccountForm').addEventListener('submit', function() {
  deleteAccount(); // Call function to handle account deletion.
});
