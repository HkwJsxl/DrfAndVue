from django.urls import path
from serializer_related import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index_view'),


]
