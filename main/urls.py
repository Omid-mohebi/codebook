from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='main-home'),
    path('group/<str:pk>/', views.group, name='group-veiw')
]
