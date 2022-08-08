from django.contrib import admin
from django.urls import path,include 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('base.urls')), #base uygulamasının urllerini aldık
    path('api/',include('base.api.urls'))
]
