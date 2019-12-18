from django.urls import path

from . import views

urlpatterns = [
    #path('', views.index, name='index'),
    #path('temp_plot/', views.temp_plot, name='temp_plot'),
    path('', views.IndexTempSensorListView.as_view(), name='index'),
    path('temp_plot/', views.temp_plot, name='temp_plot'),
]
