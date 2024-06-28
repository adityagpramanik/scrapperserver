from django.urls import path
from . import views

app_name = 'extracter'

urlpatterns = [
    path('github', views.github, name='github'),
]
