from django.urls import path
from . import views

app_name = 'forum'
urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_template, name='login'),
    path('register_user/', views.register_user, name='register_user'),
    path('login_user/', views.login_user, name='login_user'),
    path('savepost/', views.savepost, name='savepost'),
    path('logout/', views.logout_user, name='logout'),
    path('edit_post/', views.edit_post, name='edit_post'),
    path('delete_post/', views.delete_post, name="delete_post"),
    path('test_recursion/', views.test_recursion, name='test_recursion')
    
]