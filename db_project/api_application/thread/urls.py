from django.conf.urls import url
from views.create import create
from views.subscribe import subscribe
from views.details import details
urlpatterns = [
    url(r'^create/', create, name="create"),
    url(r'^subscribe/', subscribe, name="subscribe"),
    url(r'^details/', details, name="details"),
]
