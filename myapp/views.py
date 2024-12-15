from django.shortcuts import render
from django.http import HttpResponse
from myapp.models import Hall
from myapp.models import Event

def event_form(request):
    if request.method == 'POST':
        department_name = request.POST['department_name']
        event_name = request.POST['event_name']
        num_students = int(request.POST['num_students'])
        event_date = request.POST['event_date']
        start_time = request.POST['start_time']
        end_time = request.POST['end_time']

        # Save event details
        event = Event.objects.create(
            department_name=department_name,
            event_name=event_name,
            num_students=num_students,
            event_date=event_date,
            start_time=start_time,
            end_time=end_time,
        )
        event.save()
         #Filter halls
        #available_halls = Hall.objects.filter(capacity__gte=num_students)
        available_halls = Hall.objects.filter(capacity__gte=num_students, is_booked=False)


        return render(request, 'hall_suggestions.html', {
            'event': event,
            'available_halls': available_halls,
        })
    return render(request, 'event_form.html')
    
from django.shortcuts import render, get_object_or_404, redirect

def hall_suggestions(request, event_name):
    available_halls = Hall.objects.filter(is_booked=False)
    return render(request, 'hall_suggestions.html', {
        'event': {'event_name': event_name},
        'available_halls': available_halls
    })

def book_hall(request, hall_id):
    hall = get_object_or_404(Hall, id=hall_id)
    hall.is_booked = True
    hall.save()
    return redirect('hall_suggestions', event_name='Your Event Name')


from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages

def login_view(request):
    if request.method == "POST":
        # Get form data
        user_role = request.POST.get("user_role")
        username = request.POST.get("username")
        password = request.POST.get("password")
        
        # Validate user authentication
        user = authenticate(request, username=username, password=password)
        # if user is not None:
            # Add role-based access (optional)
            # if user.groups.filter(name=user_role).exists():
            #     login(request, user)
            #     messages.success(request, f"Welcome {user_role.capitalize()}!")
                # Redirect based on role
        if user_role == "admin":
                    return redirect("admin_dashboard")
        elif user_role == "faculty":
                    return redirect("faculty_home")
        elif user_role == "student":
                    return redirect("student_dashboard")
        #     else:
        #         messages.error(request, "You do not have permission for this role.")
        # else:
        #     messages.error(request, "Invalid username or password.")
    return render(request, 'login.html')
def faculty_home(request):
    return render(request, 'faculty_home.html',{})
def calendar(request):
    return render(request, 'calendar.html',{})
from django.contrib import messages
from django.urls import reverse

def notifications(request):
    # Fetch all booking requests for the logged-in user (assuming a user relationship exists)
    booking_requests = HallBookingRequest.objects.all() # Adjust this to match your model's user reference
    
    notifications_list = []
    for booking in booking_requests:
        notifications_list.append({
            'message': f"Your booking request for {booking.event_name} on {booking.event_date} is {booking.status}.",
            'edit_url': reverse('edit_booking_request', args=[booking.id]) if booking.status == 'Pending' else None,
            'cancel_url': reverse('cancel_booking_request', args=[booking.id]) if booking.status == 'Pending' else None,
            'details_url': reverse('user_booking_details', args=[booking.id]),  # Link to details
        })
    
    return render(request, 'notification.html', {'notifications': notifications_list})


from django.shortcuts import render, redirect, get_object_or_404
from .models import Hall, HallBookingRequest
from django.contrib import messages

def request_hall_booking(request, hall_id):
    hall = get_object_or_404(Hall, id=hall_id)
    
    if request.method == 'POST':
        # Create a new booking request
        booking_request = HallBookingRequest(
            hall=hall,
            department_name=request.POST['department_name'],
            event_name=request.POST['event_name'],
            num_students=request.POST['num_students'],
            event_date=request.POST['event_date'],
            start_time=request.POST['start_time'],
            end_time=request.POST['end_time'],
            faculty_coordinator_name=request.POST['faculty_coordinator_name'],
            faculty_coordinator_mobile=request.POST['faculty_coordinator_mobile'],
            student_coordinator_name=request.POST['student_coordinator_name'],
            student_coordinator_mobile=request.POST['student_coordinator_mobile'],
            event_description=request.POST['event_description'],
        )
        booking_request.save()
        messages.success(request, 'Your booking request has been submitted and is pending approval.')
        return redirect('hall_suggestions', event_name=hall.name)  # Redirect back to hall suggestions or another page
    
    return render(request, 'book_hall_request.html', {'hall': hall})
from django.shortcuts import render, get_object_or_404
from .models import HallBookingRequest

def user_booking_details(request, request_id):
    booking_request = get_object_or_404(HallBookingRequest, id=request_id)
    return render(request, 'user_booking_details.html', {'booking_request': booking_request})

