from django.conf.urls import url
from views.create import create
from views.details import details
from views.list import list
from views.remove import remove

urlpatterns = [
    url(r'^create/', create, name="create"),
    url(r'^details/', details, name="details"),
    url(r'^list/', list, name="list"),
    url(r'^remove/', remove, name="remove"),
]
