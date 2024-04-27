from django.urls import path
from . import views

urlpatterns = [
    path('file/', views.FileList.as_view()),
    path('file/<int:pk>/', views.FileDetail.as_view()),
    path('group/', views.GroupList.as_view()),
    path('group/<int:pk>/', views.GroupDetail.as_view()),
    path('filesharing/', views.FileSharingList.as_view()),
    path('permission/', views.PermissionList.as_view()),
    path('permission/<int:pk>/', views.PermissionDetail.as_view()),
    path('sentfile/', views.SentFileList.as_view()),
    path('receivedfile/', views.ReceivedFileList.as_view()),  
    path('readlist/', views.ReadFileList.as_view()),  
    path("changelist/", views.ChangeFileList.as_view()),
]    