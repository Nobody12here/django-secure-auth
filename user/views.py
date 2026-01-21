from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from drf_spectacular.utils import extend_schema
from .serializers import LoginSerializer, LogoutSerializer


@extend_schema(
    methods=["POST"],
    request=LoginSerializer,
    responses={
        400: "Email or password not provided !",
        401: "Please check credentials or register!",
        200: "Sucessfully",
    },
)
@api_view(["POST"])
def login(request: Request):
    email = request.data.get("email")
    password = request.data.get("password")
    if (not email) or (not password):
        return Response(
            {"error": "Email or password not provided !"},
            status=status.HTTP_400_BAD_REQUEST,
        )
    user = authenticate(request, email=email, password=password)
    if user is None:
        return Response(
            {"error": "Please check credentials or register!"},
            status=status.HTTP_401_UNAUTHORIZED,
        )
    else:
        if not user.is_active:
            return Response(
                {"error": "The user account is deactivated\nContact Admin"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        refresh_token = RefreshToken.for_user(user)
        return Response(
            {
                "access": str(refresh_token.access_token),
                "refresh": str(refresh_token),
                "user_id": user.id,
                "email": user.email,
            },
            status=status.HTTP_200_OK,
        )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def logout(request: Request):
    refresh_token = request.data.get("refresh_token")
    if not refresh_token:
        return Response(
            {"error": "Refresh token not provided!"}, status=status.HTTP_400_BAD_REQUEST
        )
    try:
        token = RefreshToken(refresh_token)
        if token.get("id") != request.user.id:
            return Response(
                {"error": "Token does not belong to the authenticated user"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        token.blacklist()
        return Response({"message": "Logout sucessfully"}, status=status.HTTP_200_OK)
    except TokenError:
        return Response(
            {"error": "Refresh token invalid or expired"},
            status=status.HTTP_400_BAD_REQUEST,
        )
