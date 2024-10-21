from django.urls import path

from .views import get_grievances, grievance_details, login_user, post_grievance, signup_user

urlpatterns = [
    path('signup/', signup_user, name='signup_user'),
    path('login/', login_user, name='login_user'),

    # Grievance URLs
    path('grievances/', get_grievances, name='get_grievances'),
    path('grievances/create/', post_grievance, name='post_grievance'),
    path('grievances/<int:pk>/', grievance_details, name='grievance_details'),
]