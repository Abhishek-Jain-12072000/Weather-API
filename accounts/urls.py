from .views import RegisterAPI
from django.urls import path
from knox import views as knox_views
from .views import LoginAPI,get_data
from django.urls import path

urlpatterns = [
    path('api/register/', RegisterAPI.as_view(), name='register'),
    path('api/login/', LoginAPI.as_view(), name='login'),
    path('api/logout/', knox_views.LogoutView.as_view(), name='logout'),
    path('api/logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall'),
    # path('api/get_data/', get_data, name='get_data'),
    path('api/get_data/<int:page_number>/', get_data, name='get_data'),
]