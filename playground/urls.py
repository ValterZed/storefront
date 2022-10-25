from django.urls import path
from . import views

#URLConf
urlpatterns = [
    path("", views.render_home),
    path("loggingIn/", views.logged_in)
]