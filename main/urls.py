from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView
from .views import property_search

urlpatterns = [
    path('', views.home, name='home'),  # Ensure this exists and is correct
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
     # Property URLs
    path('property/create/', views.property_create_view, name='property_create'),  # Create property
    path('property/<int:property_id>/', views.property_detail_view, name='property_detail'),  # View property details

    # Booking URLs
    path('property/<int:property_id>/booking/', views.booking_view, name='booking'),  # Create booking for a property
    path('booking/<int:booking_id>/', views.booking_detail_view, name='booking_detail'),  # View booking details
    path("bookings/", views.bookings_list, name="bookings_list"),

    # Review URLs
    path('property/<int:property_id>/review/', views.review_create_view, name='review_create'),  # Submit a review for property

    # Payment Method URL
    path('payment-method/', views.payment_method_view, name='payment_method'),  # Add or manage payment methods

    # Address URLs
    path('address/create/', views.address_create_view, name='address_create'),  # Create a new address for user

    # User Profile URL
    path('profile/', views.user_profile_view, name='profile'),  # User profile page

    # Promo Code URL
    path('promo-code/', views.apply_promo_code, name='apply_promo_code'),  # Apply promo code to booking

    # Contact Form URL
    path("about-us/", views.about_us, name="about_us"),
    path("contact-us/", views.contact_us, name="contact_us"),

      path('search/', property_search, name='property_search'),
    
]
