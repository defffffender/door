from django import forms
from .models import ContactRequest


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactRequest
        fields = ['name', 'phone', 'email', 'message', 'file']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Ваше имя', 'class': 'form-input'}),
            'phone': forms.TextInput(attrs={'placeholder': '+998 __ ___ __ __', 'class': 'form-input'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email', 'class': 'form-input'}),
            'message': forms.Textarea(attrs={'placeholder': 'Сообщение', 'class': 'form-input', 'rows': 4}),
            'file': forms.FileInput(attrs={'class': 'form-file'}),
        }
