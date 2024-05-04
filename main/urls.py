from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='main-home'),
    path('group/<str:pk>/', views.group, name='group-veiw'),
    path('create-group/', views.create_group, name='create-group'),
    path('edit-group/<str:pk>/', views.edit_group, name='edit-group'),
]
