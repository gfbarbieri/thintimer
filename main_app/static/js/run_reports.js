// Function to fetch and populate the report
function fetchAndPopulateReport() {
    const startDate = document.getElementById('startDate').value;
    const endDate = document.getElementById('endDate').value;
    const frequency = document.getElementById('frequency').value;

    // Fetch data from your API based on the selected parameters
    // Replace the URL with your actual API endpoint
    fetch(`/api/report?startDate=${startDate}&endDate=${endDate}&frequency=${frequency}`)
    .then(response => response.json())
    .then(data => {
        const reportTableBody = document.getElementById('reportTable').querySelector('tbody');
        reportTableBody.innerHTML = '';  // Clear existing rows
        console.log(data);  // Add this line to inspect the data

        // Loop through object keys
        Object.keys(data).forEach(taskId => {
            const row = data[taskId];
            const tableRow = document.createElement('tr');
            
            // Populate the Task column
            const taskCell = document.createElement('td');
            taskCell.textContent = row.name;
            tableRow.appendChild(taskCell);

            // Populate the Description column
            const descriptionCell = document.createElement('td');
            descriptionCell.textContent = row.description;
            tableRow.appendChild(descriptionCell);

            // Populate the Tags column
            const tagsCell = document.createElement('td');
            tagsCell.textContent = row.tags.join(', ');
            tableRow.appendChild(tagsCell);

            // Populate the Time Spent column
            const timeSpentCell = document.createElement('td');
            const totalSeconds = row.total_time;
            const hours = Math.floor(totalSeconds / 3600);
            const minutes = Math.floor((totalSeconds % 3600) / 60);
            const seconds = totalSeconds % 60;
            const roundedSeconds = Math.round(seconds * 10) / 10;
            timeSpentCell.textContent = `${hours}:${minutes}:${roundedSeconds}`;
            tableRow.appendChild(timeSpentCell);

            // const timeSpentCell = document.createElement('td');
            // timeSpentCell.textContent = row.total_time;
            // tableRow.appendChild(timeSpentCell);

            // Append the row to the table body
            reportTableBody.appendChild(tableRow);
        });
    })
    .catch(error => {
        console.error('Error fetching report:', error);
    });
}

// Event listener for the "Run Report" button
document.getElementById('runReportBtn').addEventListener('click', fetchAndPopulateReport);

document.getElementById('exportBtn').addEventListener('click', function(event) {
    event.preventDefault();  // Prevent default form submission

    const startDate = document.getElementById('startDate').value;
    const endDate = document.getElementById('endDate').value;
    const frequency = document.getElementById('frequency').value;

    // Create the URL with query parameters
    const url = `/api/generate_xlsx_report/?startDate=${startDate}&endDate=${endDate}&frequency=${frequency}`;

    // Fetch the XLSX file from the server
    fetch(url)
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.blob();
    })
    .then(blob => {
        // Create a blob URL and anchor element to trigger the download
        const blobUrl = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = blobUrl;
        a.download = 'report.xlsx';
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
    })
    .catch(error => {
        console.error('Error exporting report:', error);
    });
});
