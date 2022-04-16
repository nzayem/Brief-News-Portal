from django.urls import path
from . import views


urlpatterns = [
    path('news/create/', views.create_post, name='create_page'),
    path('news/<int:news_id>/', views.post_view, name='news_page'),
    path('news/', views.news_home, name='news'),
    path('', views.index, name='index')
]
