from django.conf.urls import url
from views.create import create
from views.details import details
from views.listUsers import listUsers

urlpatterns = [
    url(r'^create/', create, name="create"),
    url(r'^details/', details, name="details"),
    url(r'^listUsers/', listUsers, name="listUsers"),
]
