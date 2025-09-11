from django import template
from booking.forms import BookingForm

register = template.Library()


@register.simple_tag(takes_context=True)
def get_booking_form(context):
    if 'form' in context:
        return context['form']
    
    if 'page' in context and hasattr(context['page'], '_form'):
        return context['page']._form
        
    return BookingForm()
