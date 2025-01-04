from django.urls import path
from . import views

urlpatterns = [
    path('HomePage/', views.HomePage, name='HomePage'),
    path('ToDoList/', views.list_view, name='tdl'),
    path('<int:id>/', views.items_view, name="TDLItem")
]