from django.urls import path
from rango import views

app_name = 'rango'

urlpatterns = [
    path('', views.index, name='index'),
    #creates a path to the view about
    path('about/', views.about, name='about'),
    #path to any category according to its slug
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('buying/<slug:name>', views.buying, name='buying'),
    path('enquire/', views.enquire, name='enquire'),
    path('sellers/', views.sellers, name='sellers'),
    path('show_seller/<slug:username>/',
        views.show_seller, name='show_seller'),
    path('add_car/<slug:username>/', views.add_car, name='add_car'),
    
]