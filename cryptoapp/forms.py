from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from .models import Transaction, UserProfile


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

class UpdateUserForm(forms.ModelForm):
    first_name = forms.CharField(max_length=32)
    last_name = forms.CharField(max_length=32)
    class Meta:
        model = UserProfile
        fields = ["profile_pic", "first_name", "last_name", "user_doc"]

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['amount', 'quantity']

    def __init__(self, *args, **kwargs):
        super(TransactionForm, self).__init__(*args, **kwargs)

        # Set required=False for both fields
        self.fields['amount'].required = False
        self.fields['quantity'].required = False
    def clean(self):
        cleaned_data = super().clean()
        quantity = cleaned_data.get('quantity')
        amount = cleaned_data.get('amount')

        if not quantity and not amount:
            raise forms.ValidationError("Please provide either quantity or amount.")
        elif quantity and amount:
            raise forms.ValidationError("Please provide either quantity or amount, not both.")

        return cleaned_data

class AddBalanceForm(forms.Form):
    amount = forms.DecimalField(label='Amount', min_value=0.01)