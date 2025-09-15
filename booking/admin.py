from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet
from .models import FormSubmission


class FormSubmissionAdmin(SnippetViewSet):
    model = FormSubmission
    menu_label = 'Booking Submissions'
    menu_icon = 'calendar'
    list_display = ['customer_full_name', 'service', 'location', 'preferred_date', 'preferred_time', 'status', 'submitted_at']
    list_filter = ['status', 'location', 'preferred_date']
    search_fields = ['customer_first_name', 'customer_last_name', 'customer_email', 'customer_phone']
    ordering = ['-submitted_at']
    
    # Enable adding/editing
    add_to_admin_menu = True

# Register as snippet
register_snippet(FormSubmission, FormSubmissionAdmin)