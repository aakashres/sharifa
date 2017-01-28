from django import forms
from django.utils import timezone
from datetime import timedelta
from .models import *
from django.contrib.auth.models import User


class SignUpForm(forms.Form):
    first_name = forms.CharField(max_length=30, label='First Name',
                                 widget=forms.TextInput(attrs={'placeholder': 'Frist Name'}))
    last_name = forms.CharField(max_length=30, label='Last Name',
                                widget=forms.TextInput(attrs={'placeholder': 'Frist Name'}))

    def signup(self, request, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()

        from django.contrib.auth.models import Group
        grp = Group.objects.get(name='Customer')
        grp.user_set.add(user)

        # default profile
        profile = UserProfile()
        profile.user = user
        profile.save()

        # default limited membership
        membership = Membership()
        membership.user = user
        membership.type = 0
        membership.valid_from = timezone.now()
        membership.valid_to = timezone.now() + timedelta(days=5000)
        membership.save()


class LogInForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'required': 'true',
            'id': 'username',
        }))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'required': 'true',
            'id': 'password',

        }))


class StaffForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({'class': 'form-control'})


class EmailForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'required': 'true',
            'id': 'email',
        }))


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "email",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({'class': 'form-control'})


class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = [
            "description",
            "photo"
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({'class': 'form-control'})


class RequestedProductForm(forms.ModelForm):
    class Meta:
        model = RequestedProduct
        fields = [
            'title',
            'link',
            'remarks',
            'number',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({'class': 'form-control'})
        self.fields['title'].widget.attrs.update({'placeholder': 'Product Title'})
        self.fields['link'].widget.attrs.update({'placeholder': 'Product Link'})
        self.fields['number'].widget.attrs.update({'placeholder': 'Product Quantity'})
        self.fields['remarks'].widget.attrs.update({'placeholder': 'Product Remarks', 'cols': '40', 'rows': '5'})


class PageForm(forms.ModelForm):
    class Meta:
        model = Page
        fields = [
            'title',
            'slug',
            'description',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({'class': 'form-control'})


class SiteConfigForm(forms.ModelForm):
    class Meta:
        model = SiteConfig
        fields = [
            'key',
            'value',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({'class': 'form-control'})


class ShopForm(forms.ModelForm):
    class Meta:
        model = Shop
        fields = [
            'name',
            'logo',
            'link',
            'category',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({'class': 'form-control'})


class ItemCategoryForm(forms.ModelForm):
    class Meta:
        model = ItemCategory
        fields = [
            'title',
            'slug',
            'description',
            'harmony_code',
            'popularity',
            'percent_rate',
            'flat_rate',
            'volume_rate',
            'ecs',
            'vat',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({'class': 'form-control'})


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'title',
            'slug',
            'link',
            'description',
            'photo',
            'category',
            'price',
            'approx_taxes',
            'domestic_shipping',
            'height',
            'length',
            'width',
            'weight',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({'class': 'form-control'})


class QuotationForm(forms.ModelForm):
    class Meta:
        model = Quotation
        fields = [
            'category',
            'price',
            'approx_taxes',
            'domestic_shipping',
            'height',
            'length',
            'width',
            'weight',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({'class': 'form-control'})


class ContactForm(forms.Form):
    name = forms.CharField(max_length=30, label='Name',
                           widget=forms.TextInput(attrs={'placeholder': 'Your Name Here....'}))
    email = forms.EmailField(max_length=30, label='Email',
                             widget=forms.TextInput(attrs={'placeholder': 'Your Email'}))
    subject = forms.CharField(max_length=30, label='Subject',
                              widget=forms.TextInput(attrs={'placeholder': 'Subject'}))
    message = forms.CharField(max_length=30, label='Message',
                              widget=forms.Textarea(attrs={'placeholder': 'Your Message'}))

    class Meta:
        fields = [
            "name",
            "email",
            "subject",
            "message"
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({'class': 'form-control'})


SHIPPING_TYPE = (
    (0, 'Standard Shipping'),
    (1, 'Express Shipping')
)


class EstimateForm(forms.Form):
    price = forms.FloatField(label='Price of item', widget=forms.NumberInput(
        attrs={'placeholder': 'Price of item in $'}))
    sales_tax = forms.FloatField(label='Sales Tac', widget=forms.NumberInput(
        attrs={'placeholder': 'Sales Tax in %'}))
    domestic_shipping = forms.FloatField(
        label='Domestic Shipping', widget=forms.NumberInput(attrs={'placeholder': 'Domestic Shipping Charge in Rs'}))
    weight = forms.FloatField(label='Weight', widget=forms.NumberInput(attrs={'placeholder': 'Weight in lbs'}))
    length = forms.FloatField(label='Length', widget=forms.NumberInput(attrs={'placeholder': 'Length in Inch'}))
    width = forms.FloatField(label='Width', widget=forms.NumberInput(attrs={'placeholder': 'Width in Inch'}))
    height = forms.FloatField(label='Height', widget=forms.NumberInput(attrs={'placeholder': 'Height in Inch'}))
    shipping_type = forms.ChoiceField(choices=SHIPPING_TYPE, label='Shipping Type', widget=forms.Select())

    class Meta:
        fields = [
            "price",
            "sales_tax",
            "domestic_shipping",
            "weight",
            "length",
            "width",
            "height",
            "shipping_type"
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({'class': 'form-control'})
