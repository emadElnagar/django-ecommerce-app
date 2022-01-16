from django.urls import path
from . import views

app_name ='accounts'

urlpatterns = [
    path('profile/<int:pk>', views.UserProfile.as_view(), name='profile'),
    path('profile/update/<int:pk>', views.UpdateProfile.as_view(), name='update_profile'),
    path('profile/delete/<int:pk>', views.delete_user, name='delete_user'),
    path('signup', views.signup, name='signup'),
]
