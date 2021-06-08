from django.urls import path,include
from . import views
from django.conf import settings
from django.conf.urls.static import static



urlpatterns=[
    path('',views.index,name="index"),
    path('sign/',views.signup,name="reg"),
    path('profile/',views.profile,name="profile"),
    path('auth/',include('registration.backends.simple.urls')),
    path('forgot/',views.forgot_password,name='change'),
    path('change/pass/', views.change_password, name='pass'),
    path('search/', views.search_results, name='search'),
    path('items/<int:pk>/',views.items,name='items'),
    path('category/<slug:keyword>/',views.category_item),
    path('add/<int:pk>/',views.add_to_cart,name='addcart'),
    path('cart/', views.viewcart, name='viewcart'),
    path('orders/',views.viewOrders, name='vieworders'),
    path('chat/<int:pk>/',views.chat,name="chat"),
    path('online/lipa', views.lipa_na_mpesa_online, name='lipa_na_mpesa'),
    path('confirmation/', views.confirmation, name='confirmation'),
    path('remove/cart/<int:pk>/',views.removeItem,name='removeCart'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )