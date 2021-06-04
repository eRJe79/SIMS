from django.urls import path

from .views import (
    create_article,
    create_item,
    create_mainuser,
    create_lambdauser,
    ArticleListView,
    ItemListView,
    MainUserListView,
    LambdaUserListView,
)

urlpatterns = [
    path('create-article/', create_article, name='create-article'),
    path('create-item/', create_item, name='create-item'),
    path('create-mainuser/', create_mainuser, name='create-mainuser'),
    path('create-lambdauser/', create_lambdauser, name='create-lambdauser'),

    path('article-list/', ArticleListView.as_view(), name='article-list'),
    path('item-list/', ItemListView.as_view(), name='item-list'),
    path('mainuser-list/', MainUserListView.as_view(), name='mainuser-list'),
    path('lambdauser-list/', LambdaUserListView.as_view(), name='lambdauser-list'),
]