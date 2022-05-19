from django.urls import path
from .views import PostList, PostDetail, PostCreateView, PostUpdateView, PostDeleteView, PostSearchView, CatSubView

app_name = 'news'
urlpatterns = [
    path('', PostList.as_view()),
    path('add/', PostCreateView.as_view(), name='post_add'),
    path('search/', PostSearchView.as_view(), name='post_search'),
    path('<int:pk>', PostDetail.as_view(), name='post_detail' ),
    path('<int:pk>/edit', PostUpdateView.as_view(), name='post_edit'),
    path('<int:pk>/delete', PostDeleteView.as_view(), name='post_delete'),
    path('subscribe/', CatSubView.as_view()),
]
