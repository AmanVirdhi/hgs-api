from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework.decorators import api_view # type: ignore
from rest_framework.response import Response # type: ignore
from rest_framework import status
from django.contrib.auth import authenticate
from .models import Grievance, Signup
from .serializers import GrievanceSerializer, SignupSerializer 
from django.contrib.auth.hashers import check_password

# Create your views here.
# @api_view(['POST'])
# def signup_user(request):
#     serializer = SignupSerializer(data=request.data)
#     if serializer.is_valid():
#         serializer.save()  # This will hash the password due to the save method in your model
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def signup_user(request):
    if request.method == 'POST':
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['POST'])
# def login_user(request):
#     email = request.data.get('email')
#     password = request.data.get('password')

#     if not email or not password:
#         return Response({'error': 'Email and password are required'}, status=status.HTTP_400_BAD_REQUEST)

#     try:
#         user = Signup.objects.get(email=email)
        
#         # Manually check the hashed password
#         if check_password(password, user.password):
#             return Response({'token': 'your_token', 'user': user.username}, status=status.HTTP_200_OK)
#         else:
#             return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    
#     except Signup.DoesNotExist:
#         return Response({'error': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def login_user(request):
    if request.method == 'POST':
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response({'error': 'Email and password are required'}, status=status.HTTP_400_BAD_REQUEST)

        user = None
        # Attempt to retrieve the user by email
        try:
            user = Signup.objects.get(email=email)
        except Signup.DoesNotExist:
            return Response({'error': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)

        # Check the hashed password
        if check_password(password, user.password):
            # Optionally, generate a token here if you're using token-based authentication
            token = 'your_token'  # Replace with actual token generation logic if necessary
            return Response({'token': token, 'user': user.username}, status=status.HTTP_200_OK)
        
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

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
