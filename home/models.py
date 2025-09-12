from django.db import models
from wagtail.models import Page
from wagtail.fields import RichTextField, StreamField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock
from wagtail.images import get_image_model_string


class HeroMixin(models.Model):
    """
    Mixin that adds hero section fields to any page.
    Pages can enable/disable the hero section and customize all hero content.
    """
    # Hero control
    show_hero = models.BooleanField(
        default=True, 
        help_text="Show hero section at the top of this page"
    )
    
    # Hero content fields (matching HeroBlock fields)
    hero_title = models.CharField(
        max_length=200, 
        blank=True,
        default="Welcome to Beauty Salon",
        help_text="Main hero headline"
    )
    hero_subtitle = models.TextField(
        blank=True,
        default="Transform your beauty with premium treatments",
        help_text="Subtitle text below the main headline"
    )
    hero_image = models.ForeignKey(
        get_image_model_string(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text="Hero image (overlays background)"
    )
    hero_background_image = models.ForeignKey(
        get_image_model_string(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text="Background image for hero section"
    )
    
    # Hero buttons
    hero_primary_button_text = models.CharField(
        max_length=50,
        blank=True,
        default="Book Now",
        help_text="Primary button text"
    )
    hero_primary_button_url = models.URLField(
        blank=True,
        help_text="Primary button URL"
    )
    hero_secondary_button_text = models.CharField(
        max_length=50,
        blank=True,
        default="Services",
        help_text="Secondary button text"
    )
    hero_secondary_button_url = models.URLField(
        blank=True,
        help_text="Secondary button URL"
    )
    
    # Admin panel configuration for hero fields
    hero_panels = [
        FieldPanel('show_hero'),
        MultiFieldPanel([
            FieldPanel('hero_title'),
            FieldPanel('hero_subtitle'),
        ], heading="Hero Text"),
        MultiFieldPanel([
            FieldPanel('hero_image'),
            FieldPanel('hero_background_image'),
        ], heading="Hero Images"),
        MultiFieldPanel([
            FieldPanel('hero_primary_button_text'),
            FieldPanel('hero_primary_button_url'),
            FieldPanel('hero_secondary_button_text'),
            FieldPanel('hero_secondary_button_url'),
        ], heading="Hero Buttons"),
    ]
    
    class Meta:
        abstract = True


class ServiceBlock(blocks.StructBlock):
    image = ImageChooserBlock()
    title = blocks.CharBlock(max_length=100)
    description = blocks.TextBlock()
    link_url = blocks.URLBlock(required=False)
    
    class Meta:
        template = 'blocks/service_block.html'
        icon = 'pick'
        label = 'Service'


class FeatureBlock(blocks.StructBlock):
    image = ImageChooserBlock()
    title = blocks.CharBlock(max_length=100)
    description = blocks.TextBlock()
    
    class Meta:
        template = 'blocks/feature_block.html'
        icon = 'tick'
        label = 'Feature'


# HeroBlock removed - now handled by HeroMixin on all pages
# Hero functionality is available via the "Hero Section" tab in page admin


class ServicesGridBlock(blocks.StructBlock):
    title = blocks.CharBlock(max_length=200, default="Our Services")
    subtitle = blocks.TextBlock(default="Professional beauty treatments")
    services = blocks.ListBlock(ServiceBlock())
    
    class Meta:
        template = 'blocks/services_grid_block.html'
        icon = 'list-ul'
        label = 'Services'


class FeaturesGridBlock(blocks.StructBlock):
    title = blocks.CharBlock(max_length=200, default="Why Choose Us")
    subtitle = blocks.TextBlock(default="Quality service you can trust")
    features = blocks.ListBlock(FeatureBlock())
    background_style = blocks.ChoiceBlock(
        choices=[
            ('white', 'White'),
            ('light', 'Light Gray'),
            ('primary', 'Brand Color'),
        ],
        default='light'
    )
    
    class Meta:
        template = 'blocks/features_grid_block.html'
        icon = 'tick-inverse'
        label = 'Features'


class CallToActionBlock(blocks.StructBlock):
    title = blocks.CharBlock(max_length=200, default="Book Your Appointment")
    subtitle = blocks.TextBlock(default="Ready to look your best?")
    primary_button_text = blocks.CharBlock(max_length=50, default="Book Now")
    primary_button_url = blocks.URLBlock(required=False)
    secondary_button_text = blocks.CharBlock(max_length=50, default="Contact")
    secondary_button_url = blocks.URLBlock(required=False)
    background_style = blocks.ChoiceBlock(
        choices=[
            ('white', 'White'),
            ('light', 'Light Gray'), 
            ('primary', 'Brand Color'),
        ],
        default='white'
    )
    
    class Meta:
        template = 'blocks/cta_block.html'
        icon = 'plus'
        label = 'Call to Action'


class TextBlock(blocks.StructBlock):
    title = blocks.CharBlock(max_length=200, required=False)
    content = blocks.RichTextBlock()
    background_style = blocks.ChoiceBlock(
        choices=[
            ('white', 'White'),
            ('light', 'Light Gray'),
            ('primary', 'Brand Color'),
        ],
        default='white'
    )
    
    class Meta:
        template = 'blocks/text_block.html'
        icon = 'edit'
        label = 'Text'


class ImageGalleryBlock(blocks.StructBlock):
    title = blocks.CharBlock(max_length=200, required=False)
    images = blocks.ListBlock(ImageChooserBlock())
    
    class Meta:
        template = 'blocks/gallery_block.html'
        icon = 'image'
        label = 'Gallery'


class HomePage(HeroMixin, Page):
    content = StreamField([
        ('services', ServicesGridBlock()),
        ('features', FeaturesGridBlock()),
        ('cta', CallToActionBlock()),
        ('text', TextBlock()),
        ('gallery', ImageGalleryBlock()),
    ], blank=True, use_json_field=True)

    content_panels = Page.content_panels + [
        MultiFieldPanel(HeroMixin.hero_panels, heading="Hero Section", classname="collapsible"),
        FieldPanel('content'),
    ]


class EmployeesPage(HeroMixin, Page):
    """
    Parent page for all employee pages. This page displays a listing of all employees.
    """
    intro = RichTextField(blank=True, help_text="Introduction text for the employees page")
    
    content_panels = Page.content_panels + [
        MultiFieldPanel(HeroMixin.hero_panels, heading="Hero Section", classname="collapsible"),
        FieldPanel('intro'),
    ]

    # Constrain child pages to only EmployeePage
    subpage_types = ['home.EmployeePage']
    
    class Meta:
        verbose_name = "Employees Page"


class EmployeePage(HeroMixin, Page):
    """
    Individual employee page. Can only be created as a child of EmployeesPage.
    """
    # Import Location model from booking app
    from booking.models import Location
    
    # Employee fields as requested
    first_name = models.CharField(max_length=100, help_text="Employee's first name")
    last_name = models.CharField(max_length=100, help_text="Employee's last name")
    full_name = models.CharField(max_length=200, blank=True, help_text="Full display name (auto-generated if empty)") 
    employee_image = models.ForeignKey(
        get_image_model_string(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text="Employee photo"
    )
    email = models.EmailField(blank=True, help_text="Employee's email address")
    job_title = models.CharField(max_length=200, help_text="Employee's job title/position")
    description = RichTextField(blank=True, help_text="Employee's bio, specialties, or description")
    work_location = models.ForeignKey(
        'booking.Location', 
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="Employee's primary work location"
    )

    content_panels = Page.content_panels + [
        MultiFieldPanel(HeroMixin.hero_panels, heading="Hero Section", classname="collapsible"),
        MultiFieldPanel([
            FieldPanel('first_name'),
            FieldPanel('last_name'),
            FieldPanel('full_name'),
        ], heading="Name Information"),
        FieldPanel('employee_image'),
        MultiFieldPanel([
            FieldPanel('email'),
            FieldPanel('job_title'),
        ], heading="Contact & Position"),
        FieldPanel('description'),
        FieldPanel('work_location'),
    ]

    # Constrain parent pages to only EmployeesPage
    parent_page_types = ['home.EmployeesPage']
    
    def save(self, *args, **kwargs):
        # Auto-generate full_name if empty
        if not self.full_name:
            self.full_name = f"{self.first_name} {self.last_name}".strip()
        super().save(*args, **kwargs)
        
        # Sync with booking Employee model when page is live
        if self.live:
            self.sync_to_booking_employee()
    
    def sync_to_booking_employee(self):
        """Create/update corresponding Employee in booking app"""
        from booking.models import Employee as BookingEmployee
        
        if not self.work_location:
            return  # Need work_location for booking employee
            
        # Get or create booking employee
        booking_employee, created = BookingEmployee.objects.get_or_create(
            employee_page=self,
            defaults={
                'first_name': self.first_name,
                'last_name': self.last_name,
                'location': self.work_location,
                'is_active': True,
            }
        )
        
        # Update fields if not created
        if not created:
            booking_employee.first_name = self.first_name
            booking_employee.last_name = self.last_name
            booking_employee.location = self.work_location
            booking_employee.save()
    
    def unpublish(self, *args, **kwargs):
        """Deactivate booking employee when page is unpublished"""
        result = super().unpublish(*args, **kwargs)
        
        # Deactivate corresponding booking employee
        from booking.models import Employee as BookingEmployee
        try:
            booking_employee = BookingEmployee.objects.get(employee_page=self)
            booking_employee.is_active = False
            booking_employee.save()
        except BookingEmployee.DoesNotExist:
            pass
            
        return result
    
    @property
    def display_name(self):
        """Primary display name: first_name + last_name"""
        return f"{self.first_name} {self.last_name}".strip()
    
    @property 
    def short_name(self):
        """Short name for links/breadcrumbs: last_name"""
        return self.last_name
        
    def __str__(self):
        return self.display_name
    
    class Meta:
        verbose_name = "Employee Page"


class LocationsPage(HeroMixin, Page):
    """
    Parent page for all location pages. This page displays a listing of all locations.
    """
    intro = RichTextField(blank=True, help_text="Introduction text for the locations page")
    
    content_panels = Page.content_panels + [
        MultiFieldPanel(HeroMixin.hero_panels, heading="Hero Section", classname="collapsible"),
        FieldPanel('intro'),
    ]

    # Constrain child pages to only LocationPage
    subpage_types = ['home.LocationPage']
    
    class Meta:
        verbose_name = "Locations Page"


class LocationPage(HeroMixin, Page):
    """
    Individual location page. Can only be created as a child of LocationsPage.
    """
    # Basic location information
    location_name = models.CharField(max_length=100, help_text="Location name (e.g. 'Downtown Salon')")
    address = models.TextField(help_text="Full address of this location")
    phone = models.CharField(max_length=20, blank=True, help_text="Contact phone number")
    email = models.EmailField(blank=True, help_text="Contact email")
    
    # Location image for the page
    location_image = models.ForeignKey(
        get_image_model_string(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text="Location photo"
    )
    
    # Description for the location page
    description = RichTextField(blank=True, help_text="Location description, amenities, special features")
    
    # Hours (matching the booking Location model)
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

    content_panels = Page.content_panels + [
        MultiFieldPanel(HeroMixin.hero_panels, heading="Hero Section", classname="collapsible"),
        MultiFieldPanel([
            FieldPanel('location_name'),
            FieldPanel('address'),
        ], heading="Location Information"),
        FieldPanel('location_image'),
        MultiFieldPanel([
            FieldPanel('phone'),
            FieldPanel('email'),
        ], heading="Contact Information"),
        FieldPanel('description'),
        MultiFieldPanel([
            FieldPanel('monday_hours'),
            FieldPanel('tuesday_hours'),
            FieldPanel('wednesday_hours'),
            FieldPanel('thursday_hours'),
            FieldPanel('friday_hours'),
            FieldPanel('saturday_hours'),
            FieldPanel('sunday_hours'),
        ], heading="Opening Hours", classname="collapsible"),
    ]

    # Constrain parent pages to only LocationsPage
    parent_page_types = ['home.LocationsPage']
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        # Sync with booking Location model when page is live
        if self.live:
            self.sync_to_booking_location()
    
    def sync_to_booking_location(self):
        """Create/update corresponding Location in booking app"""
        from booking.models import Location as BookingLocation
        
        if not self.location_name:
            return  # Need location name for booking location
            
        # Get or create booking location
        booking_location, created = BookingLocation.objects.get_or_create(
            location_page=self,
            defaults={
                'name': self.location_name,
                'address': self.address,
                'phone': self.phone,
                'email': self.email,
                'monday_hours': self.monday_hours,
                'tuesday_hours': self.tuesday_hours,
                'wednesday_hours': self.wednesday_hours,
                'thursday_hours': self.thursday_hours,
                'friday_hours': self.friday_hours,
                'saturday_hours': self.saturday_hours,
                'sunday_hours': self.sunday_hours,
            }
        )
        
        # Update fields if not created
        if not created:
            booking_location.name = self.location_name
            booking_location.address = self.address
            booking_location.phone = self.phone
            booking_location.email = self.email
            booking_location.monday_hours = self.monday_hours
            booking_location.tuesday_hours = self.tuesday_hours
            booking_location.wednesday_hours = self.wednesday_hours
            booking_location.thursday_hours = self.thursday_hours
            booking_location.friday_hours = self.friday_hours
            booking_location.saturday_hours = self.saturday_hours
            booking_location.sunday_hours = self.sunday_hours
            booking_location.save()
    
    def unpublish(self, *args, **kwargs):
        """Handle unpublishing of location page"""
        result = super().unpublish(*args, **kwargs)
        
        # Note: We don't delete booking location on unpublish since
        # it might be referenced by employees and bookings
        # Instead, we could add an is_active field if needed
            
        return result

    @property
    def display_name(self):
        """Primary display name for location"""
        return self.location_name or self.title
    
    def __str__(self):
        return self.display_name
    
    class Meta:
        verbose_name = "Location Page"
