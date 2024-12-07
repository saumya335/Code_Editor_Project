from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('codeEditor/', views.codeEditor, name='codeEditor'),
    path('collaborate/', views.collaborate_view, name='collaborate'),
    path('login_success/', views.login_success_view, name='login_success'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('logout/', views.logout, name='logout'),
    path('my_projects/', views.my_projects, name='my_projects'),
    path('password_change/', views.password_change, name='password_change'),
    path('code-editor-api/', views.code_editor_api, name='code_editor_api'),
    path('fetch_online_users/', views.fetch_online_users, name='fetch_online_users'),
path('fetch_users_by_status/', views.fetch_users_by_status, name='fetch_users_by_status'),
]
