from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.forms import UserCreationForm
from .forms import LoginForm, SignUpForm, PropertyForm, BookingForm, ReviewForm, PaymentMethodForm, AddressForm, UserProfileForm, PromoCodeForm, ContactForm
from .models import Property, Booking, Review, PaymentMethod, Address, UserProfile, PromoCode
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import datetime
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.db.models import Q
from django.core.paginator import Paginator


def home(request):
    property = Property.objects.all()
    return render(request, 'main/home.html',{'property':property})  # Use 'main/home.html' since it's inside 'main' folder

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Invalid login credentials.')
    else:
        form = LoginForm()
    
    # Corrected the template path to 'main/login.html'
    return render(request, 'main/login.html', {'form': form})

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create_user(username=email, email=email, password=password)
            user.first_name = name
            user.save()
            messages.success(request, 'Sign up successful! Please log in.')
            return redirect('login')
    else:
        form = SignUpForm()

    # Corrected the template path to 'main/signup.html'
    return render(request, 'main/signup.html', {'form': form})

def logout_view(request):
    logout(request)  # Logs out the user
    return redirect('login')

# Property Creation View (Admin or Owner)
@login_required
def property_create_view(request):
    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES)
        if form.is_valid():
            property = form.save(commit=False)
            property.owner = request.user  # Set the owner to the current logged-in user
            property.save()
            return redirect('home')  # Redirect to a property listing page or success page
    else:
        form = PropertyForm()
    
    return render(request, 'main/property_create.html', {'form': form})

# Property Detail View
def property_detail_view(request, property_id):
    property_instance = Property.objects.get(id=property_id)
    return render(request, 'main/property_detail.html', {'property': property_instance})

# Booking View (For a Property)
def booking_view(request, property_id):
    property_instance = get_object_or_404(Property, id=property_id)
    if request.method == 'POST':
        form = BookingForm(request.POST, property=property_instance)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.property = property_instance
            booking.user = request.user
            booking.save()
            return redirect('payment_method')
            # Redirect or return success response
    else:
        form = BookingForm(property=property_instance)

    return render(request, 'main/booking.html', {'form': form, 'property': property_instance})

# Booking Detail View
def booking_detail_view(request, booking_id):
    booking_instance = Booking.objects.get(id=booking_id)
    return render(request, 'main/booking_detail.html', {'booking': booking_instance})

@staff_member_required
def bookings_list(request):
    # Fetch all bookings
    bookings = Booking.objects.all()

    if request.method == "POST":
        # Handle booking deletion
        booking_id = request.POST.get("booking_id")
        booking = get_object_or_404(Booking, id=booking_id)
        booking.delete()
        return redirect("bookings_list")

    return render(request, "main/bookings_list.html", {"bookings": bookings})

# Review Form View
@login_required
def review_create_view(request, property_id):
    property_instance = Property.objects.get(id=property_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.property = property_instance
            review.user = request.user
            review.save()
            messages.success(request, "Review submitted successfully!")
            return redirect('property_detail', property_id=property_instance.id)
    else:
        form = ReviewForm()
    return render(request, 'main/review_form.html', {'form': form, 'property': property_instance})

# Payment Method View
@login_required
def payment_method_view(request):
    if request.method == 'POST':
        form = PaymentMethodForm(request.POST)
        if form.is_valid():
            payment_method = form.save(commit=False)
            payment_method.user = request.user
            payment_method.save()
            messages.success(request, "Payment method added successfully!")
            return redirect('home')  # Or redirect to a page where payment methods are listed
    else:
        form = PaymentMethodForm()
    return render(request, 'main/payment_method.html', {'form': form})

# Address View (User Address)
@login_required
def address_create_view(request):
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()
            messages.success(request, "Address added successfully!")
            return redirect('profile')  # Or redirect to the user's address list
    else:
        form = AddressForm()
    return render(request, 'main/address_form.html', {'form': form})

# User Profile Update View
@login_required
def user_profile_view(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('profile')
    else:
        form = UserProfileForm(instance=user_profile)
    return render(request, 'main/user_profile_form.html', {'form': form})

# Promo Code View
@login_required
def apply_promo_code(request):
    if request.method == 'POST':
        form = PromoCodeForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data.get('code')
            try:
                promo_code = PromoCode.objects.get(code=code)
                if promo_code.expiration_date < datetime.date.today():
                    form.add_error('code', 'This promo code has expired.')
                else:
                    # Apply the discount logic here
                    messages.success(request, f"Promo code {code} applied successfully!")
                    return redirect('booking_summary')
            except PromoCode.DoesNotExist:
                form.add_error('code', 'Invalid promo code.')
    else:
        form = PromoCodeForm()
    return render(request, 'promo_code_form.html', {'form': form})

# Contact Form View
def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.send_email()  # Implement email sending logic
            messages.success(request, "Your message has been sent!")
            return redirect('contact')
    else:
        form = ContactForm()
    return render(request, 'contact_form.html', {'form': form})

# Home View
def home_view(request):
    properties = Property.objects.all()
    return render(request, 'home.html', {'properties': properties})

def about_us(request):
    return render(request, "main/about.html")

def contact_us(request):
    if request.method == "POST":
        # Handle form submission logic (e.g., sending email)
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")
        # Add logic to process the message, e.g., send email or save to database
    return render(request, "main/contact.html")


def property_search(request):
    query = request.GET.get('q')
    context = {}
    if query:
        # Search properties by name, description, or any other field
        properties = Property.objects.filter(
            Q(name__icontains=query) | Q(location__icontains=query)
        )

        # Paginate results
        paginator = Paginator(properties, 8)
        page_number = request.GET.get('page')
        properties_paginator = paginator.get_page(page_number)

        context = {
            'properties': properties_paginator,
        }

    return render(request, 'main/property_search.html', context)