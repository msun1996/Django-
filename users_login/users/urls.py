from django.conf.urls import url

from .views import RegisterEmailView,EmailActiveView,LoginView,LogoutView

urlpatterns = [
    url(r'^register_mail/$', RegisterEmailView.as_view(), name='register_mail'),
    url(r'active/(?P<active_code>.*)/$', EmailActiveView.as_view(), name='mail_active'),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'logout/$', LogoutView.as_view(), name='logout'),
]