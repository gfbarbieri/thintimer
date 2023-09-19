// Convert UTC time to local time
function convertUTCToLocal(utcDateString) {
    const date = new Date(utcDateString);
    const options = { hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: true };
    return date.toLocaleTimeString('en-US', options);
}

// 
function fetchEntriesForDate(date) {
    // Clear existing rows, otherwise, rows will append/duplicate.
    document.getElementById('entryTableBody').innerHTML = '';

    // 
    fetch(`/api/entries/${date.toISOString().split('T')[0]}`)
    .then(response => response.json())
    .then(data => {
        // Your existing code to populate the table goes here
        if (data.length > 0) {
            const entryTableBody = document.getElementById('entryTableBody');
            data.forEach(entry => {
                const row = document.createElement('tr');
                
                // Create and append the checkbox cell
                const checkboxCell = document.createElement('td');
                checkboxCell.innerHTML = `<input type="checkbox" class="entryCheckbox" data-entry-id="${entry.id}">`;
                row.appendChild(checkboxCell);

                const nameCell = document.createElement('td');
                nameCell.textContent = entry.task_name;
                row.appendChild(nameCell);
                
                const startTimeCell = document.createElement('td');
                startTimeCell.textContent = convertUTCToLocal(entry.start_time);
                row.appendChild(startTimeCell);
                
                const endTimeCell = document.createElement('td');
                endTimeCell.textContent = convertUTCToLocal(entry.end_time);
                row.appendChild(endTimeCell);

                const totalTimeCell = document.createElement('td');
                totalTimeCell.textContent = entry.total_time;
                row.appendChild(totalTimeCell);
                
                entryTableBody.appendChild(row);
            });
        } else {
            const entryTableBody = document.getElementById('entryTableBody');
            const row = document.createElement('tr');
            const cell = document.createElement('td');
            cell.textContent = 'No entries for this day';
            cell.setAttribute('colspan', '4');  // Assuming you have 4 columns
            row.appendChild(cell);
            entryTableBody.appendChild(row);
        }
    })
    .catch(error => {
        console.error('Error fetching entries:', error);
    });
}

// 
function deleteTasks() {
    const selectedTasks = Array.from(document.querySelectorAll('input[type="checkbox"]:checked')).map(checkbox => checkbox.getAttribute('data-entry-id'));
    const deletePromises = [];

    selectedTasks.forEach(taskId => {
        const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

        const deletePromise = fetch(`/api/entries/${taskId}/`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken
            },
        });
        deletePromises.push(deletePromise);
    });

    Promise.all(deletePromises)
    .then(() => {
        // Refresh the task list for the day after all deletions are complete.
        const selectedDate = document.getElementById('datePicker').value;
        fetchEntriesForDate(new Date(selectedDate));
    })
    .catch(error => {
        console.error('Error deleting tasks:', error);
    });
}

// 
document.addEventListener('DOMContentLoaded', function() {
    const currentDate = new Date();
    document.getElementById('datePicker').valueAsDate = currentDate; // Set the date picker to the current date
    fetchEntriesForDate(currentDate); // Fetch entries for the current date
});

// Format the date to YYYY-MM-DD for the API
// Update the date picker with the current date
document.getElementById('datePicker').valueAsDate = new Date();

// Event listener for the "Previous Day" button
document.getElementById('prevDayBtn').addEventListener('click', function() {
    // Get the current date from the date picker
    const datePicker = document.getElementById('datePicker');
    const currentDate = new Date(datePicker.value);
    
    // Subtract one day from the current date
    currentDate.setDate(currentDate.getDate() - 1);
    
    // Update the date picker with the new date
    datePicker.valueAsDate = currentDate;

    // Fetch entries for the new date
    fetchEntriesForDate(currentDate);
});

// 
document.getElementById('nextDayBtn').addEventListener('click', function() {
    // Get the current date from the date picker
    const datePicker = document.getElementById('datePicker');
    const currentDate = new Date(datePicker.value);

    // Add one day to the current date
    currentDate.setDate(currentDate.getDate() + 1);

    // Update the date picker with the new date
    datePicker.valueAsDate = currentDate;

    // Fetch entries for the new date
    fetchEntriesForDate(currentDate);
});

// 
const entryForm = document.getElementById('createEntryForm');

entryForm.addEventListener('submit', function(event) {
    const selectedDate = document.getElementById('datePicker').value; // Get the selected date

    event.preventDefault();
    
    // Extract form data
    const formData = new FormData(entryForm);
    
    // Convert to JSON
    const jsonData = {};
    
    formData.forEach((value, key) => {
        if (key === 'start_time' || key === 'end_time') {           
            // Create a new Date object for the selected date but using the current time
            const localDate = new Date(`${selectedDate}T${value}`);
            
            // Convert to UTC.
            value = localDate.toISOString();
        }        
        jsonData[key] = value;
    });

    // Make sure to use the task_id from the dropdown
    jsonData['task'] = document.getElementById('taskDropdown').value;

    // Send POST request to create a new entry
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    fetch('/api/entries/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify(jsonData),
    })
    .then(response => response.json())
    .then(data => {
        // Refresh the entries table
        fetchEntriesForDate(new Date(selectedDate));
    })
    .catch(error => {
        console.error('Error creating entry:', error);
    });
});

document.getElementById('showCreateEntryForm').addEventListener('click', function() {
    const formContainer = document.getElementById('createEntryFormContainer');

    // Toggle form display
    formContainer.style.display = (formContainer.style.display === 'none' || formContainer.style.display === '') ? 'block' : 'none';

    // If the form is now visible, fetch tasks
    if (formContainer.style.display === 'block') {
        // Clear existing options in the dropdown
        const taskDropdown = document.getElementById('taskDropdown');
        taskDropdown.innerHTML = '';

        // Fetch tasks and populate dropdown
        fetch('/api/tasks/')
        .then(response => response.json())
        .then(data => {
            data.forEach(task => {
                const option = document.createElement('option');
                option.value = task.id;
                option.textContent = task.name;
                taskDropdown.appendChild(option);
            });
        })
        .catch(error => {
            console.error('Error fetching tasks:', error);
        });
    }
});

// 
document.getElementById('datePicker').addEventListener('change', function() {
    const selectedDate = new Date(this.value);
    fetchEntriesForDate(selectedDate);
});

// 

document.getElementById('deleteSelectedEntries').addEventListener('click', function() {
    deleteTasks();
});

