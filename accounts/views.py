from django.shortcuts import render

# Create your views here.
from rest_framework import generics, permissions
from rest_framework.response import Response
from knox.models import AuthToken
from .serailizers import UserSerializer, RegisterSerializer

from django.contrib.auth import login

from rest_framework import permissions
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.core.cache import cache
from rest_framework.permissions import IsAuthenticated
import requests

from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

# DICTIONARY FOR CITY NAME WITH LAT & LNG
city_dic={'Delhi': [28.66, 77.23],
 'Mumbai': [18.9667, 72.8333],
 'Kolkāta': [22.5411, 88.3378],
 'Bangalore': [12.9699, 77.598],
 'Chennai': [13.0825, 80.275],
 'Hyderābād': [17.3667, 78.4667],
 'Pune': [18.5196, 73.8553],
 'Ahmedabad': [23.03, 72.58],
 'Sūrat': [21.17, 72.83],
 'Lucknow': [26.847, 80.947],
 'Jaipur': [26.9167, 75.8667],
 'Cawnpore': [26.4725, 80.3311],
 'Mirzāpur': [25.15, 82.58],
 'Nāgpur': [21.1539, 79.0831],
 'Ghāziābād': [28.6667, 77.4167],
 'Indore': [22.7206, 75.8472],
 'Vadodara': [22.3, 73.2],
 'Vishākhapatnam': [17.7333, 83.3167],
 'Bhopāl': [23.25, 77.4167],
 'Chinchvad': [18.6278, 73.8131],
 'Patna': [25.61, 85.1414],
 'Ludhiāna': [30.9083, 75.8486],
 'Āgra': [27.18, 78.02],
 'Kalyān': [19.2502, 73.1602],
 'Madurai': [9.9197, 78.1194],
 'Jamshedpur': [22.8, 86.1833],
 'Nāsik': [20.0, 73.7833],
 'Farīdābād': [28.4333, 77.3167],
 'Aurangābād': [19.88, 75.32],
 'Rājkot': [22.2969, 70.7984],
 'Meerut': [28.99, 77.7],
 'Jabalpur': [23.1667, 79.9333],
 'Thāne': [19.18, 72.9633],
 'Dhanbād': [23.7928, 86.435],
 'Allahābād': [25.455, 81.84],
 'Vārānasi': [25.3189, 83.0128],
 'Srīnagar': [34.0911, 74.8061],
 'Amritsar': [31.6167, 74.85],
 'Alīgarh': [27.88, 78.08],
 'Bhiwandi': [19.3, 73.0667]}

# Register API
class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
        "user": UserSerializer(user, context=self.get_serializer_context()).data,
        "token": AuthToken.objects.create(user)[1]
        })



#Login API
class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginAPI, self).post(request, format=None)



#GET WEATHER DATA API
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_data(request,page_number):
    # return Response({"status":"authenticated"})
        # Try to get the data from the cache
    data = cache.get('weather_data')

    # If the data is not in the cache, call the third-party API and store the data in the cache
    if data is None:
        data = json_res()
        cache.set('weather_data', data, 1800) #1800 sec = 30 minutes 

    # Create a paginator object with a 10 item limit per page
    paginator = Paginator(data, 10)

    # Get the data for the current page
    page_data = paginator.get_page(page_number)

    # Return the paginated data as a JSON response
    return JsonResponse({'data': list(page_data)})


def json_res():
    res=[]
    for i in city_dic.keys():
        loc=city_dic[i]
        json_res="https://api.openweathermap.org/data/2.5/weather?lat="+str(loc[0])+"&lon="+str(loc[1])+"&appid=f4dd17518510eb75383bacfd52f08b44"
        response = requests.get(json_res)
        data = response.json()
        res.append(data)
    return res






