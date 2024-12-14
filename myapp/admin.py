from django.contrib import admin
from myapp.models import Hall  # Correct relative import
from django.utils.html import format_html

@admin.register(Hall)
class HallAdmin(admin.ModelAdmin):
    list_display = ('name', 'capacity', 'is_booked', 'image_preview')  # Added 'image_preview' for thumbnail display
    list_filter = ('is_booked',)
    search_fields = ('name',)

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 50px; height: 50px;" />', obj.image.url)
        return "No Image"
    image_preview.short_description = 'Image Preview'
from .models import HallBookingRequest

@admin.register(HallBookingRequest)
class HallBookingRequestAdmin(admin.ModelAdmin):
    list_display = ('event_name', 'department_name', 'num_students', 'event_date', 'start_time', 'end_time', 'faculty_coordinator_name', 'faculty_coordinator_mobile', 'student_coordinator_name', 'student_coordinator_mobile', 'event_description', 'status', 'created_at')
    list_filter = ('status',)
    actions = ['approve_booking', 'cancel_booking']
    
    def approve_booking(self, request, queryset):
        queryset.update(status='Approved')
        for booking in queryset:
            booking.hall.is_booked = True  # Mark the hall as booked
            booking.hall.save()
        self.message_user(request, "Selected requests have been approved and halls booked.")
    
    def cancel_booking(self, request, queryset):
        queryset.update(status='Canceled')
        for booking in queryset:
            booking.hall.is_booked = False  # Mark the hall as available again
            booking.hall.save()
        self.message_user(request, "Selected requests have been canceled.")
# from django.contrib import admin
# from myapp.models import Hall  # Correct relative import

# @admin.register(Hall)
# class HallAdmin(admin.ModelAdmin):
#     list_display = ('name', 'capacity', 'is_booked')
#     list_filter = ('is_booked',)
#     search_fields = ('name',)
# Hall.objects.create(name="Hall A", capacity=100)
# Hall.objects.create(name="kaviprathiba", capacity=200)
# Hall.objects.create(name="Hall C", capacity=50)
# from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin
# from .models import CustomUser

# class CustomUserAdmin(UserAdmin):
#     # Fields to display in the admin panel user list
#     list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'is_staff')
    
#     # Fields to search in the admin panel
#     search_fields = ('username', 'email', 'role')
    
#     # Grouping fields for better layout in admin panel
#     fieldsets = (
#         (None, {'fields': ('username', 'password')}),
#         ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'role')}),
#         ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
#         ('Important dates', {'fields': ('last_login', 'date_joined')}),
#     )
    
#     # Fields to include when creating a new user in the admin panel
#     add_fieldsets = (
#         (None, {
#             'classes': ('wide',),
#             'fields': ('username', 'role', 'password1', 'password2'),
#         }),
#     )
    
#     # Enable filtering by role
#     list_filter = ('role', 'is_staff', 'is_superuser', 'is_active')

# # Register the CustomUser model with the custom admin
# admin.site.register(CustomUser, CustomUserAdmin)
# from django.contrib import admin
# from .models import Hall, Event, CustomUser
# from django.contrib.auth.admin import UserAdmin

# @admin.register(Hall)
# class HallAdmin(admin.ModelAdmin):
#     list_display = ('name', 'capacity')
#     Hall.objects.create(name="Hall A", capacity=100)
#     Hall.objects.create(name="kaviprathiba hall", capacity=200)
#     Hall.objects.create(name="Hall C", capacity=50)

# @admin.register(Event)
# class EventAdmin(admin.ModelAdmin):
#     list_display = ('department_name', 'event_name', 'num_students', 'event_date', 'start_time', 'end_time')

# @admin.register(CustomUser)
# class CustomUserAdmin(UserAdmin):
#     list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'is_staff')
