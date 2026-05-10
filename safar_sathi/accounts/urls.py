from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('guides/', views.GuideListView.as_view(), name='guide_list'),
    path('guides/<int:pk>/', views.guide_detail_view, name='guide_detail'),
    path('guides/create/', views.guide_create_view, name='guide_create'),
    path('guides/<int:pk>/edit/', views.guide_update_view, name='guide_update'),
    path('guides/<int:pk>/delete/', views.guide_delete_view, name='guide_delete'),
]
