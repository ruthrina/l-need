from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserRegistrationSerializer, loginLogicSerializer
from django.contrib.auth import authenticate
from .serializers import UserProfileSerializer
from .models import loginLogic 
from django.http import JsonResponse
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.shortcuts import get_object_or_404
from .models import UserProfile
from rest_framework.authtoken.models import Token

# ... (other imports)


class UserRegistrationAPIView(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"User Created successfully","user":serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginAPIView(APIView):
     def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)

        if user:
            # Check if the UserProfile exists for the authenticated user
            try:
                profile = user.profile  # Accessing the related profile
                if profile:
                    token = Token.objects.get_or_create(user=user)
                    print(token)
                    return Response({'message': 'Login successful. Profile exists.',"token":token[0].key}, status=status.HTTP_200_OK)
            except loginLogic.DoesNotExist:
                # If profile does not exist, create one
                profile = loginLogic.objects.create(user=user)
                return Response({'message': 'First login. Proceed to profile setup.'}, status=status.HTTP_200_OK)

        return Response({'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class UserProfileAPIView(APIView):
    authentication_classes = [TokenAuthentication]  # Add appropriate authentication classes
    permission_classes = [IsAuthenticated]  # Ensure the user is authenticated

    def get(self, request, pk):
        # Retrieve the user profile with the given primary key (pk)
        try:
            profile = UserProfile.objects.get(pk=pk)
            # Process and serialize the profile data
            serializer = UserProfileSerializer(profile)
            return Response(serializer.data)
        except UserProfile.DoesNotExist:
            return Response({"message": "User profile does not exist"}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        user = request.user  # Access the authenticated user
        required_fields = ['username', 'bio', 'interests', 'location', 'age']

        if not all(field in request.data for field in required_fields):
            return JsonResponse(
                {'error': 'Please provide all required fields.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Modify the serializer creation to include the user instance
        serializer = UserProfileSerializer(data=request.data, context={'user': user})

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        else:
            print("Serializer errors:", serializer.errors)  # Add this log to check serializer errors
            return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)