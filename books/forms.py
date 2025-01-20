from django import forms
from .models import Transaction

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['member', 'book', 'issue_date', 'return_date', 'status', 'note']


from django import forms
from .models import Staff

class StaffForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = ['name', 'email', 'role', 'phone_number']

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if len(phone_number) != 10:
            raise forms.ValidationError("Phone number must be 10 digits.")
        if not phone_number.isdigit():
            raise forms.ValidationError("Phone number must only contain digits.")
        return phone_number

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if '@' not in email:
            raise forms.ValidationError("Please enter a valid email address.")
        return email
