from django.apps import AppConfig
from django.urls import path
from . import views


class SummarizerConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "summarizer"


urlpatterns = [

    path("templates", views.index, name="index"),

]