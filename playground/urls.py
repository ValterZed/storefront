from . import views
from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import include, path
from django.views.generic.base import RedirectView
from django.conf import settings

#URLConf
urlpatterns = [
    path("", views.render_home),
    path("loggingIn/", views.logged_in),
    path("gen/", views.generate)
]