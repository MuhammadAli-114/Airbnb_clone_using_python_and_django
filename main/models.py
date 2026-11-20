from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class PropertyType(models.Model):
    """Define property types like rooms, houses, etc."""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Property(models.Model):
    """Model for properties available for booking."""
    name = models.CharField(max_length=200)
    property_type = models.ManyToManyField(PropertyType, related_name="property")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="properties")
    description = models.TextField()
    location = models.CharField(max_length=255)
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    max_guests = models.IntegerField()
    availability_start = models.DateField()
    availability_end = models.DateField()
    image = models.ImageField(upload_to="property_images/", blank=True, null=True)
    amenities = models.ManyToManyField('Amenity', related_name="properties")

    def __str__(self):
        return f"{self.name} ({self.property_type.name}) - {self.location}"

class Amenity(models.Model):
    """Define amenities that properties can have (e.g., WiFi, Pool)."""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Booking(models.Model):
    """Model for user bookings."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bookings")
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="bookings")
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    guests = models.IntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('confirmed', 'Confirmed'), ('cancelled', 'Cancelled')])

    def save(self, *args, **kwargs):
        # Calculate total price before saving
        days = (self.check_out_date - self.check_in_date).days
        self.total_price = self.property.price_per_night * days
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Booking: {self.property.name} by {self.user.username}"

class Review(models.Model):
    """Model for user reviews of properties."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="reviews")
    rating = models.PositiveSmallIntegerField()  # e.g., 1 to 5
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user.username} for {self.property.name} - {self.rating} stars"

class PaymentMethod(models.Model):
    """Define payment methods for users."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="payment_methods")
    method_type = models.CharField(max_length=50, choices=[('credit_card', 'Credit Card'), ('paypal', 'PayPal')])
    details = models.TextField()

    def __str__(self):
        return f"{self.method_type} - {self.user.username}"

class Payment(models.Model):
    """Model for payments made by users for bookings."""
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name="payments")
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.CASCADE, related_name="payments")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[('completed', 'Completed'), ('pending', 'Pending'), ('failed', 'Failed')])

    def __str__(self):
        return f"Payment for {self.booking.property.name} - {self.amount} by {self.booking.user.username}"

class Address(models.Model):
    """Model for addresses related to users or properties."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="addresses", null=True, blank=True)
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="addresses", null=True, blank=True)
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.street}, {self.city}, {self.country}"

class Wishlist(models.Model):
    """Model for user wishlists of properties."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="wishlists")
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="wishlists")

    def __str__(self):
        return f"{self.user.username}'s wishlist - {self.property.name}"

class Transaction(models.Model):
    """Model for transaction logs."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="transactions")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=50, choices=[('debit', 'Debit'), ('credit', 'Credit')])
    description = models.TextField()
    transaction_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.transaction_type} of {self.amount} by {self.user.username}"

class Notification(models.Model):
    """Model for user notifications."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
    message = models.TextField()
    read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user.username}"

class UserProfile(models.Model):
    """Model for storing additional user details."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    profile_picture = models.ImageField(upload_to="profile_pics/", blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"Profile of {self.user.username}"

class Report(models.Model):
    """Model for reporting issues or disputes related to bookings or properties."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reports")
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="reports", null=True, blank=True)
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name="reports", null=True, blank=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[('open', 'Open'), ('resolved', 'Resolved'), ('closed', 'Closed')])

    def __str__(self):
        return f"Report by {self.user.username} on {self.created_at}"

class PropertyImage(models.Model):
    """Model for images related to properties."""
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="property_images/")

    def __str__(self):
        return f"Image for {self.property.name}"

class Feature(models.Model):
    """Define features that can be associated with properties (e.g., pet-friendly)."""
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class PropertyFeature(models.Model):
    """Associates properties with features."""
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="features")
    feature = models.ForeignKey(Feature, on_delete=models.CASCADE, related_name="properties")

    def __str__(self):
        return f"{self.property.name} - {self.feature.name}"

class RentalHistory(models.Model):
    """Track the rental history of properties."""
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="rental_history")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="rental_history")
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"Rental by {self.user.username} from {self.start_date} to {self.end_date}"

class PaymentGateway(models.Model):
    """Define payment gateways (e.g., Stripe, PayPal)."""
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

class PromoCode(models.Model):
    """Define promo codes for discounts."""
    code = models.CharField(max_length=20, unique=True)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    expiration_date = models.DateField()

    def __str__(self):
        return self.code

class PropertyBooking(models.Model):
    """Tracks property booking details."""
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="property_bookings")
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name="property_bookings")

    def __str__(self):
        return f"Booking for {self.property.name} - {self.booking.user.username}"

class Message(models.Model):
    """Model for communication between users (e.g., messages between guests and hosts)."""
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_messages")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_messages")
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.sender.username} to {self.receiver.username}"
