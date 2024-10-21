from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework.decorators import api_view # type: ignore
from rest_framework.response import Response # type: ignore
from rest_framework import status
from django.contrib.auth import authenticate
from .models import Grievance
from .serializers import GrievanceSerializer, SignupSerializer 

# Create your views here.
@api_view(['POST'])
def signup_user(request):
    serializer = SignupSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()  # This will hash the password due to the save method in your model
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login_user(request):
    email = request.data.get('email')
    password = request.data.get('password')

    # Check if both fields are provided
    if not email or not password:
        return Response({'error': 'Email and password are required'}, status=status.HTTP_400_BAD_REQUEST)

    print("Email:", email)  # Debug print
    print("Password:", password)  # Debug print

    try:
        # Get the user by email
        user = User.objects.get(email=email)
        # Authenticate using the username (not email) and password
        user = authenticate(username=user.username, password=password)
        
        if user is not None:
            # Successful authentication
            return Response({'token': 'your_token', 'user': user.username}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    
    except User.DoesNotExist:
        return Response({'error': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)
    

@api_view(['GET'])
def get_grievances(request):
    grievances = Grievance.objects.all()
    serializer = GrievanceSerializer(grievances, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def post_grievance(request):
    serializer = GrievanceSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def grievance_details(request, pk):
    try:
        grievance = Grievance.objects.get(pk=pk)
    except Grievance.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = GrievanceSerializer(grievance)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = GrievanceSerializer(grievance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        grievance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
