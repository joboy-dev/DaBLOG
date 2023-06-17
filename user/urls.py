from django.urls import path

from . import views

app_name = 'user'
urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginV.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('user-details', views.UserDetails.as_view(), name='user-details'),
    path('user-profile-update/<int:pk>', views.UpdateUserProfile.as_view(), name='user-profile-update'),
    path('upload-profile-pic/<int:pk>', views.UploadProfilePicture.as_view(), name='upload-profile-pic')
]

