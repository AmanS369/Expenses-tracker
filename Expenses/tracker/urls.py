from django.urls import path,include
from . import views
urlpatterns = [
    
    path('',views.home,name='home'),
    path('login',views.Login,name='login'),
    path('logout',views.Logout,name='logout'),
    path('transcation',views.Transcation,name='transcation'),
    path('register_income',views.register_income,name='register_income'),
    path('register',views.register,name='register'),
]