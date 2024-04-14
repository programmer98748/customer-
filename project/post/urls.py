from django.urls import path

from .views import * 

app_name = 'post'

urlpatterns = [
    path('', PostList.as_view(), name='blog'),
    #path('blog_single', blog_single, name='blog_single'),
    path('<slug:slug>/', PostDetail.as_view(), name='blog_single'),

]