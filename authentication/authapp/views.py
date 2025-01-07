from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import Vendor, Customer
from .serializers import VendorSerializer, CustomerSerializer, UserSerializer
from rest_framework.permissions import IsAuthenticated
# Generate JWT tokens
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class RegisterVendor(APIView):
    def post(self, request):
        serializer = VendorSerializer(data=request.data)
        if serializer.is_valid():
            user_data = serializer.validated_data.pop('user')
            user = User.objects.create_user(**user_data)
            Vendor.objects.create(user=user, **serializer.validated_data)
            return Response({'message': 'Vendor registered successfully!'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RegisterCustomer(APIView):
    def post(self, request):
        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid():
            user_data = serializer.validated_data.pop('user')
            user = User.objects.create_user(**user_data)
            Customer.objects.create(user=user, **serializer.validated_data)
            return Response({'message': 'Customer registered successfully!'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class RegisteredUsersView(APIView):
    permission_classes = [IsAuthenticated]  # Optional: If you want to restrict to logged-in users

    def get(self, request):
        # Fetch all registered users
        users = User.objects.all()  # Replace with CustomUser.objects.all() if you're using a custom user model

        # Serialize the users
        serializer = UserSerializer(users, many=True)

        # Return the serialized data
        return Response(serializer.data, status=status.HTTP_200_OK)


class Login(APIView):
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        # Validate if username is provided
        if not username:
            return Response({"detail": "Username is required."}, status=status.HTTP_400_BAD_REQUEST)

        # Validate if password is provided
        if not password:
            return Response({"detail": "Password is required."}, status=status.HTTP_400_BAD_REQUEST)

        # Authenticate user
        user = authenticate(username=username, password=password)
        
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'access': str(refresh.access_token),
                'refresh': str(refresh),
            })

        return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)