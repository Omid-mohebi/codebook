from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='main-home'),
    path('group/<str:pk>/', views.group, name='group-veiw'),
    path('create-group/', views.create_group, name='create-group'),
    path('edit-group/<str:pk>/', views.edit_group, name='edit-group'),
    path('delete-group/<str:pk>/', views.delete_group, name='delete-group'),
    path("login/", views.login_veiw, name="login"),
    path("logout/", views.logout_veiw, name="logout"),
    path("register/", views.register, name="register"),
    path('delete-message/<str:pk1>/<str:pk2>/', views.delete_message, name='delete-message'),
    path('users-profile/<str:pk>/', views.users_profile, name='users-profile'),

]
