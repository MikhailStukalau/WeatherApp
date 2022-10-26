from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:pk>', views.DetailCity.as_view(), name='detail'),
    path('delete', views.DeleteCity.as_view(), name='delete_city'),
]