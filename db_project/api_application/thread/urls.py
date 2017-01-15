from django.conf.urls import url
from views.create import create
from views.subscribe import subscribe
from views.details import details
from views.close import close
from views.open import open
from views.remove import remove
from views.restore import restore
from views.vote import vote


urlpatterns = [
    url(r'^create/', create, name="create"),
    url(r'^subscribe/', subscribe, name="subscribe"),
    url(r'^details/', details, name="details"),
    url(r'^close/', close, name="close"),
    url(r'^open/', open, name="open"),
    url(r'^remove/', remove, name="remove"),
    url(r'^restore/', restore, name="restore"),
    url(r'^vote/', vote, name="vote"),
]

