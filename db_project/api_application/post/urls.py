from django.conf.urls import url
from views.create import create
from views.details import details
from views.list import list
from views.remove import remove
from views.restore import restore
from views.update import update

urlpatterns = [
    url(r'^create/', create, name="create"),
    url(r'^details/', details, name="details"),
    url(r'^list/', list, name="list"),
    url(r'^remove/', remove, name="remove"),
    url(r'^restore/', restore, name="restore"),
    url(r'^update/', update, name="update"),
]
