from rest_framework import generics
from .models import *
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q



class FileList(generics.ListCreateAPIView):
    queryset = File.objects.all()
    serializer_class = FileSerializer
    permission_classes = [IsAuthenticated]
    
    
    def get_queryset(self):
        user = self.request.user
        if not user.is_anonymous:
            return File.objects.filter(
                Q(author=self.request.user) | 
                ( Q(permissions__user=self.request.user) &
               ( Q(permissions__permission='read') | Q(permissions__permission='change'))))


class FileDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = FileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return File.objects.filter(
            Q(author=self.request.user) | (
            Q(group__author=self.request.user) & Q(permissions__permission='change')
            )
            )

   

    

class GroupList(generics.ListCreateAPIView):
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Group.objects.filter(author=self.request.user)

class GroupDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Group.objects.filter(author=self.request.user)

class FileSharingList(generics.CreateAPIView):
    queryset = FileSharing.objects.all()
    serializer_class = FileSharingSerializer
    permission_classes = [IsAuthenticated]



class PermissionList(generics.ListCreateAPIView):
    queryset = Permissions.objects.all()
    serializer_class = PermissionsSerializer
    permission_classes = [IsAuthenticated]

class PermissionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Permissions.objects.all()
    serializer_class = PermissionsSerializer
    permission_classes = [IsAuthenticated]

class SentFileList(generics.ListAPIView):
    serializer_class = ExchangeFileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return FileSharing.objects.filter(file__author=self.request.user)
    
class ReceivedFileList(generics.ListAPIView):
    serializer_class = ExchangeFileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return FileSharing.objects.filter(user=self.request.user)
    
class ReadFileList(generics.ListAPIView):
    serializer_class = PermissionFileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Permissions.objects.filter(permission='read', user=self.request.user)
    
class ChangeFileList(generics.ListAPIView):
    serializer_class = PermissionFileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Permissions.objects.filter(permission='change', user=self.request.user)