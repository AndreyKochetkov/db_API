from django.conf.urls import url
from views.create import create
from views.details import details
#from views.follow import follow
#from views.listFollowers import listFollowers
#from views.listFollowing import listFollowing
#from views.listPosts import listPosts
#from views.unfollow import unfollow
#from views.updateProfile import updateProfile

urlpatterns = [
    url(r'^create/', create, name="create"),
    url(r'^details/', details, name="details"),
   # url(r'^follow/', follow),
   # url(r'^listFollowers/', listFollowers),
   # url(r'^listFollowing/', listFollowing),
   # url(r'^listPosts/', listPosts),
   # url(r'^unfollow/', unfollow),
   # url(r'^updateProfile/', updateProfile),
]
