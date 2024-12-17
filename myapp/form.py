from django.forms import ModelForm
from .models import Expense
from django.contrib.auth.models import User
from django import forms


class ExpenseForm(ModelForm):
    class Meta:
        model = Expense
        fields = ('name', 'amount', 'category')

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput, label='confirm_password')

    class Meta:
        model = User
        fields = ['username', 'email']

        def password_confirm(self):
            password = self.cleaned_data.get('password')
            confirm_password = self.cleaned_data.get('confirm_password')
            if password and confirm_password and password != confirm_password:
                raise forms.validationError('invalid passsword')
