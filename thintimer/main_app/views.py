
###############################################################################
# IMPORTS
###############################################################################

# Standard library imports.
from datetime import datetime, timedelta

# Third-party imports: Django natives.
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render

# Third-party imports: Django DRF.
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.response import Response

# Third-party imports: Other.
from openpyxl import Workbook

# Local imports.
from .models import Entry, Task
from .serializers import EntrySerializer, TaskSerializer

###############################################################################
# MODEL VIEWSETS
###############################################################################

class TaskViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for handling tasks.
    
    Attributes
    ----------
    serializer_class : TaskSerializer
        The serializer class for Task objects.
    permission_classes : list
        List of permission classes. Only authenticated users are allowed.

    Methods
    -------
    get_queryset()
        Returns queryset for tasks belonging to the authenticated user.
    perform_create(serializer)
        Associates tasks with the authenticated user.
    partial_update(request, *args, **kwargs)
        Handles partial updates to Task objects.

    Returns
    -------
    Response
        A DRF Response object containing serialized data or errors.
    """
    
    # Initialize serializer and permissions
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Returns a queryset for tasks that belong to the authenticated user.

        Returns
        -------
        QuerySet
            A QuerySet of Task objects.
        """
        return Task.objects.filter(user=self.request.user).order_by('-created_at')

    def perform_create(self, serializer):
        """
        Save the authenticated user as the user associated with the task.

        Parameters
        ----------
        serializer : TaskSerializer
            A serializer containing validated Task data.

        Returns
        -------
        None
        """
        serializer.save(user=self.request.user)

    def partial_update(self, request, *args, **kwargs):
        """
        Implement partial update for a task.

        Parameters
        ----------
        request : Request
            HTTP request containing data to update.
        args : tuple
            Positional arguments.
        kwargs : dict
            Keyword arguments.

        Returns
        -------
        Response
            A DRF Response object containing serialized data or errors.
        """
        instance = self.get_object()  # Retrieve the task instance.
        serializer = self.get_serializer(instance, data=request.data, partial=True)  # Perform partial update.

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EntryViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for handling entries.
    
    Attributes
    ----------
    serializer_class : EntrySerializer
        The serializer class for Entry objects.
    permission_classes : list
        List of permission classes. Only authenticated users are allowed.
        
    Methods
    -------
    get_queryset()
        Returns queryset for entries belonging to the authenticated user.
    perform_create(serializer)
        Saves a new entry.
    get_entries_for_date(request, date=None, **kwargs)
        Filters entries based on a given date.
        
    Returns
    -------
    Response
        A DRF Response object containing serialized data or errors.
    """

    serializer_class = EntrySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Returns a queryset for entries that belong to the authenticated user.
        
        Returns
        -------
        QuerySet
            A QuerySet of Entry objects.
        """
        return Entry.objects.filter(task__user=self.request.user).order_by('-start_time')

    def perform_create(self, serializer):
        """
        Save a new entry.
        
        Parameters
        ----------
        serializer : EntrySerializer
            A serializer containing validated Entry data.
        
        Returns
        -------
        None
        """
        serializer.save()
    
    @action(detail=False, methods=['GET'], url_path='(?P<date>\d{4}-\d{2}-\d{2})')
    def get_entries_for_date(self, request, date=None, **kwargs):
        """
        Filters entries for a given date.
        
        Parameters
        ----------
        request : Request
            HTTP request containing data to filter by date.
        date : str
            Date string in YYYY-MM-DD format.
        kwargs : dict
            Keyword arguments.
            
        Returns
        -------
        Response
            A DRF Response object containing serialized data.
        """

        # Convert the date string to a datetime object
        date_obj = datetime.strptime(date, '%Y-%m-%d').date()
        
        # Filter entries by the given date
        entries = Entry.objects.filter(task__user=request.user, start_time__date=date_obj)
        
        # Serialize the entries
        serializer = EntrySerializer(entries, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

###############################################################################
# DJANGO REST API FRAMEWORK (DRF) VIEWS
###############################################################################

@api_view(['GET'])
def generate_report(request):
    """
    Generate a report based on task entries within a specified date range.

    Parameters
    ----------
    request : Request
        HTTP request containing query parameters for date range.

    Returns
    -------
    Response
        A DRF Response object containing aggregated task data or errors.
    """
    
    start_date_str = request.GET.get('startDate', None)
    end_date_str = request.GET.get('endDate', None)
    frequency = request.GET.get('frequency', 'daily')

    # Validate date inputs
    if not start_date_str or not end_date_str:
        return Response({"error": "Start and end dates are required"}, status=status.HTTP_400_BAD_REQUEST)

    # Convert string dates to datetime objects
    start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
    end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()

    # Fetch entries within the date range.
    entries = Entry.objects.filter(start_time__date__range=(start_date, end_date))

    # Initialize the result dictionary for data aggregation.
    result = {}
    
    # Aggregate entry data
    for entry in entries:
        task = entry.task
        task_id = task.id
        if task_id not in result:
            result[task_id] = {
                'name': task.name,
                'description': task.description,
                'tags': task.tags.split(',') if task.tags else [],
                'total_time': 0
            }
        # Update the total time for the task.
        result[task_id]['total_time'] += entry.total_time().total_seconds()

    return Response(result, status=status.HTTP_200_OK)

###############################################################################
# DJANGO NATIVE API VIEWS
###############################################################################

def generate_xlsx_report(request):
    """
    Generate an Excel report based on time tracking data for tasks and entries.
    
    Parameters
    ----------
    request : HttpRequest
        The request object containing query parameters that specify the start date, end date, and frequency for the report.
    
    Attributes
    ----------
    start_date_str : str
        The start date in string format as passed in the query parameters.
    end_date_str : str
        The end date in string format as passed in the query parameters.
    frequency : str
        The frequency for the report, can be 'daily' or 'monthly'.
    start_date : datetime.date
        The start date in datetime format.
    end_date : datetime.date
        The end date in datetime format.
    
    Returns
    -------
    HttpResponse
        An HTTP response containing the generated Excel report as an attachment.
    """
    
    # Retrieve query parameters for start date, end date, and frequency.
    start_date_str = request.GET.get('startDate')
    end_date_str = request.GET.get('endDate')
    frequency = request.GET.get('frequency')
    
    # Convert string dates to datetime objects.
    start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
    end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
    
    # Initialize a new Excel workbook and worksheet.
    wb = Workbook()
    ws = wb.active
    ws.title = "Report"
    
    # Define the headers for the worksheet
    headers = ['Task Name', 'Task Description', 'Tags']
    
    # Initialize an empty list to store date range
    date_range = []
    
    # Populate date range based on frequency
    if frequency == 'daily':
        delta = end_date - start_date
        for i in range(delta.days + 1):
            day = start_date + timedelta(days=i)
            date_range.append(day.strftime('%Y-%m-%d'))
    elif frequency == 'monthly':
        # Assumes start and end date are in the same year.
        for month in range(start_date.month, end_date.month + 1):
            date_range.append(datetime(start_date.year, month, 1).strftime('%Y-%m'))
    
    # Extend headers with the populated date range.
    headers.extend(date_range)
    ws.append(headers)
    
    # Fetch tasks data.
    tasks = Task.objects.all()
    
    # Iterate through tasks to populate worksheet.
    for task in tasks:
        row = [task.name, task.description, task.tags]
        time_data = [0] * len(date_range)  # Initialize time data.
        
        # Fetch entries related to the task and within the specified date range.
        entries = Entry.objects.filter(task=task, start_time__gte=start_date, end_time__lte=end_date)
        
        # Calculate total time for entries
        for entry in entries:
            total_time = entry.total_time().total_seconds() / 3600  # Convert to hours.
            if frequency == 'daily':
                index = (entry.start_time.date() - start_date).days
            elif frequency == 'monthly':
                index = entry.start_time.month - start_date.month
            time_data[index] += total_time
        
        # Extend row with the calculated time data.
        row.extend(time_data)
        ws.append(row)
    
    # Prepare HTTP response to return Excel file.
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=report.xlsx'
    
    # Save workbook to response.
    wb.save(response)
    
    return response

###############################################################################
# PAGE RENDERING
###############################################################################

def homepage_view(request):
    """
    Render the homepage view.

    Parameters
    ----------
    request : HttpRequest
        The request object that triggered this view.

    Returns
    -------
    HttpResponse
        The HttpResponse object that contains the rendered homepage HTML.
    """
    return render(request, 'homepage.html')

def task_management_view(request):
    """
    Render the task management view.

    Parameters
    ----------
    request : HttpRequest
        The request object that triggered this view.

    Returns
    -------
    HttpResponse
        The HttpResponse object that contains the rendered task management HTML.
    """
    return render(request, 'task_management.html')

def edit_entries(request):
    """
    Render the edit entries view.

    Parameters
    ----------
    request : HttpRequest
        The request object that triggered this view.

    Returns
    -------
    HttpResponse
        The HttpResponse object that contains the rendered edit entries HTML.
    """
    return render(request, 'edit_entries.html')

def timer(request):
    """
    Render the timer view.

    Parameters
    ----------
    request : HttpRequest
        The request object that triggered this view.

    Returns
    -------
    HttpResponse
        The HttpResponse object that contains the rendered timer HTML.
    """
    return render(request, 'timer.html')

def run_reports(request):
    """
    Render the run reports view.

    Parameters
    ----------
    request : HttpRequest
        The request object that triggered this view.

    Returns
    -------
    HttpResponse
        The HttpResponse object that contains the rendered run reports HTML.
    """
    return render(request, 'run_reports.html')