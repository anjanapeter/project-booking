from django.db import models

class Hall(models.Model):
    name = models.CharField(max_length=255)
    capacity = models.IntegerField()
    image = models.ImageField(upload_to='hall_images/', blank=True, null=True)
    is_booked = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Event(models.Model):
    department_name = models.CharField(max_length=100)
    event_name = models.CharField(max_length=100)
    num_students = models.IntegerField()
    event_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return self.event_name
        
class HallBookingRequest(models.Model):
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE)
    department_name = models.CharField(max_length=100)
    event_name = models.CharField(max_length=100)
    num_students = models.IntegerField()
    event_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    faculty_coordinator_name = models.CharField(max_length=100)
    faculty_coordinator_mobile = models.CharField(max_length=15)
    student_coordinator_name = models.CharField(max_length=100)
    student_coordinator_mobile = models.CharField(max_length=15)
    event_description = models.TextField()
    status = models.CharField(
        max_length=20, choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Canceled', 'Canceled')],
        default='Pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Request for {self.event_name} by {self.department_name}"
# from django.contrib.auth.models import AbstractUser

# class CustomUser(AbstractUser):
#     ROLE_CHOICES = [
#         ('admin', 'Admin'),
#         ('faculty', 'Faculty'),
#         ('student', 'Student'),
#     ]
#     role = models.CharField(max_length=10, choices=ROLE_CHOICES)


