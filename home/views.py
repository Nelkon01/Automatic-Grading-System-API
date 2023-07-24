from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from home.models import User
from home.serializers import UserSerializers
from home.tokens import create_jwt_pair_for_user


class RegisterView(APIView):
    '''
    Creates a new *lecturer*, *student*, or admin user
    '''
    def post(self, request):
        serializer = UserSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            "status": "success",
            "data": serializer.data,
            "message": "user created"
        }, status=status.HTTP_201_CREATED)

class LoginViews(APIView):
    ''' Handles login requests i.e. authentication '''

    def post(self, request):
        email = request.data.get('login_id')
        password = request.data.get('password')

        user = authenticate(login_id=email, password=password)
        if not user:
            return Response({
                "status": "error",
                "message": "incorrect credentials"
            }, status=status.HTTP_401_UNAUTHORIZED)

        token = create_jwt_pair_for_user(user)

        serializer = UserSerializers(user)

        return Response({
            "status": "success",
            "data": serializer.data,
            "token": token,
            "message": "Login Successful"
        }, status=status.HTTP_200_OK)


class UserViews(APIView):
    ''' Handles user operations i.e. fetching user data and deleting users '''
    def get(self, request):
        user = request.user
        user = User.objects.filter(id=user.id).first()
        if not user:
            return Response({"status": "error", "data": [], "message": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = UserSerializers(user)

        return Response({
            "status": "success",
            "data": serializer.data,
            "message": "user details"
        }, status=status.HTTP_200_OK)

    def delete(self, request):
        user = request.user
        user = User.objects.filter(id=user.id).first()
        if not user:
            return Response({"status": "error", "data": [], "message": "User not found"},
                            status=status.HTTP_401_UNAUTHORIZED)

        user.soft_delete()
        return Response({"status": "success", "data": [], "message": "user deleted"})
