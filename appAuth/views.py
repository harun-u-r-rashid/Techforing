
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
)


from rest_framework import status
from rest_framework.response import Response

from . import serializers
from .models import User, OneTimePassword
from .utils import send_code_to_activate_user_account

from drf_spectacular.utils import extend_schema


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = serializers.RegisterSerializer
    @extend_schema(
        description="Register a new user and send an activation OTP code to the user's email. Use a valid email address so that you can verify your account.",

    )

    def post(self, request):

        serializer = serializers.RegisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            user_data = serializer.data

            send_code_to_activate_user_account(user_data["email"])
            return Response(
                {
                    "data": user_data,
                    "message": "A passcode has been sent to your email",
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyUserView(APIView):
    permission_classes = [AllowAny]
    serializer_class = serializers.OTPCodeSerializer
    @extend_schema(
        description="Verify the user account by using otp code from your email.",

    )

    def post(self, request):
        serializer = serializers.OTPCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        otp_code = serializer.validated_data.get("otp")

        try:
            user_code = OneTimePassword.objects.get(code=otp_code)
            user = user_code.user
            if not user.is_active:
                user.is_active = True
                user.save()
                return Response(
                    {"message": "Email verified successfully."},
                    status=status.HTTP_200_OK,
                )
            return Response(
                {"message": "Code is not valid"}, status=status.HTTP_204_NO_CONTENT
            )
        except OneTimePassword.DoesNotExist:
            return Response(
                {"message": "Passcode not provided.."},
                status=status.HTTP_400_BAD_REQUEST,
            )


class LoginView(APIView):
    serializer_class = serializers.LoginSerializer
    permission_classes = [AllowAny]

    @extend_schema(
        description="User login by using email and password.",

    )

    def post(self, request):

        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserDetailsView(generics.RetrieveAPIView):
    serializer_class = serializers.UserSerializer
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    lookup_field = "id"

    @extend_schema(
        description="It will response the details of the user. Give a valid id of user",

    )



    def get_user(self):
        id = self.kwargs["id"]
        user = User.objects.get(id=id)
        return user


class UserUpdateView(generics.UpdateAPIView):
    serializer_class = serializers.UserUpdateSerializer
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    lookup_field = "id"

    @extend_schema(
        description="It will update the user information. Give a valid id of user",

    )

    def perform_update(self, serializer):
        serializer.save()
        return serializer.data


class UserDeleteView(generics.DestroyAPIView):
    serializer_class = serializers.UserSerializer
    permission_classes = [AllowAny]
    queryset = User.objects.all()
    lookup_field = "id"

    @extend_schema(
        description="It will delete the user. Give a valid id of user.",
    )

    def destroy(self, request, *args, **kwargs):
        user = self.get_object()
        user.delete()
        return Response({"message":"User deleted successfully"},status=status.HTTP_204_NO_CONTENT)
