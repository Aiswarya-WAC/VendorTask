from django.urls import path
from .views import RegisterVendor, RegisterCustomer, Login, RegisteredUsersView

urlpatterns = [
    path('register/vendor/', RegisterVendor.as_view(), name='register_vendor'),
    path('register/customer/', RegisterCustomer.as_view(), name='register_customer'),
    path('login/', Login.as_view(), name='login'),
    path('viewuser/',RegisteredUsersView.as_view(), name='registered_users_view'),
]
