from unicodedata import name
from django.urls import path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('', views.index, name='home'),
    path('signup', views.signup, name='signup'),
    path('signin', views.signin, name='signin'),
    path('logout', views.logout_view, name='logout'),
    path('tech',views.tech,name="tech"),
    path('sports',views.sports, name="sports"),
    path('entertainment',views.entertainment,name="entertainment")
]
urlpatterns += staticfiles_urlpatterns()