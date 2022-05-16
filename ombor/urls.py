from xml.etree.ElementInclude import include
from django.contrib import admin
from django.urls import path, include
from main.views import *


urlpatterns = [
    path('admin/', admin.site.urls),
    path('client/', ClientView.as_view()),
    path('client/<int:pk>/', ClientDetail.as_view())
    
]
