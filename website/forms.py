from django import forms
from .models import ContactEnquiry


class ContactForm(forms.ModelForm):

    class Meta:
        model = ContactEnquiry

        fields = [
            'name',
            'email',
            'phone',
            'service',
            'message',
        ]

        widgets = {

            'name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter Your Name'
                }
            ),

            'email': forms.EmailInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter Your Email'
                }
            ),

            'phone': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter Your Phone Number'
                }
            ),

            'service': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Service Interested In'
                }
            ),

            'message': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter Your Message',
                    'rows': 5
                }
            ),
        }
