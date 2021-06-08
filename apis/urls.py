from django.urls import path,include
from . import views
from django.conf import settings
from django.conf.urls.static import static



urlpatterns=[
    path(r'api/getItems/',views.ItemList.as_view()),
    path(r'api/getProfiles/',views.profileList.as_view()),
    path(r'api/getUsers/',views.userList.as_view()),
]
