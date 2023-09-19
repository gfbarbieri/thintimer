function fetchTasks() {
    // Clear existing rows, otherwise, rows will append/duplicate.
    document.getElementById('taskTableBody').innerHTML = '';

    fetch('/api/tasks/')
    .then(response => {
        return response.json();
    })
    .then(data => {
        const taskTableBody = document.getElementById('taskTableBody');

        data.forEach(task => {
            // Create a row.
            const row = document.createElement('tr');
            row.setAttribute('data-task-id', task.id);

            // Create a cell on the row for the checkbox.
            const checkboxCell = document.createElement('td');
            checkboxCell.innerHTML = `<input type="checkbox" class="task-checkbox" data-task-id="${task.id}">`;
            row.appendChild(checkboxCell);

            // Create a cell on the row for the task name.
            const nameCell = document.createElement('td');
            nameCell.textContent = task.name;
            nameCell.setAttribute('contenteditable', 'true');
            nameCell.setAttribute('class', 'editable-cell');
            nameCell.setAttribute('data-field', 'name');
            row.appendChild(nameCell);

            // Create a cell on the row for the task description.
            const descriptionCell = document.createElement('td');
            descriptionCell.textContent = task.description;
            descriptionCell.setAttribute('contenteditable', 'true');
            descriptionCell.setAttribute('class', 'editable-cell');
            descriptionCell.setAttribute('data-field', 'description');
            row.appendChild(descriptionCell);

            // Create a cell on the row for the tags. Tags are stored
            // as a string separated by commas. Turn the string into an
            // array before using join.
            let tags = task.tags;
            if (tags && !Array.isArray(tags)) {
                tags = tags.split(',');  // Convert string to array if needed
            }
            const tagsCell = document.createElement('td');
            tagsCell.textContent = tags ? tags.join(', ') : 'No tags';
            tagsCell.setAttribute('contenteditable', 'true');
            tagsCell.setAttribute('class', 'editable-cell');
            tagsCell.setAttribute('data-field', 'tags');
            row.appendChild(tagsCell);

            // Createa a cell on the row for the total time spent on the task.
            const totalTimeSpentCell = document.createElement('td');
            totalTimeSpentCell.textContent = task.total_time_spent;
            row.appendChild(totalTimeSpentCell);

            // Append the row to the table body.
            taskTableBody.appendChild(row);
        });
    })
    .catch(error => {
        console.error('Error fetching tasks:', error);
    });
}

function deleteTasks() {
    const selectedTasks = Array.from(document.querySelectorAll('input[type="checkbox"]:checked')).map(checkbox => checkbox.getAttribute('data-task-id'));
    const deletePromises = [];

    selectedTasks.forEach(taskId => {
        const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

        const deletePromise = fetch(`/api/tasks/${taskId}/`, {
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
        fetchTasks();  // Refresh the table only once after all deletions are complete
    })
    .catch(error => {
        console.error('Error deleting tasks:', error);
    });
}

document.addEventListener('DOMContentLoaded', function() {
    fetchTasks();
});

document.getElementById('deleteSelectedBtn').addEventListener('click', function() {
    const selectedCheckboxes = document.querySelectorAll('.task-checkbox:checked');
    const selectedTaskIds = Array.from(selectedCheckboxes).map(checkbox => checkbox.getAttribute('data-task-id'));

    deleteTasks(selectedTaskIds);
});

document.getElementById('showCreateTaskForm').addEventListener('click', function() {
    const formContainer = document.getElementById('createTaskFormContainer');

    formContainer.style.display = (formContainer.style.display === 'none' || formContainer.style.display === '') ? 'block' : 'none';
});

// CREATE NEW TASK.
const taskForm = document.getElementById('createTaskForm');

taskForm.addEventListener('submit', function(event) {
    event.preventDefault();
    
    // Extract form data
    const formData = new FormData(taskForm);

    // Convert to JSON
    const jsonData = {};
    
    formData.forEach((value, key) => {
        jsonData[key] = value;
    });

    // Send POST request to create a new task
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    fetch('/api/tasks/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify(jsonData),
    })
    .then(response => response.json())
    .then(data => {
        fetchTasks();
        document.getElementById('createTaskFormContainer').style.display = 'none';
    })
    .catch(error => {
        console.error('Error creating task:', error);
    });
});

// EDIT TASKS INLINE
document.getElementById('taskTableBody').addEventListener('blur', function(event) {
    if (event.target.classList.contains('editable-cell')) {
        
        const taskId = event.target.closest("tr").getAttribute("data-task-id");
        const field = event.target.getAttribute("data-field");
        const value = event.target.textContent;

        // Prepare data to send
        const data = {};
        data[field] = value;

        // Send PATCH request to update the task
        const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

        fetch(`/api/tasks/${taskId}/`, {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken
            },
            body: JSON.stringify(data),
        })
        .then(response => response.json())
        .then(data => {
        })
        .catch(error => {
            console.log('Error updating task:', error);
        });
    }
}, true);
