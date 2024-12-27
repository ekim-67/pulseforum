from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='blog-home'),
    path('home/<int:pk>/', views.clubHome, name='club-home'),
    path('member-list', views.MemberListView.as_view(), name='member-list'),
    path('create-club/', views.create_club, name='create-club'),
    path('club-list/', views.club_list, name='club-list'),
    path('home/<int:pk>/update', views.ClubUpdateView.as_view(), name="club-update"),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post-detail'),
    path('post/new/<int:club_id>/', views.PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update', views.PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete', views.PostDeleteView.as_view(), name='post-delete'),
    path('comment-delete/<int:pk>', views.comment_delete, name='comment-delete'),
    path('about/', views.about, name='blog-about'),
]
