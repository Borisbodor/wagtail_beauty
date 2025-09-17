from django.db import models
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from wagtail.models import Page
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.fields import RichTextField, StreamField
from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock
from modelcluster.models import ClusterableModel
from modelcluster.fields import ParentalKey
# Import blocks and mixins from home app
from home.models import HeroMixin, FeaturesGridBlock, CallToActionBlock, TextBlock, ImageGalleryBlock, ServiceChooserBlock, EmployeeChooserBlock, LocationChooserBlock


# ============================================================================
# BOOKING FORM BLOCK
# ============================================================================

class BookingFormBlock(blocks.StructBlock):
    title = blocks.CharBlock(max_length=200, default="Book Your Appointment")
    subtitle = blocks.TextBlock(default="Fill out the form below and we'll contact you to confirm your booking.")
    
    class Meta:
        template = 'blocks/booking_form_block.html'
        icon = 'form'
        label = 'Booking Form'


# ============================================================================
# BOOKING PAGE MODEL
# ============================================================================

class BookingPage(HeroMixin, Page):
    content = StreamField([
        ('booking_form', BookingFormBlock()),
        ('service_selector', ServiceChooserBlock()),
        ('employee_selector', EmployeeChooserBlock()),
        ('location_selector', LocationChooserBlock()),
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
    
    def serve(self, request, *args, **kwargs):
        from .views import booking_page_view
        return booking_page_view(request, self)


# ============================================================================
# FORM SUBMISSION MODEL
# ============================================================================

class FormSubmission(models.Model):
    """
    Booking form submissions. References page models directly instead of snippets.
    """
    # Customer information
    customer_first_name = models.CharField(max_length=50, help_text="Customer's first name")
    customer_last_name = models.CharField(max_length=50, help_text="Customer's last name")
    customer_email = models.EmailField(help_text="Customer's email address")
    customer_phone = models.CharField(max_length=20, help_text="Customer's phone number")
    
    # Booking details - now reference page models directly
    location = models.ForeignKey(
        'home.LocationPage',
        on_delete=models.CASCADE,
        related_name='booking_submissions',
        help_text="Which location?"
    )
    service = models.ForeignKey(
        'home.ServicePage',
        on_delete=models.CASCADE,
        related_name='booking_submissions',
        help_text="Which service?"
    )
    preferred_employee = models.ForeignKey(
        'home.EmployeePage',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='booking_submissions',
        help_text="Preferred employee (optional - leave blank for any available)"
    )
    
    # Appointment details
    preferred_date = models.DateField(help_text="Preferred appointment date")
    preferred_time = models.TimeField(help_text="Preferred appointment time")
    notes = models.TextField(blank=True, help_text="Additional notes or special requests from customer")
    
    # Status tracking
    STATUS_CHOICES = [
        ('pending', 'Pending Review'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    staff_notes = models.TextField(blank=True, help_text="Internal notes for staff (not visible to customer)")
    
    # Timestamps
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
        ], heading="Status & Notes"),
    ]

    class Meta:
        verbose_name = "Booking Submission"
        verbose_name_plural = "Booking Submissions"
        ordering = ['-submitted_at']

    def __str__(self):
        return f"{self.customer_full_name} - {self.service.display_name} at {self.location.display_name}"
    
    @property
    def customer_full_name(self):
        return f"{self.customer_first_name} {self.customer_last_name}"
    
    def get_employee_preference(self):
        """Get preferred employee display name or 'Any Available'"""
        if self.preferred_employee:
            return self.preferred_employee.display_name
        return "Any Available"
    get_employee_preference.short_description = "Preferred Employee"