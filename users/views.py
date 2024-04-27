from rest_framework import generics, status
from .serializers import UserSerializer, CustonRegisterSerializer
from .models import CustomUser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate



class UserList(generics.ListCreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


# class CurrentUser(generics.RetrieveAPIView):
#     serializer_class = UserSerializer
#     permission_classes = [IsAuthenticated]

#     def get_object(self):
#         return self.request.user
    

class CustomRegisterView(generics.CreateAPIView):
    serializer_class = CustonRegisterSerializer   
    
    def perform_create(self, serializer):
        user = serializer.save()
        if user:
            return Response(
                serializer.data,
                status = status.HTTP_201_CREATED )
        else:
            return Response(
                status = status.HTTP_400_BAD_REQUEST
            )
        

class UserLoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        
        
class CurrentUserView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    queryset = CustomUser.objects.all()