from django.contrib import admin
from django.urls import path
from api import views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Dashboard
    path('', views.loadDashboard, name='home'),
    path('api/resources/', views.resource_api, name='resource_api'),

    # Auth
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),

    # Deployment
    path('deploy/ec2/', views.create_server, name='create_server'),

    # --- ADD THIS MISSING LINE ---
    path('api/terminal/', views.terminal_api, name='terminal_api'),
]

