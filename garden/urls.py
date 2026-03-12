from django.urls import path
from . import views

urlpatterns = [
    path('', views.about_veggieguard, name='home'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),

    # Scan — core feature
    path('scan/', views.scan_vegetable, name='scan_vegetable'),
    path('scan/<int:pk>/', views.scan_result, name='scan_result'),
    path('scan/history/', views.scan_history, name='scan_history'),

    # Vegetables
    path('add/', views.add_vegetable, name='add_vegetable'),
    path('vegetable/<int:pk>/', views.vegetable_detail, name='vegetable_detail'),

    # Waste & analytics
    path('waste/', views.waste_log, name='waste_log'),
    path('analytics/', views.analytics, name='analytics'),
    path('monitor/', views.monitor, name='monitor'),

    # AJAX
    path('api/tips/', views.get_tips_ajax, name='get_tips'),

    # About
    path('about/', views.about_veggieguard, name='about_veggieguard'),
]