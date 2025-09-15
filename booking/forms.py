from django import forms
from django.core.exceptions import ValidationError
from .models import FormSubmission


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
        
        # Import page models
        from home.models import LocationPage, ServicePage, EmployeePage
        
        # Only show locations initially - services and employees will be populated via API
        self.fields['location'].queryset = LocationPage.objects.live()
        self.fields['location'].empty_label = "Select a location"
        
        # Start with empty querysets for display, but allow all live pages for validation
        # The JavaScript will populate the options, but Django needs access to all objects for validation
        all_services = ServicePage.objects.live()
        all_employees = EmployeePage.objects.live()
        
        self.fields['service'].queryset = all_services
        self.fields['service'].empty_label = "Select a location first"
        
        self.fields['preferred_employee'].queryset = all_employees
        self.fields['preferred_employee'].empty_label = "Select a location first"
        
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
        location = cleaned_data.get('location')
        
        # Validate employee works at selected location
        if preferred_employee and location:
            if preferred_employee.work_location and preferred_employee.work_location != location:
                raise ValidationError(
                    f"{preferred_employee.display_name} works at {preferred_employee.work_location.display_name}, "
                    f"not at {location.display_name}. Please select a different employee or location."
                )
        
        # Validate service is available at selected location
        if service and location:
            # Check if service is offered at the selected location through ServiceLocation model
            from home.models import ServiceLocation
            if not ServiceLocation.objects.filter(service=service, location=location).exists():
                available_locations = [sl.location.display_name for sl in service.service_locations.all()]
                if available_locations:
                    locations_text = ", ".join(available_locations)
                    raise ValidationError(
                        f"{service.display_name} is only available at: {locations_text}. "
                        f"Please select a different service or location."
                    )
                else:
                    raise ValidationError(
                        f"{service.display_name} is not available at any locations yet. "
                        f"Please select a different service."
                    )
        
        return cleaned_data
