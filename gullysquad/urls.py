from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('matches/', views.matches_list, name='matches-list'),
    path('squads/', views.squads_list, name='squads-list'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('admin/', admin.site.urls),
    path('api/users/', include('users.urls')),
    path('api/matches/', include('matches.urls')),
    path('api/squads/', include('squads.urls')),
    path('api/chat/', include('chat.urls')),
    path('matches/create/', views.match_create, name='match-create'),
    path('squads/create/', views.squad_create, name='squad-create'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 