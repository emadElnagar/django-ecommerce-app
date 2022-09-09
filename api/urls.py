from django.urls import path
from . import views

app_name ='api'

urlpatterns = [
    # CATEGORY API
    path('category/all', views.GetAllCategories),
    path('category/new', views.NewCategory),
    path('category/<str:slug>', views.SingleCategory),
    # PRODUCTS API
    path('products/all', views.ProductsList),
    path('products/new', views.NewProduct),
    path('products/<str:slug>', views.SingleProduct),
    # REVIEWS API
    path('reviews/update/<int:pk>', views.UpdateReview),
    path('reviews/delete/<int:pk>', views.DeleteReview),
    # SEARCH API
    path('Search', views.Search),
    # AUTH API
    path('users/changepassword', views.ChangePasswordView.as_view()),
    path('users/profile/<int:pk>', views.UserProfile.as_view()),
    path('users/user/delete', views.DeleteUser),
    path('users/user/<int:pk>', views.UserView.as_view()),
    path('users/signup', views.SignUp),
    # ORDER API
    path('checkout/order', views.OrderView.as_view()),
]
