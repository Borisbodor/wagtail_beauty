from django.db import models
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from wagtail.models import Page
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.snippets.models import register_snippet
from wagtail.fields import RichTextField, StreamField
from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock
from modelcluster.models import ClusterableModel
from modelcluster.fields import ParentalKey
# Import blocks and mixins from home app
from home.models import HeroMixin, ServicesGridBlock, FeaturesGridBlock, CallToActionBlock, TextBlock, ImageGalleryBlock


# ============================================================================
# BOOKING LOCATION MODEL - Synced with Page-based Location System
# ============================================================================
# 
# This Location model is used for booking functionality and stays synced
# with the page-based LocationPage system in home/models.py.
# 
# The page system (LocationPage) handles:
# - Public location profiles and content management  
# - Rich descriptions, images, full information pages
# 
# This model handles:
# - Booking form dropdowns and selections
# - Employee location assignments
# - Internal operational data (hours, contact info)
# 
# They stay in sync automatically when locations are published/unpublished.

@register_snippet
class Location(models.Model):
    """
    Location model for booking functionality.
    Synced with LocationPage from home app.
    """
    name = models.CharField(max_length=100, help_text="Location name (e.g. 'Downtown Salon')")
    address = models.TextField(help_text="Full address of this location")
    phone = models.CharField(max_length=20, blank=True, help_text="Contact phone number")
    email = models.EmailField(blank=True, help_text="Contact email")
    
    # Reference to the page (optional, for sync)
    location_page = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        help_text="Connected location page (auto-set)"
    )
    
    HOUR_CHOICES = [
        ('Closed', 'Closed'),
        ('8:00 AM - 4:00 PM', '8:00 AM - 4:00 PM'),
        ('8:00 AM - 5:00 PM', '8:00 AM - 5:00 PM'),
        ('8:00 AM - 6:00 PM', '8:00 AM - 6:00 PM'),
        ('8:00 AM - 8:00 PM', '8:00 AM - 8:00 PM'),
        ('9:00 AM - 5:00 PM', '9:00 AM - 5:00 PM'),
        ('9:00 AM - 6:00 PM', '9:00 AM - 6:00 PM'),
        ('9:00 AM - 7:00 PM', '9:00 AM - 7:00 PM'),
        ('9:00 AM - 8:00 PM', '9:00 AM - 8:00 PM'),
        ('10:00 AM - 4:00 PM', '10:00 AM - 4:00 PM'),
        ('10:00 AM - 5:00 PM', '10:00 AM - 5:00 PM'),
        ('10:00 AM - 6:00 PM', '10:00 AM - 6:00 PM'),
        ('11:00 AM - 4:00 PM', '11:00 AM - 4:00 PM'),
        ('11:00 AM - 5:00 PM', '11:00 AM - 5:00 PM'),
    ]
    
    monday_hours = models.CharField(max_length=50, choices=HOUR_CHOICES, default="9:00 AM - 6:00 PM")
    tuesday_hours = models.CharField(max_length=50, choices=HOUR_CHOICES, default="9:00 AM - 6:00 PM")
    wednesday_hours = models.CharField(max_length=50, choices=HOUR_CHOICES, default="9:00 AM - 6:00 PM")
    thursday_hours = models.CharField(max_length=50, choices=HOUR_CHOICES, default="9:00 AM - 6:00 PM")
    friday_hours = models.CharField(max_length=50, choices=HOUR_CHOICES, default="9:00 AM - 6:00 PM")
    saturday_hours = models.CharField(max_length=50, choices=HOUR_CHOICES, default="10:00 AM - 4:00 PM")
    sunday_hours = models.CharField(max_length=50, choices=HOUR_CHOICES, default="Closed")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    panels = [
        FieldPanel('location_page'),  # Readonly - shows connected page
        FieldPanel('name'),
        FieldPanel('address'),
        MultiFieldPanel([
            FieldPanel('phone'),
            FieldPanel('email'),
        ], heading="Contact Information"),
        MultiFieldPanel([
            FieldPanel('monday_hours'),
            FieldPanel('tuesday_hours'),
            FieldPanel('wednesday_hours'),
            FieldPanel('thursday_hours'),
            FieldPanel('friday_hours'),
            FieldPanel('saturday_hours'),
            FieldPanel('sunday_hours'),
        ], heading="Opening Hours"),
    ]

    class Meta:
        verbose_name = "Location"
        verbose_name_plural = "Locations"
        ordering = ['name']

    def __str__(self):
        return self.name


