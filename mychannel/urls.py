from django.conf.urls import url
from .import views
from django.conf import settings

urlpatterns = [
    url(r'^$', views.homepage, name='homepage'),
    url(r'^user_check/$', views.user_check),
    url(r'^logout/$', views.userlogout),
    url(r'^dashboard/$', views.dashboard, name='dashboard'),
    url(r'^dashboard/msg_sent/$', views.msg_sent, name='msg_sent'),
    url(r'^dashboard/msg_get/$', views.msg_get, name='msg_get'),
    url(r'^chatter/(?P<user_id>[0-9]+)/$', views.chatter, name='chatter'),
    url(r'^dashboard/fetch_user/$', views.fetch_user, name='fetch_user'),
]