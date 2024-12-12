from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import timedelta, date
from django.core.exceptions import ValidationError

# Create your models here.

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role_choices = (
        ('student', 'Student'),
        ('admin', 'Admin'),
        ('manager', 'Manager'),
    )
    role = models.CharField(max_length=10, choices=role_choices, default='student')
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    
    gender_choices = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('Nb', 'Non-binary'),
    )
    gender = models.CharField(max_length=2, choices=gender_choices, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s profile"
    
    def is_student(self):
        return self.role == 'student'

    def is_admin(self):
        return self.role == 'admin'

    def is_manager(self):
        # Managers are treated as admins, so return True for both 'admin' and 'manager' roles
        return self.role in ['admin', 'manager']



class Course(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    instructor = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    end_date = models.DateField(default=date.today)  # Default value set here
    image = models.ImageField(upload_to='course_images/', blank=True, null=True)  # New image field


    def clean(self):
        if self.end_date < date.today():
            raise ValidationError("End date cannot be in the past.")

    def __str__(self):
        return self.name

class SubCourse(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="sub_courses")  # Link to main course
    name = models.CharField(max_length=100)  # Name of the sub-course (module/lesson)
    description = models.TextField()  # Description of the sub-course
    content = models.TextField()  # Content of the sub-course (could be text, videos, assignments, etc.)
    
    def __str__(self):
        return f"{self.name} - {self.course.name}"

class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)  # Changed to reference Student
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date_enrolled = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['student', 'course'], name='unique_enrollment')
        ]  # Ensure unique enrollment per student and course

    def __str__(self):
        return f"{self.student.user.username} - {self.course.name}"


class Testimonial(models.Model):
    name = models.CharField(max_length=100)
    designation = models.CharField(max_length=100, blank=True, null=True)
    message = models.TextField()
    image = models.ImageField(upload_to='testimonials/', default='default.jpg')

    def __str__(self):
        return self.name
    

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    # Skip for superusers or users who already have a profile
    if instance.is_superuser:
        return

    if created:
        # Create a profile for newly created users
        student_profile, created = Student.objects.get_or_create(user=instance)
        student_profile.role = 'student'  # Assign 'student' role by default
        student_profile.save()
        print(f"Student profile created for {instance.username}")
    else:
        # Update existing profile if necessary
        if hasattr(instance, 'student'):
            instance.student.save()
            print(f"Student profile updated for {instance.username}")


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['user', 'gender']
    search_fields = ['user__username', 'role']
    list_filter = ['gender', 'role']
