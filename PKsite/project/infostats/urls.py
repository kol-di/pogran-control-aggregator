from django.urls import path

from . import views

app_name = 'infostats'

urlpatterns = [
    path('', views.index, name='index'),
    path('info_timeline/', views.info_timeline, name='timeline'),
    path('info_piechart/', views.info_piechart, name='piechart'),
    path('info_dynamics/', views.info_dynamics, name='dynamics'),
    path('stories/', views.stories, name='stories')
]
