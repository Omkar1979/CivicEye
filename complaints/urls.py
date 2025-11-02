from django.urls import path
from . import views, auth_views

app_name = 'complaints'

urlpatterns = [
    path('', views.community_feed, name='home'),
    path('report/', views.report_view, name='report'),
    path('complaint/<int:id>/', views.detail_view, name='detail'),
    path('like/<int:complaint_id>/', views.like_post, name='like_post'),
    path('comment/<int:complaint_id>/', views.add_comment, name='add_comment'),
     path('my_complaints/', views.my_complaints, name='my_complaints'),
   

    # Admin URLs
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    # Authentication URLs
    path('register/', auth_views.register_view, name='register'),
    path('login/', auth_views.login_view, name='login'),
    path('logout/', auth_views.logout_view, name='logout'),

    
     path('delete/<int:complaint_id>/', views.delete_complaint, name='delete_complaint'),
]
