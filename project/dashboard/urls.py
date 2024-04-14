from django.urls import path, re_path
from . import views
from .views import (
    PageDeleteView,
    PageCreateView,
    AccountCreateView,
    AccountUpdateView,
    AccountDeleteView,
    PostListView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    PostLanguageListView,
    PostLanguageCreateView,
    PostLanguageUpdateView,
    PostLanguageDeleteView,

    CommentListView
)

from django.contrib.auth.views import LogoutView

from django.contrib.auth import views as auth_views


app_name = 'dashboard'

urlpatterns = [
    path('', views.index, name='home'),
    path('informaion_site/', views.edite_informaion, name='informaion_site'),
    path('profile/', views.profile, name='profile'),
    path("logout/", views.auth_logout, name="logout"),
###
    path('gallery/', views.gallery, name='gallery'),
    path('gallery/delete', views.delete, name='delete'),

###
    path('service/', views.services, name='services'),
    path('service/edite/<int:id>/', views.services_edite, name='services_edite'),
    path('service/delete/<int:id>/', views.services_delete, name='services_delete'),
    path('service/create/', views.services_add, name='services_add'),


##
    path('page/', views.page, name='page'),
    path('page/about', views.page_about, name='page_about'),

    path('page/create/', PageCreateView.as_view(), name='page_add'),
    path('page/edite/<int:id>/', views.page_edite, name='page_edite'),
 #   path('page/delete/<int:id>/', views.page_delete, name='page_delete'),
    path('page/delete/<int:pk>/', PageDeleteView.as_view(), name='page_delete'),

##
    path('aluser/<int:pk>', views.AEditUser.as_view(), name='user_edite'),
    path('aluser/', views.user_show, name='accounts'),
   # path('create_use/', views.create_user, name='create_user_form'),
   
    path('account/create/', AccountCreateView.as_view(), name='accounts_create'),
    path('account/update/<int:pk>/', AccountUpdateView.as_view(), name='accounts_update'),
    path('account/delete/<int:pk>/', AccountDeleteView.as_view(), name='accounts_delete'),
    
    path('alvuser/<int:pk>', views.ALViewUser.as_view(), name='alvuser'),
   # path('aeuser/<int:pk>', views.AEditUser.as_view(), name='aeuser'),
   # path('aduser/<int:pk>', views.ADeleteUser.as_view(), name='aduser'),



    #### posts
    path('posts/', PostListView.as_view(), name='posts'),
    path('post/create/', PostCreateView.as_view(), name='post_create'),
  # path('post/update/<slug:slug>/', PostUpdateView.as_view(), name='post_update'),
    #path('post/delete/<slug:slug>/', PostDeleteView.as_view(), name='post_delete'),

    path('post/update/<int:id>/', views.post_update, name='post_update'),
    path('post/delete/<int:id>/', views.post_delete, name='post_delete'),

    path('posts/translation/', PostLanguageListView.as_view(), name='posts_language'),
    path('post/add/translation/<int:id>/', PostLanguageCreateView.as_view(), name='post_language_create'),
    path('post/update/translation/<int:pk>/', views.post_language_update, name='post_language_update'),
    path('post/delete/translation/<int:pk>/', views.post_language_delete, name='post_language_delete'),

        # Comments Urls
    path('comment/', CommentListView.as_view(), name='comments'),
    path('comments/delete/<int:id>/', views.comment_delete, name='comment_delete'),



###  brands
    path('brands/', views.brands, name='brands'),
    path('brands/delete/<int:id>/', views.brands_delete, name='brands_delete'),
    path('brands/create/', views.brands_add, name='brands_add'),

    
]