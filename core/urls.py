from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.bonds_list, name='bonds_list'),
    path('search', views.bonds_search, name='bonds_search'),
    path('login', views.user_login, name='login'),
    path('logout', views.user_logout, name='logout'),
    path('loader', views.data_loader, name='loader'),
    path('<str:isin>', views.bonds_detail, name='bonds_detail'),
]
