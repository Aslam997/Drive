from rest_framework import serializers
from .models import File, Permissions, Group, FileSharing
from users.models import CustomUser
from users.serializers import UserSerializer
import json




class PermissionsSerializer(serializers.ModelSerializer):

    file = serializers.SlugRelatedField(slug_field='name', queryset=File.objects.none(), required=True)
    user = serializers.SlugRelatedField(slug_field='username', queryset=CustomUser.objects.none(), required=True)

    def __init__(self, *args, **kwargs):
        super(PermissionsSerializer, self).__init__(*args, **kwargs)
        request = self.context.get('request', None)
        if request and hasattr(request, "user") and not request.user.is_anonymous:
            self.fields['file'].queryset = File.objects.filter(author=request.user)
            self.fields['user'].queryset = CustomUser.objects.exclude(id=request.user.id)

    class Meta:
        model = Permissions
        fields = '__all__'

class GroupSerializer(serializers.ModelSerializer):

    author = serializers.SlugRelatedField(slug_field='username', queryset=CustomUser.objects.none(), required=True)

    def __init__(self, *args, **kwargs):
        super(GroupSerializer, self).__init__(*args, **kwargs)
        request = self.context.get('request', None)
        if request and hasattr(request, "user") and not request.user.is_anonymous:
            self.fields['author'].queryset = CustomUser.objects.filter(id=request.user.id)

    class Meta:
        model = Group
        fields = '__all__'

class FileSerializer(serializers.ModelSerializer):

    group = serializers.SlugRelatedField(slug_field='name', queryset=Group.objects.none(), required=True)

    author = serializers.SlugRelatedField(slug_field='username', queryset=CustomUser.objects.none(), required=True)


    def __init__(self, *args, **kwargs):
        super(FileSerializer, self).__init__(*args, **kwargs)
        request = self.context.get('request', None)
        if request and hasattr(request, "user") and not request.user.is_anonymous:
            self.fields['group'].queryset = Group.objects.filter(author=request.user)
        if request and hasattr(request, "user"):
            self.fields['author'].queryset = CustomUser.objects.filter(id=request.user.id)

    class Meta:
        model = File
        fields = '__all__'



class FileSharingSerializer(serializers.ModelSerializer):

    user = serializers.SlugRelatedField(slug_field='username', queryset=CustomUser.objects.none(), required=True)

    file = serializers.SlugRelatedField(slug_field='name', queryset=File.objects.none(), required=True)

    def __init__(self, *args, **kwargs):
        super(FileSharingSerializer, self).__init__(*args, **kwargs)
        request = self.context.get('request', None)
        if request and hasattr(request, "user") and not request.user.is_anonymous:
            self.fields['user'].queryset = CustomUser.objects.exclude(id=request.user.id)
            self.fields['file'].queryset = File.objects.filter(author=request.user)

    
    class Meta:
        model = FileSharing
        fields = '__all__'

class ExchangeFileSerializer(serializers.Serializer):
    file = FileSerializer()
    user = UserSerializer()

    class Meta:
        model = FileSharing
        fields = '__all__'

class PermissionFileSerializer(serializers.Serializer):
    file = FileSerializer()
    user = UserSerializer()

    class Meta:
        model = Permissions
        fields = ['file', 'user', 'permission']