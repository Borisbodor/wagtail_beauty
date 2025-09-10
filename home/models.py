from django.db import models
from wagtail.models import Page
from wagtail.fields import RichTextField, StreamField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock


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


class HeroBlock(blocks.StructBlock):
    title = blocks.CharBlock(max_length=200, default="Welcome to Beauty Salon")
    subtitle = blocks.TextBlock(default="Transform your beauty with premium treatments")
    hero_image = ImageChooserBlock(required=False)
    background_image = ImageChooserBlock(required=False)
    primary_button_text = blocks.CharBlock(max_length=50, default="Book Now")
    primary_button_url = blocks.URLBlock(required=False)
    secondary_button_text = blocks.CharBlock(max_length=50, default="Services")
    secondary_button_url = blocks.URLBlock(required=False)
    
    class Meta:
        template = 'blocks/hero_block.html'
        icon = 'image'
        label = 'Hero'


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


class HomePage(Page):
    content = StreamField([
        ('hero', HeroBlock()),
        ('services', ServicesGridBlock()),
        ('features', FeaturesGridBlock()),
        ('cta', CallToActionBlock()),
        ('text', TextBlock()),
        ('gallery', ImageGalleryBlock()),
    ], blank=True, use_json_field=True)

    content_panels = Page.content_panels + [
        FieldPanel('content'),
    ]
