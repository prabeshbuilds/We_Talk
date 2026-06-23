from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Connection

User = get_user_model()

@api_view(['POST'])
def register(request):
    data = request.data

    user = User.objects.create(
        username=data['username'],
        email=data['email'],
        password=make_password(data['password']),
        age=data.get('age'),
        gender=data.get('gender'),
        location=data.get('location'),
    )

    return Response({"message": "User created", "user": user.username})

@api_view(['POST'])
def login(request):
    data = request.data
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return Response(
            {"detail": "Username and password are required."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    user = authenticate(request, username=username, password=password)
    if user is None:
        return Response(
            {"detail": "Invalid credentials."},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    refresh = RefreshToken.for_user(user)
    return Response(
        {
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "user": user.username,
        }
    )

@api_view(['GET'])
def api_root(request):
    return Response(
        {
            "message": "Welcome to Nepali Dating API",
            "endpoints": {
                "register": "/api/register/ (POST)",
                "login": "/api/login/ (POST)",
                "discover": "/api/discover/ (GET)",
                "connect": "/api/connect/<user_id>/ (POST)",
            },
        }
    )

@api_view(['GET'])
def discover_users(request):
    users = User.objects.exclude(id=request.user.id)
    serialized = [
        {
            "id": user.id,
            "username": user.username,
            "age": user.age,
            "gender": user.gender,
            "location": user.location,
            "bio": user.bio,
        }
        for user in users
    ]
    return Response(serialized)

@api_view(['POST'])
def send_request(request, user_id):
    sender = request.user
    receiver = get_object_or_404(User, id=user_id)

    if sender == receiver:
        return Response(
            {"detail": "Cannot send request to yourself."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    connection, created = Connection.objects.get_or_create(
        sender=sender,
        receiver=receiver,
    )

    if not created:
        return Response(
            {"detail": "Request already sent."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    return Response({"message": "Connection request sent."})

@api_view(['POST'])
def respond_request(request, connection_id):
    connection = get_object_or_404(Connection, id=connection_id)

    if connection.receiver != request.user:
        return Response(
            {"detail": "You are not authorized to respond to this request."},
            status=status.HTTP_403_FORBIDDEN,
        )

    action = request.data.get("action")
    if action not in ["accept", "reject"]:
        return Response(
            {"detail": "Invalid action. Use 'accept' or 'reject'."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    connection.status = "accepted" if action == "accept" else "rejected"
    connection.save()

    return Response({"message": f"Connection request {connection.status}."})