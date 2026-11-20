from django import forms
from .models import PromoCode,Property, Amenity, PropertyType,Booking,Review,PaymentMethod,Address, UserProfile
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
import datetime
class LoginForm(forms.Form):
    email = forms.EmailField(label='Email', max_length=100, required=True)
    password = forms.CharField(label='Password', widget=forms.PasswordInput(), required=True)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not User.objects.filter(email=email).exists():
            raise ValidationError('Email does not exist.')
        return email

class SignUpForm(forms.Form):
    name = forms.CharField(label='Full Name', max_length=100, required=True)
    email = forms.EmailField(label='Email', max_length=100, required=True)
    password = forms.CharField(label='Password', widget=forms.PasswordInput(), required=True)
    confirm_password = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(), required=True)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError('Email already exists.')
        return email

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 8:
            raise ValidationError('Password must be at least 8 characters long.')
        return password

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise ValidationError('Passwords do not match.')

        return cleaned_data

class PropertyForm(forms.ModelForm):
    """Form to create/edit a property."""
    class Meta:
        model = Property
        fields = ['name', 'property_type', 'description', 'location', 'price_per_night', 
                  'max_guests', 'availability_start', 'availability_end', 'image', 'amenities']
        widgets = {
            'availability_start': forms.DateInput(attrs={'type': 'date'}),
            'availability_end': forms.DateInput(attrs={'type': 'date'}),
        }

    amenities = forms.ModelMultipleChoiceField(
        queryset=Amenity.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    def __init__(self, *args, **kwargs):
        super(PropertyForm, self).__init__(*args, **kwargs)
        self.fields['property_type'].queryset = PropertyType.objects.all()

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['check_in_date', 'check_out_date', 'guests']
        widgets = {
            'check_in_date': forms.DateInput(attrs={'type': 'date'}),
            'check_out_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, property=None, **kwargs):
        super().__init__(*args, **kwargs)
        if property:
            self.fields['property'].initial = property

    total_price = forms.DecimalField(widget=forms.HiddenInput(), required=False)
    property = forms.ModelChoiceField(queryset=Property.objects.all(), widget=forms.HiddenInput(), required=False)

    def clean(self):
        cleaned_data = super().clean()
        check_in = cleaned_data.get('check_in_date')
        check_out = cleaned_data.get('check_out_date')

        if check_in and check_out:
            if check_out <= check_in:
                raise forms.ValidationError("Check-out date must be after the check-in date.")
        return cleaned_data


class ReviewForm(forms.ModelForm):
    """Form for submitting a review for a property."""
    class Meta:
        model = Review
        fields = ['rating', 'comment']

    rating = forms.IntegerField(min_value=1, max_value=5, widget=forms.NumberInput(attrs={'class': 'rating'}))
    comment = forms.CharField(widget=forms.Textarea, required=False)

class PaymentMethodForm(forms.ModelForm):
    """Form for adding a payment method."""
    class Meta:
        model = PaymentMethod
        fields = ['method_type', 'details']
        
    method_type = forms.ChoiceField(choices=[('credit_card', 'Credit Card'), ('paypal', 'PayPal')])
    details = forms.CharField(widget=forms.Textarea)

class AddressForm(forms.ModelForm):
    """Form for creating a new address."""
    class Meta:
        model = Address
        fields = ['street', 'city', 'state', 'zip_code', 'country']

class UserProfileForm(forms.ModelForm):
    """Form for updating user profile details."""
    class Meta:
        model = UserProfile
        fields = ['phone_number', 'profile_picture', 'date_of_birth']
    
    phone_number = forms.CharField(max_length=15, required=False)
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=False)

class PromoCodeForm(forms.Form):
    """Form for applying a promo code."""
    code = forms.CharField(max_length=20, required=True)
    
    def clean_code(self):
        code = self.cleaned_data.get('code')
        try:
            promo_code = PromoCode.objects.get(code=code)
            if promo_code.expiration_date < datetime.date.today():
                raise forms.ValidationError("This promo code has expired.")
        except PromoCode.DoesNotExist:
            raise forms.ValidationError("Invalid promo code.")
        return code

class ContactForm(forms.Form):
    """Form for general user inquiries."""
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)

    def send_email(self):
        # Implement actual email sending logic here
        pass

class ContactForm(forms.Form):
    """Form for general user inquiries."""
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)

    def send_email(self):
        # Implement actual email sending logic here
        pass
