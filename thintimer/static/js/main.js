// main.js

// Add click event listener to the 'openTimerWindow' element
document.getElementById('openTimerWindow').addEventListener('click', function() {
    // Open a new window or tab at the '/timer' URL when the button is clicked.
    // The new window will have a width of 400px and height of 600px.
    window.open('/timer', '_blank', 'width=400,height=600');
});