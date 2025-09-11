from django import forms
from django.core.exceptions import ValidationError
from .models import FormSubmission, Location, Service, Employee


class BookingForm(forms.ModelForm):
    class Meta:
        model = FormSubmission
        fields = [
            'customer_first_name',
            'customer_last_name', 
            'customer_email',
            'customer_phone',
            'location',
            'service',
            'preferred_employee',
            'preferred_date',
            'preferred_time',
            'notes',
        ]
        
        widgets = {
            'customer_first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your first name'
            }),
            'customer_last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your last name'
            }),
            'customer_email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'your.email@example.com'
            }),
            'customer_phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '(555) 123-4567'
            }),
            'location': forms.Select(attrs={
                'class': 'form-control'
            }),
            'service': forms.Select(attrs={
                'class': 'form-control'
            }),
            'preferred_employee': forms.Select(attrs={
                'class': 'form-control'
            }),
            'preferred_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'preferred_time': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Any special requests or notes...',
                'rows': 4
            }),
        }
        
        labels = {
            'customer_first_name': 'First Name',
            'customer_last_name': 'Last Name',
            'customer_email': 'Email Address',
            'customer_phone': 'Phone Number',
            'location': 'Location',
            'service': 'Service',
            'preferred_employee': 'Preferred Employee (Optional)',
            'preferred_date': 'Preferred Date',
            'preferred_time': 'Preferred Time',
            'notes': 'Additional Notes',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['preferred_employee'].required = False
        self.fields['preferred_employee'].empty_label = "Any Available Employee"
        
        self.fields['location'].queryset = Location.objects.all()
        self.fields['service'].queryset = Service.objects.filter(is_active=True)
        self.fields['preferred_employee'].queryset = Employee.objects.filter(is_active=True)
        
        self.fields['notes'].required = False
    
    def clean_preferred_date(self):
        from datetime import date
        preferred_date = self.cleaned_data.get('preferred_date')
        
        if preferred_date and preferred_date < date.today():
            raise ValidationError("Please select a future date.")
        
        return preferred_date
    
    def clean(self):
        cleaned_data = super().clean()
        service = cleaned_data.get('service')
        preferred_employee = cleaned_data.get('preferred_employee')
        
        if service and preferred_employee:
            if not preferred_employee.services.filter(id=service.id).exists():
                raise ValidationError(
                    f"{preferred_employee.full_name} does not offer {service.name}. "
                    f"Please select a different employee or choose 'Any Available'."
                )
        
        return cleaned_data