@register_snippet  
class Service(models.Model):
    name = models.CharField(max_length=100, help_text="Service name (e.g. 'Haircut & Style')")
    description = models.TextField(help_text="Detailed description of the service")
    price = models.DecimalField(max_digits=8, decimal_places=2, help_text="Price in dollars (e.g. 45.00)")
    duration_minutes = models.PositiveIntegerField(help_text="How long does this service take? (in minutes)")
    
    locations = models.ManyToManyField(Location, help_text="Which locations offer this service?")
    
    
    CATEGORY_CHOICES = [
        ('hair', 'Hair Services'),
        ('nails', 'Nail Services'),
        ('skincare', 'Skincare & Facials'),
        ('massage', 'Massage & Spa'),
        ('makeup', 'Makeup Services'),
        ('other', 'Other Services'),
    ]
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='other')
    is_active = models.BooleanField(default=True, help_text="Uncheck to hide this service from booking")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    panels = [
        FieldPanel('name'),
        FieldPanel('description'),
        MultiFieldPanel([
            FieldPanel('price'),
            FieldPanel('duration_minutes'),
            FieldPanel('category'),
        ], heading="Service Details"),
        FieldPanel('locations'),
        FieldPanel('is_active'),
    ]

    class Meta:
        verbose_name = "Service"
        verbose_name_plural = "Services"
        ordering = ['category', 'name']

    def __str__(self):
        return f"{self.name} (${self.price})"
        
    def get_locations_list(self):
        return ", ".join([loc.name for loc in self.locations.all()])


# ============================================================================
# BOOKING EMPLOYEE MODEL - Synced with Page-based Employee System
# ============================================================================
# 
# This Employee model is used for booking functionality and stays synced
# with the page-based EmployeePage system in home/models.py.
# 
# The page system (EmployeePage) handles:
# - Public employee profiles and content management
# - Rich descriptions, images, full bios
# 
# This model handles:
# - Booking form dropdowns and selections
# - Service assignments and scheduling
# - Internal operational data
# 
# They stay in sync automatically when employees are published/unpublished.

@register_snippet
class Employee(models.Model):
    """
    Simplified Employee model for booking functionality.
    Synced with EmployeePage from home app.
    """
    # Basic info (synced from EmployeePage)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100) 
    
    # Reference to the page (optional, for sync)
    employee_page = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        help_text="Connected employee page (auto-set)"
    )
    
    # Booking-specific fields
    location = models.ForeignKey(Location, on_delete=models.CASCADE, help_text="Primary work location")
    services = models.ManyToManyField(Service, help_text="Services this employee can perform")
    is_active = models.BooleanField(default=True, help_text="Available for bookings?")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    panels = [
        MultiFieldPanel([
            FieldPanel('first_name'),
            FieldPanel('last_name'),
        ], heading="Name"),
        MultiFieldPanel([
            FieldPanel('location'),
            FieldPanel('services'),
        ], heading="Work Assignment"),
        FieldPanel('is_active'),
    ]

    class Meta:
        verbose_name = "Employee"
        verbose_name_plural = "Employees"
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
        
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
        
    def get_services_list(self):
        return ", ".join([service.name for service in self.services.all()])


