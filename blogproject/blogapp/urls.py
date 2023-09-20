from django.urls import path
from . import views 


urlpatterns = [
    path('', views.log_in,name='login'),
    path('register/', views.register,name='register'),
    path('home/',views.home,name='home'),
    path('create/',views.BlogCreateView.as_view(),name='create'),
    path('home/<int:pk>/', views.BlogDetailView.as_view(), name='detail'),
    path('update/<int:pk>/',views.edit_blog_post,name='update'),
    path('delete/<int:pk>/',views.delete_blog_post,name='delete'),
    path('logout/',views.logout_user,name='logout'),
    path('comment/<int:pk>/', views.comment_post, name='comment')

   
]

