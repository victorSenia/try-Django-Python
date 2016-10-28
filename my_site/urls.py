"""test_site URL Configuration

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
from django.conf.urls import url

from my_site.views import index, user, client, userInfo, clientInfo, userDelete, clientDelete, register, user_login, \
    user_logout

app_name = 'my_site'

urlpatterns = [
    url(r'^$', view=index, name="index"),
    url(r'^user/$', user, name="user"),
    url(r'^user/(?P<id>[0-9]+)/$', view=userInfo, name="userInfo"),
    url(r'^user/(?P<id>[0-9]+)/delete/$', view=userDelete, name="userDelete"),
    url(r'^client/$', view=client, name="client"),
    url(r'^client/(?P<id>[0-9]+)/$', view=clientInfo, name="clientInfo"),
    url(r'^client/(?P<id>[0-9]+)/delete/$', view=clientDelete, name="clientDelete"),
    url(r'^register/$', register, name="register"),
    url(r'^login/$', user_login, name="login"),
    url(r'^logout/$', user_logout, name="logout"),
]
