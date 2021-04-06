from django.urls import path
from rango import views

app_name = 'rango'

urlpatterns = [
    #views to main pages
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('enquire/', views.enquire, name='enquire'),
    path('sellers/', views.sellers, name='sellers'),
    path('search/', views.search, name='search'),
    #path to any seller/car according to its slug
    path('show_seller/<slug:username>/',
        views.show_seller, name='show_seller'),
    path('add_car/<slug:username>/', views.add_car, name='add_car'),
    path('buying/<slug:name>', views.buying, name='buying'),
]