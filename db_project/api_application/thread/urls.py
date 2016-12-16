from django.conf.urls import url
from views.create import create
from views.subscribe import subscribe
urlpatterns = [
    url(r'^create/', create, name="create"),
    url(r'^subscribe/', subscribe, name="subscribe"),
]
