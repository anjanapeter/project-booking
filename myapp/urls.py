from django.urls import path
from myapp import views


urlpatterns = [
    path('', views.login_view, name='login'),
    path('event_form/', views.event_form, name='event_form'),
    path('faculty_home/', views.faculty_home, name='faculty_home'),
    path('calendar/', views.calendar, name='calendar'),
    path('notifications/', views.notifications, name='notifications'),
    path('hall_suggestions/<str:event_name>/', views.hall_suggestions, name='hall_suggestions'),
    path('book_hall/<int:hall_id>/', views.request_hall_booking, name='request_hall_booking'),
    path('user_booking_details/<int:request_id>/', views.user_booking_details, name='user_booking_details'),
    path('edit_request/<int:request_id>/', views.edit_booking_request, name='edit_booking_request'),
    path('cancel_request/<int:request_id>/', views.cancel_booking_request, name='cancel_booking_request'),
    path('api/calendar-events/', views.calendar_events, name='calendar_events'),
    path('calendar_view/', views.calendar_view, name='calendar_view'),
    path('api/hall_suggestions/', views.hall_suggestions_api, name='hall_suggestions_api'),
    path('view_bookings/', views.view_bookings, name='view_bookings'),
    path('upload_report/<int:booking_id>/', views.upload_report, name='upload_report'),
    path('delete_report/<int:booking_id>/', views.delete_report, name='delete_report'),
]
