# serializers.py

# Import necessary modules and functions from Django and REST framework.
from django.contrib.auth.models import User
from rest_framework import serializers

# Define serializers for user-related operations.

"""
Notes on base serializers:

1. UserLoginSerializer (derived from serializers.Serializer):
* Use Case: This serializer is designed for handling user login data.
* Characteristics:
    * It allows custom validation and processing of the incoming data.
    * You explicitly define each field and its validation rules, giving you
    fine-grained control over how the data is validated and processed.
    * Typically used when you need to validate data that doesn't map directly
    to a Django model or when you need to perform custom validation logic.

2. UserSignUpSerializer (derived from serializers.ModelSerializer):
* Use Case: This serializer is used for user signup and registration.
* Characteristics:
    * It automatically generates serialization and deserialization logic based
    on a Django model (User in this case).
    * The fields and their validation rules are inferred from the model's fields,
    reducing the need for explicit field definitions.
    * Convenient when you want to serialize/deserialize data that directly
    corresponds to a Django model.

In summary, the choice between serializers.Serializer and
serializers.ModelSerializer depends on your specific requirements and
whether you are working with data that aligns with a Django model (use
ModelSerializer) or data that requires more custom handling (use Serializer).
The flexibility of using Serializer allows you to define validation and
processing logic explicitly, while ModelSerializer simplifies the process
when your data closely matches a model's structure.

"""

class UserLoginSerializer(serializers.Serializer):
    """
    Serializer for user login data.

    This serializer is used to validate and serialize user login data.
    It includes fields for 'username' and 'password' (write-only).
    """
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

class UserSignUpSerializer(serializers.ModelSerializer):
    """
    Serializer for user signup data.

    This serializer is used to validate and serialize user signup data.
    It uses the User model and includes fields for 'username', 'email', and 'password'.
    """
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
