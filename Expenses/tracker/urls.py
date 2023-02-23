from django.urls import path,include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers
from .views import ExpensesViewSet
router= routers.DefaultRouter()
router.register(r'expenses',ExpensesViewSet)
urlpatterns = [
    
    path('',views.home,name='home'),
    path('login',views.Login,name='login'),
    path('logout',views.Logout,name='logout'),
    path('transcation',views.Transcation,name='transcation'),
    path('money_in',views.money_in,name='money_in'),
    path('register_income',views.register_income,name='register_income'),
    path('register',views.register,name='register'),
   
    path('api', include(router.urls)),
    path('expense_category_summary',views.expense_category_summary,name="expense_category_summary"),
    path('transaction_table',views.Transcation_Table,name='transcation_table'),
    path('stats',views.stats_view,name='stats'),
    path("delete_transcation",views.delete_transcation,name="delete_transcation")
]+static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)