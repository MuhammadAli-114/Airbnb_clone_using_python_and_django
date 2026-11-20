from django.contrib import admin
from .models import (
    PropertyType, Property, Amenity, Booking, Review, PaymentMethod, Payment, Address,
    Wishlist, Transaction, Notification, UserProfile, Report, PropertyImage, Feature, 
    PropertyFeature, RentalHistory, PaymentGateway, PromoCode, PropertyBooking, Message
)
# Registering models using admin.site.register()
admin.site.register(PropertyType)
admin.site.register(Property)
admin.site.register(Amenity)
admin.site.register(Booking)
admin.site.register(Review)
admin.site.register(PaymentMethod)
admin.site.register(Payment)
admin.site.register(Address)
admin.site.register(Wishlist)
admin.site.register(Transaction)
admin.site.register(Notification)
admin.site.register(UserProfile)
admin.site.register(Report)
admin.site.register(PropertyImage)
admin.site.register(Feature)
admin.site.register(PropertyFeature)
admin.site.register(RentalHistory)
admin.site.register(PaymentGateway)
admin.site.register(PromoCode)
admin.site.register(PropertyBooking)
admin.site.register(Message)
