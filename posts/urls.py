from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),
    path('posts/', views.posts, name='posts'),
    path('posts/<int:id>/',views.post_detail,name='post_detail'),
    path('register/',views.register,name='register'),
    path('login/',views.user_login,name='login'),
    path('logout/',views.user_logout,name='logout'),
    path('posts/create/',views.create_post,name='create_post'),
    path('posts/update/<int:id>/',views.update_post,name='update_post'),
    path('posts/delete/<int:id>/',views.delete_post,name='delete_post'),
]