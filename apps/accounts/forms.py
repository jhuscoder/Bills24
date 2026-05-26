import uuid
from django import forms
from .models import Account 
from django.contrib.auth.forms import ReadOnlyPasswordHashField

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['email', 'first_name', 'last_name', 'phone']
        
        
class AccountCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = Account
        fields = ['email', 'first_name', 'last_name', 'phone']

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get('password1')
        if password:
            user.set_password(password)
        if not user.user_id:
            user.user_id = f"{uuid.uuid4()}"
        if commit:
            user.save()
        return user


class AccountChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = Account
        fields = ['email', 'password', 'first_name', 'last_name', 'phone', 'is_active', 'is_staff']

    def clean_password(self):
        return self.initial['password']