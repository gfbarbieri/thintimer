# views.py

###############################################################################
# IMPORTS
###############################################################################

# Third-party imports: Django Native
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.shortcuts import render, redirect

# Third-party imports: Django DRF
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import UserLoginSerializer, UserSignUpSerializer

###############################################################################
# DJANGO REST API FRAMEWORK (DRF) VIEWS
###############################################################################

"""
Notes on the use of @api_view decorators in the Django REST framework.

The `@api_view` decorators are used in conjunction with Django REST framework
to define views for handling API requests. These decorators are part of Django
REST framework and serve specific purposes:

1. **`@api_view(['GET', 'POST'])`**:
    - Purpose: It indicates that the `user_login` view can handle HTTP GET and
    POST requests. In this context, it's used for user login functionality.
    - Effect: When a request is made to the associated URL with a supported HTTP
    method (GET or POST), the view function is invoked to handle the request.
    The decorator ensures that the view can only handle the specified HTTP
    methods.

3. **`@api_view(['POST'])`**:
    - Purpose: It indicates that the view can only handle HTTP POST requests.
    This view is used for user registration and signup.
    - Effect: It restricts the view to only respond to POST requests, ensuring
    that it's used specifically for submitting user registration data.

In summary, the `@api_view` decorators are used to specify the HTTP methods
that a view function can handle. These decorators are commonly used in Django
REST framework to create views for API endpoints that respond to specific HTTP
actions (e.g., GET, POST) and ensure that the views are appropriately mapped to
those actions.
"""

@api_view(['GET', 'POST'])
def user_login(request):
    """
    Handle user login requests.

    For POST requests, validate user login data and authenticate the user.
    If authentication is successful, log in the user and redirect to the home
    page. If authentication fails, return an error response.

    For GET requests, render the login.html template.

    Args:
        request: The HTTP request object.

    Returns:
        HTTP response, either a redirection or an error response.
    """

    # Handle GET requests for user login. For GET requests, render the
    # login.html template.
    if request.method == 'GET':
        return render(request, 'login.html')

    # Create a serializer to validate user login data.
    serializer = UserLoginSerializer(data=request.data)

    # If serializer validation fails, return a response with serializer
    # errors.
    if not serializer.is_valid():
        return render(request, 'login.html', {'errors': serializer.errors})
    
    # Extract username and password from validated data.
    username = serializer.validated_data['username']
    password = serializer.validated_data['password']

    # Authenticate the user.
    user = authenticate(username=username, password=password)

    # If authentication fails, return an error response.
    if not user:
        return render(request, 'login.html', {'error': "Invalid credentials"})
    
    # If authentication is successful, log in the user and redirect to
    # the home page.
    login(request, user)
    return redirect('home')

@api_view(['GET','POST'])
def user_logout(request):
    """
    Handle user logout requests.

    Log out the user and render the login.html template.

    Args:
        request: The HTTP request object.

    Returns:
        HTTP response, rendering the login.html template.
    """

    # Log the user out and render the login.html template.
    logout(request)
    return render(request, 'login.html')

@api_view(['POST'])
def user_signup(request):
    """
    Handle user signup requests.

    Validate user signup data, create a new user if data is valid, and return
    appropriate responses. If a user with the same email or username already
    exists, return an error response.

    Args:
        request: The HTTP request object.

    Returns:
        HTTP response, indicating success or an error.
    """

    # Create a serializer to validate user signup data.
    serializer = UserSignUpSerializer(data=request.data)
    
    # Handle serializer validation errors by rendering the signup page with
    # error messages.
    if not serializer.is_valid():
        # return render(request, 'signup.html', {'errors': serializer.errors})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # Extract username, email, and password from validated data.
    username = serializer.validated_data['username']
    email = serializer.validated_data['email']
    password = serializer.validated_data['password']

    # Check that email and username are not empty. If email or username
    # is empty, return an error response.
    if not (email and username):
        # return render(request, 'signup.html', {'error': "Both email
        # and username must be set"})
        return Response({"error": "Both email and username must be set"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # Create a new user with the provided username, email, and password.
        User.objects.create_user(username=username, email=email, password=password)
        # return redirect(reverse('user_login'))
        return Response({"status": "User created"}, status=status.HTTP_201_CREATED)
    except IntegrityError:
        # If a user with the same email or username already exists, return an
        # error response.
        # return render(request, 'signup.html', {'error': "A user with this email or username already exists."})
        return Response({"error": "A user with this email or username already exists."}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def update_username(request):
    """
    Updates the username of the authenticated user using Django Rest Framework.

    Parameters
    ----------
    request : Request
        The request object containing the new username in POST data.

    Returns
    -------
    Response
        Response object indicating the status of the operation.

    """
    # Extract the new username from POST data
    new_username = request.data.get('new_username')
    
    # Get the current authenticated user
    user = request.user
    
    # Update the username
    user.username = new_username
    
    # Save the updated user object
    user.save()
    
    # Return Response object indicating success
    return Response({'status': 'success'})

@api_view(['POST'])
def update_email(request):
    """
    Updates the email of the authenticated user.

    Parameters
    ----------
    request : HttpRequest
        The request object containing the new email in POST data.

    Returns
    -------
    Response
        JSON response indicating the status of the operation.

    """
    # Extract the new username from POST data
    new_email = request.data.get('new_email')  # Use request.data to access parsed content
    
    # Get the current authenticated user
    user = request.user

    # Update the username
    user.email = new_email

    # Save the updated user object
    user.save()
    
    # Return Response object indicating success
    return Response({'status': 'success'})

@api_view(['POST'])
def reset_password(request):
    """
    Resets the password for the authenticated user.

    Parameters
    ----------
    request : HttpRequest
        The request object containing old and new passwords in POST data.

    Returns
    -------
    Response
        JSON response indicating the status of the operation, and a message if the reset failed.

    """
    # Use request.data to access parsed content
    old_password = request.data.get('old_password')  
    new_password = request.data.get('new_password')  
    
    # Validate that required fields are present
    if not old_password or not new_password:
        return Response({'status': 'failure', 'message': 'Missing required fields'}, status=400)

    # Get the current authenticated user
    user = request.user

    # Check if the old password is correct
    if user.check_password(old_password):
        # Update the user's password
        user.set_password(new_password)
        user.save()

        # Refresh session to include new password
        update_session_auth_hash(request, user)

        return Response({'status': 'success'})
    else:
        return Response({'status': 'failure', 'message': 'Old password is incorrect'})

@api_view(['POST'])
def delete_account(request):
    """
    Deletes the authenticated user's account.

    Parameters
    ----------
    request : HttpRequest
        The request object.

    Returns
    -------
    Response
        JSON response indicating the status of the operation.

    """
    # Get the current authenticated user
    user = request.user

    # Delete the user account
    user.delete()

    # Return JSON response indicating success
    return Response({'status': 'success'})

###############################################################################
# PAGE RENDERING
###############################################################################

def project_homepage(request):
    """
    Render the project's homepage.

    Args:
        request: The HTTP request object.

    Returns:
        HTTP response, rendering the login.html template.
    """

    return render(request, 'login.html')

def signup_page(request):
    """
    Render the signup page.

    Args:
        request: The HTTP request object.

    Returns:
        HTTP response, rendering the signup.html template.
    """

    return render(request, 'signup.html')

def settings(request):
    """
    Render the settings page.

    Args:
        request: The HTTP request object.

    Returns:
        HTTP response, rendering the signup.html template.
    """

    return render(request, 'settings.html')
