from django.conf.urls import url
from views.create import create
from views.details import details

urlpatterns = [
    url(r'^create/', create, name="create"),
    url(r'^details/', details, name="details"),

]
