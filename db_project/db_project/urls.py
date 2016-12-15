"""db_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from api_application.user import urls as user_urls
from api_application.forum import urls as forum_urls
from api_application.thread import urls as thread_urls
from api_application.post import urls as post_urls
urlpatterns = [
    url(r'^db/api/admin/', admin.site.urls),
    url(r'^db/api/user/', include(user_urls)),
    url(r'^db/api/forum/', include(forum_urls)),
    url(r'^db/api/thread/', include(thread_urls)),
    url(r'^db/api/post/', include(post_urls)),
]
