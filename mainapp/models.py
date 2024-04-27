from django.db import models
from django.core.exceptions import ValidationError
from users.models import CustomUser

# Create your models here.


class Group(models.Model):
    name = models.CharField(max_length=255)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)


    def __str__(self):
        return self.name
class File(models.Model):
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to='files/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='files')
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='files')
    

    def save(self, *args, **kwargs):
        # Check if the author is a registered CustomUser
        if not CustomUser.objects.filter(pk=self.author_id).exists():
            raise ValueError('The specified author must be a registered CustomUser.')

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
class Permissions(models.Model):
    READ = 'read'
    CHANGE = 'change'
    PERMISSION_CHOICES = [
        (READ, 'Read'),
        (CHANGE, 'Change'),
    ]
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='permissions')
    file = models.ForeignKey(File, on_delete=models.CASCADE, related_name='permissions')
    permission = models.CharField(max_length=10, choices=PERMISSION_CHOICES)



    def __str__(self):
        return f"{self.user.username} - {self.permission} - {self.file.name}"
    

        

    def __str__(self):
        return self.user
    
class FileSharing(models.Model):
    file = models.ForeignKey(File, on_delete=models.CASCADE, related_name='shared_files')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='shared_files')
    shared_at = models.DateTimeField(auto_now_add=True)

   
        

    def __str__(self):
        return self.user


    
