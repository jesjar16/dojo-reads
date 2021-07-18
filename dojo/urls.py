from dojo import views_ajax
from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name="my_index"),
    path('success/', views.success, name="my_success"),
    path('register/', views.register, name="my_register"),
    path('login/', views.login, name="my_login"),
    path('homepage/', views.homepage, name="my_homepage"),
    path('book_review/', views.book_review, name="my_book_review"),
    path('add_breview/', views.add_breview, name="my_add_breview"),
    path('del_breview/', views.del_breview, name="my_del_breview"),
    path('add_sm_review/', views.add_sm_review, name="my_add_sm_review"),
    path('add/', views.add, name="my_add"),
    path('users/<int:user_id>/', views.users, name="my_users"),
    path('book/<int:book_id>/', views.book, name="my_book"),
    path('about/', views.about, name="my_about"),
    path('logout/', views.logout, name="my_logout"),
]