def edit_booking_request(request, request_id):
    booking_request = get_object_or_404(HallBookingRequest, id=request_id)

    if request.method == 'POST':
        # Update the booking request fields
        booking_request.department_name = request.POST['department_name']
        booking_request.event_name = request.POST['event_name']
        booking_request.num_students = request.POST['num_students']
        booking_request.event_date = request.POST['event_date']
        booking_request.start_time = request.POST['start_time']
        booking_request.end_time = request.POST['end_time']
        booking_request.faculty_coordinator_name = request.POST['faculty_coordinator_name']
        booking_request.faculty_coordinator_mobile = request.POST['faculty_coordinator_mobile']
        booking_request.student_coordinator_name = request.POST['student_coordinator_name']
        booking_request.student_coordinator_mobile = request.POST['student_coordinator_mobile']
        booking_request.event_description = request.POST['event_description']
        booking_request.save()

        messages.success(request, 'Your booking request has been updated.')
        return redirect('user_booking_details', request_id=booking_request.id)
    
    return render(request, 'edit_booking_request.html', {'booking_request': booking_request})
def cancel_booking_request(request, request_id):
    booking_request = get_object_or_404(HallBookingRequest, id=request_id)

    if booking_request.status == 'Pending':
        booking_request.status = 'Canceled'
        booking_request.hall.is_booked = False  # Make hall available again
        booking_request.hall.save()
        booking_request.save()
        messages.success(request, 'Your booking request has been canceled.')
    else:
        messages.error(request, 'Only pending requests can be canceled.')
    
    return redirect('user_booking_details', request_id=booking_request.id)    
from django.http import JsonResponse
from .models import HallBookingRequest

def calendar_events(request):
    year = int(request.GET.get('year', 0))
    month = int(request.GET.get('month', 0))
    bookings = HallBookingRequest.objects.filter(
        status='Approved',
        event_date__year=year,
        event_date__month=month
    )
    events = [
        {
            'title': f"{booking.event_name} ({booking.department_name})",
            'start': booking.event_date.isoformat(),
            'description': f"Hall: {booking.hall.name}, Time: {booking.start_time} - {booking.end_time}",
        }
        for booking in bookings
    ]
    return JsonResponse(events, safe=False)

from django.shortcuts import render
from django.http import JsonResponse
from .models import Hall

def calendar_view(request):
    """
    Render the calendar page.
    """
    return render(request, 'calendar_view.html', {})
def hall_suggestions_api(request):
    date = request.GET.get('date')
    
    if not date:
        return JsonResponse({'error': 'Invalid date'}, status=400)

    # Fetch halls already booked on the given date
    booked_halls = HallBookingRequest.objects.filter(
        event_date=date,
        status='Approved'
    ).values_list('hall_id', flat=True)

    # Fetch halls not booked on the given date
    available_halls = Hall.objects.exclude(id__in=booked_halls)

    halls_data = [{'id': hall.id, 'name': hall.name} for hall in available_halls]

    return JsonResponse({'halls': halls_data})

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import HallBookingRequest
from django.core.exceptions import ValidationError
from django.shortcuts import render
from .models import HallBookingRequest

def view_bookings(request):
    # Fetch all approved bookings and their associated hall data
    approved_bookings = HallBookingRequest.objects.filter(status='Approved').select_related('hall')
    
    # Pass the approved bookings to the template
    return render(request, 'view_bookings.html', {'approved_bookings': approved_bookings})


def upload_report(request, booking_id):
    booking = get_object_or_404(HallBookingRequest, id=booking_id)
    
    if request.method == 'POST' and request.FILES['report']:
        report = request.FILES['report']
        
        # Ensure the file is an image or PDF
        if not (report.content_type.startswith('image') or report.content_type == 'application/pdf'):
            return HttpResponse('Invalid file type. Please upload an image or PDF.', status=400)
        
        # Save the report to the booking
        booking.report_upload = report
        booking.save()
        
        return redirect('view_bookings')  # Redirect to the view bookings page after upload
    else:
        return HttpResponse('Invalid request', status=400)
from django.shortcuts import render, redirect
from django.http import Http404
from .models import HallBookingRequest

def delete_report(request, booking_id):
    try:
        booking = HallBookingRequest.objects.get(id=booking_id)
    except HallBookingRequest.DoesNotExist:
        raise Http404("Booking not found")

    # Delete the uploaded report if it exists
    if booking.report_upload:
        # Delete the file from the server
        booking.report_upload.delete()
        # Set the report_upload field to None (null)
        booking.report_upload = None
        booking.save()

    # Redirect to the view_bookings page after deletion
    return redirect('view_bookings')
