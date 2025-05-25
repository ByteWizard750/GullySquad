from django.urls import path
from . import views

urlpatterns = [
    path('messages/<int:match_id>/', views.MessageListView.as_view(), name='message-list'),
] 