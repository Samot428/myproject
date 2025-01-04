from django.urls import path    
from . import views as rv

urlpatterns = [
    path('', rv.register, name='register'),
]