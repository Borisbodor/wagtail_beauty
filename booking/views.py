from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from .forms import BookingForm
from .models import FormSubmission
from home.models import LocationPage, ServicePage, EmployeePage, ServiceLocation


def booking_page_view(request, page):
    """
    Handle booking page display and form submission
    """
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            # Save the form submission
            submission = form.save()
            
            # Add success message
            messages.success(
                request, 
                f"Thank you {submission.customer_first_name}! Your booking request has been submitted. "
                f"We'll contact you within 24 hours to confirm your appointment."
            )
            
            # Redirect to the same page to prevent resubmission
            return redirect(request.path + '?success=1')
        else:
            # Form has errors, they'll be displayed in the template
            messages.error(request, "Please correct the errors below and try again.")
    else:
        form = BookingForm()
    
    # Check if this is a success redirect
    success = request.GET.get('success') == '1'
    
    return render(request, page.get_template(request), {
        'page': page,
        'form': form,
        'success': success,
    })


def get_services_by_location(request):
    """
    API endpoint to get services available at a specific location
    """
    location_id = request.GET.get('location_id')
    if not location_id:
        return JsonResponse({'services': []})
    
    try:
        location = LocationPage.objects.get(id=location_id)
        # Get services available at this location through ServiceLocation
        service_locations = ServiceLocation.objects.filter(location=location).select_related('service')
        
        services_data = []
        for sl in service_locations:
            service = sl.service
            services_data.append({
                'id': service.id,
                'name': service.display_name,
                'price': str(service.price_display),
                'duration': service.duration_display
            })
        
        return JsonResponse({'services': services_data})
    except LocationPage.DoesNotExist:
        return JsonResponse({'services': []})


def get_employees_by_location(request):
    """
    API endpoint to get employees working at a specific location
    """
    location_id = request.GET.get('location_id')
    if not location_id:
        return JsonResponse({'employees': []})
    
    try:
        location = LocationPage.objects.get(id=location_id)
        # Get employees working at this location
        employees = EmployeePage.objects.filter(work_location=location, live=True)
        
        employees_data = []
        for employee in employees:
            employees_data.append({
                'id': employee.id,
                'name': employee.display_name,
                'job_title': employee.job_title
            })
        
        return JsonResponse({'employees': employees_data})
    except LocationPage.DoesNotExist:
        return JsonResponse({'employees': []})
