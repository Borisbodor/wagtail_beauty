from django.contrib import admin
from .models import Location, Service, Employee, FormSubmission


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'phone', 'email')
    search_fields = ('name', 'address')
    list_filter = ('created_at',)


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'duration_minutes', 'is_active', 'get_locations_list')
    list_filter = ('category', 'is_active', 'locations', 'created_at')
    search_fields = ('name', 'description')
    filter_horizontal = ('locations',)


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'location', 'email', 'phone', 'is_active', 'get_services_list')
    list_filter = ('location', 'is_active', 'services', 'created_at')
    search_fields = ('first_name', 'last_name', 'email')
    filter_horizontal = ('services',)


@admin.register(FormSubmission)
class FormSubmissionAdmin(admin.ModelAdmin):
    list_display = ('customer_full_name', 'service', 'location', 'preferred_date', 'preferred_time', 'status', 'get_employee_preference')
    list_filter = ('status', 'location', 'service', 'preferred_date', 'submitted_at')
    search_fields = ('customer_first_name', 'customer_last_name', 'customer_email', 'customer_phone')
    readonly_fields = ('submitted_at', 'updated_at')
    
    fieldsets = (
        ('Customer Information', {
            'fields': ('customer_first_name', 'customer_last_name', 'customer_email', 'customer_phone')
        }),
        ('Booking Details', {
            'fields': ('location', 'service', 'preferred_employee', 'preferred_date', 'preferred_time')
        }),
        ('Additional Information', {
            'fields': ('notes', 'status', 'staff_notes')
        }),
        ('Timestamps', {
            'fields': ('submitted_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )