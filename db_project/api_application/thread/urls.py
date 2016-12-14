from django.conf.urls import url
from views.create import create

urlpatterns = [
    url(r'^create/', create, name="create"),
]
