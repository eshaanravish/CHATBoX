from django.conf.urls import url
from .import views
from django.conf import settings
from django.views.static import serve

urlpatterns = [
    url(r'^$', views.homepage, name='homepage'),
    url(r'^user_check/$', views.user_check),
    url(r'^logout/$', views.userlogout),
    url(r'^dashboard/(?P<user_id>[0-9]+)/$', views.dashboard, name='dashboard'),
    url(r'^dashboard/global/$', views.dashboard_global, name='dashboard_global'),
    url(r'^dashboard/msg_sent/$', views.msg_sent, name='msg_sent'),
    url(r'^dashboard/load_messages/$', views.load_messages, name='load_messages'),
    url(r'^dashboard/fetch_user/$', views.fetch_user, name='fetch_user'),

    # url(r'^password_reset/$', password_reset, name= 'reset_password'),
    # url(r'^password_reset/done/$', password_reset_done, name= 'password_reset_done'),
    # url(r'^accounts/password/reset/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', password_reset_confirm, name= 'password_reset_confirm'),
    # url(r'^password/complete/$', password_reset_complete, name = 'password_reset_complete'),

    url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT, }),
]