@register_snippet
class FormSubmission(models.Model):
    customer_first_name = models.CharField(max_length=50, help_text="Customer's first name")
    customer_last_name = models.CharField(max_length=50, help_text="Customer's last name")
    customer_email = models.EmailField(help_text="Customer's email address")
    customer_phone = models.CharField(max_length=20, help_text="Customer's phone number")
    
    location = models.ForeignKey(Location, on_delete=models.CASCADE, help_text="Which location?")
    service = models.ForeignKey(Service, on_delete=models.CASCADE, help_text="Which service?")
    preferred_employee = models.ForeignKey(
        Employee, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        help_text="Preferred employee (optional - leave blank for any available)"
    )
    
    preferred_date = models.DateField(help_text="Preferred appointment date")
    preferred_time = models.TimeField(help_text="Preferred appointment time")
    notes = models.TextField(blank=True, help_text="Additional notes or special requests from customer")
    STATUS_CHOICES = [
        ('pending', 'Pending Review'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    staff_notes = models.TextField(blank=True, help_text="Internal notes for staff (not visible to customer)")
    submitted_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    panels = [
        MultiFieldPanel([
            FieldPanel('customer_first_name'),
            FieldPanel('customer_last_name'),
            FieldPanel('customer_email'),
            FieldPanel('customer_phone'),
        ], heading="Customer Information"),
        MultiFieldPanel([
            FieldPanel('location'),
            FieldPanel('service'),
            FieldPanel('preferred_employee'),
        ], heading="Booking Details"),
        MultiFieldPanel([
            FieldPanel('preferred_date'),
            FieldPanel('preferred_time'),
        ], heading="Timing"),
        FieldPanel('notes'),
        MultiFieldPanel([
            FieldPanel('status'),
            FieldPanel('staff_notes'),
        ], heading="Staff Only"),
    ]

    class Meta:
        verbose_name = "Form Submission"
        verbose_name_plural = "Form Submissions"
        ordering = ['-submitted_at']

    def __str__(self):
        return f"{self.customer_first_name} {self.customer_last_name} - {self.service.name} ({self.status})"
        
    @property
    def customer_full_name(self):
        return f"{self.customer_first_name} {self.customer_last_name}"
        
    def get_employee_preference(self):
        if self.preferred_employee:
            return str(self.preferred_employee)
        return "Any Available"


class BookingFormBlock(blocks.StructBlock):
    title = blocks.CharBlock(max_length=200, default="Book Your Appointment")
    subtitle = blocks.TextBlock(default="Fill out the form below and we'll contact you within 24 hours")
    
    def get_context(self, value, parent_context=None):
        from .forms import BookingForm
        context = super().get_context(value, parent_context)
        
        form = None
        if parent_context and 'form' in parent_context:
            form = parent_context['form']
        elif parent_context and 'page' in parent_context:
            page = parent_context['page']
            if hasattr(page, '_form'):
                form = page._form
        
        if form is None:
            form = BookingForm()
            
        context['form'] = form
        return context
    
    class Meta:
        template = 'blocks/booking_form_block.html'
        icon = 'form'
        label = 'Booking Form'


class BookingPage(HeroMixin, Page):
    content = StreamField([
        ('booking_form', BookingFormBlock()),
        ('services', ServicesGridBlock()),
        ('features', FeaturesGridBlock()),
        ('cta', CallToActionBlock()),
        ('text', TextBlock()),
        ('gallery', ImageGalleryBlock()),
    ], blank=True, use_json_field=True)
    
    thank_you_text = RichTextField(
        blank=True, 
        default="<p>Thank you for your booking request! We'll contact you within 24 hours to confirm your appointment.</p>",
        help_text="Message shown after successful form submission"
    )

    content_panels = Page.content_panels + [
        MultiFieldPanel(HeroMixin.hero_panels, heading="Hero Section", classname="collapsible"),
        FieldPanel('content'),
        FieldPanel('thank_you_text'),
    ]

    def serve(self, request):
        from .forms import BookingForm
        
        if request.method == 'POST':
            form = BookingForm(request.POST)
            if form.is_valid():
                submission = form.save()
                messages.success(request, 'Your booking request has been submitted successfully!')
                return render(request, self.get_template(request), {
                    'page': self,
                    'form': BookingForm(),
                    'success': True,
                })
            else:
                messages.error(request, 'Please correct the errors below.')
        else:
            form = BookingForm()
        
        self._form = form
        
        return render(request, self.get_template(request), {
            'page': self,
            'form': form,
        })
        
    def get_context(self, request, *args, **kwargs):
        from .forms import BookingForm
        context = super().get_context(request, *args, **kwargs)
        context['form'] = BookingForm()
        
        return context

    class Meta:
        verbose_name = "Booking Page"