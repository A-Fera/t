from django.urls import path
from . import views

app_name = 'destinations'

urlpatterns = [
    path('', views.DestinationListView.as_view(), name='destination_list'),
    path('<int:pk>/', views.destination_detail_view, name='destination_detail'),
    path('create/', views.destination_create_view, name='destination_create'),
    path('<int:pk>/edit/', views.destination_update_view, name='destination_update'),
    path('<int:pk>/delete/', views.destination_delete_view, name='destination_delete'),
    path('<int:destination_pk>/upload-photo/', views.photo_upload_view, name='photo_upload'),
]
