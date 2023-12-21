from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserRegistrationSerializer, loginLogicSerializer
from django.contrib.auth import authenticate
from .serializers import UserProfileSerializer
from .models import loginLogic 
from django.http import JsonResponse


class UserRegistrationAPIView(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginAPIView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)

        if user:
            # Check if the UserProfile exists for the authenticated user
            try:
                profile = user.profile
            except loginLogic.DoesNotExist:
                profile = loginLogic.objects.create(user=user)

            if profile.first_login:
                return Response({'message': 'First login. Proceed to profile setup.'}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class UserProfileAPIView(APIView):
    def get(self, request, pk):
        profile = get_object_or_404(Profile, pk=pk)
        serializer = UserProfileSerializer(profile)
        return Response(serializer.data)

    def post(self, request):
        # Check if all required data is present
        required_fields = ['username', 'bio', 'interests', 'location', 'age', 'profileImage']
        if not all(field in request.data for field in required_fields):
            return JsonResponse(
                {'error': 'Please provide all required fields.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = UserProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)