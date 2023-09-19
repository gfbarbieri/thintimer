// Initialize variables
let currentTaskId = null;
let currentEntryId = null;
let timerInterval = null;
let startTime = null;
let isTimerRunning = false;

// Function to fetch tasks and populate the task list
function fetchTasks() {
    fetch('/api/tasks/')
    .then(response => response.json())
    .then(data => {
        const taskList = document.getElementById('taskList');
        taskList.innerHTML = '';

        data.forEach(task => {
            const listItem = document.createElement('li');
            listItem.classList.add('task-item');
            listItem.textContent = `${task.name} - ${task.total_time_spent || '00:00:00'}`;
            listItem.dataset.taskId = task.id;

            listItem.addEventListener('click', function() {
                event.stopPropagation();
                startTimer(task.id);
            });

            taskList.appendChild(listItem);
        });
    })
    .catch(error => {
        console.error('Error fetching tasks:', error);
    });
}

// Function to create a new entry
async function createEntry(taskId, startTime, endTime) {
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    const jsonData = {
        task: taskId,
        start_time: startTime.toISOString(),
        end_time: endTime.toISOString()
    };

    const response = await fetch('/api/entries/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify(jsonData),
    });

    const data = await response.json();
    return data.id;
}

// Function to update an existing entry
async function updateEntry(entryId, endTime) {
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    const jsonData = {
        end_time: endTime.toISOString()
    };

    await fetch(`/api/entries/${entryId}/`, {
        method: 'PATCH',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify(jsonData),
    });
}

// Function to start the timer for a task
function startTimer(taskId) {
    if (isTimerRunning && currentTaskId === taskId) {
        // Stop the timer if it's already running for the same task
        stopTimer();
    } else {
        console.log('Starting timer for task', taskId);

        // Stop any existing timer
        stopTimer();

        // Add 'is-active' class to the clicked task
        document.querySelector(`[data-task-id="${taskId}"]`).classList.add('is-active');
    
        // Record the start time
        startTime = new Date();  // Initialize startTime here
    
        // Create a new entry with the start time (and end time as the same)
        createEntry(taskId, startTime, startTime).then(entryId => {
            currentEntryId = entryId;
    
            // Start a new timer
            timerInterval = setInterval(function() {
                const now = new Date();
                const timeElapsed = new Date(now - startTime);
                const hours = String(timeElapsed.getUTCHours()).padStart(2, '0');
                const minutes = String(timeElapsed.getUTCMinutes()).padStart(2, '0');
                const seconds = String(timeElapsed.getUTCSeconds()).padStart(2, '0');
                
                document.getElementById('timerDisplay').textContent = `${hours}:${minutes}:${seconds}`;
            }, 1000);
    
            // Set the current task ID
            currentTaskId = taskId;
    
            isTimerRunning = true;
        });   
    }
}

// Function to stop the timer
function stopTimer() {
    console.log('Stopping timer');

    clearInterval(timerInterval);

    // Remove 'is-active' class from all tasks
    document.querySelectorAll('.task-item').forEach(item => {
        item.classList.remove('is-active');
    });

    if (currentTaskId !== null && currentEntryId !== null) {
        const endTime = new Date();
        updateEntry(currentEntryId, endTime).then(() => {
            // Refresh the task list to show the updated total time spent
            fetchTasks();
        });
    }

    currentTaskId = null;
    currentEntryId = null;
    isTimerRunning = false;
}

// Event listener for task clicks
document.addEventListener('click', function(event) {
    if (event.target.classList.contains('task-item')) {
        const taskId = event.target.getAttribute('data-task-id');
        startTimer(taskId);
    }
});

// Initial fetch to populate tasks
fetchTasks();
