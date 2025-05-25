from django.urls import path
from . import views

urlpatterns = [
    path('', views.SquadListView.as_view(), name='squad-list'),
    path('create/', views.SquadCreateView.as_view(), name='squad-create'),
    path('<int:pk>/', views.SquadDetailView.as_view(), name='squad-detail'),
    path('<int:pk>/join/', views.JoinSquadView.as_view(), name='join-squad'),
] 