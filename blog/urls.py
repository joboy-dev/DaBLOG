from django.urls import path

from blog import views

app_name = 'blog'
urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('my-blogs/', views.GetMyPostsView.as_view(), name='my-posts'),

    path('post-create/', views.CreatePost.as_view(), name='new-post'),
    path('post-detail/<int:pk>', views.GetPostDetail.as_view(), name='post-details'),
    path('post-update/<int:pk>', views.UpdatePost.as_view(), name='post-update'),
    path('post-delete/<int:pk>', views.DeletePost.as_view(), name='post-delete'),
]
