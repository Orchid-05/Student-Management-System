from django.contrib import admin
from .models import Course, SubCourse, Enrollment, Testimonial, Student


# Register the Course model
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['name', 'instructor', 'created_at', 'end_date']
    search_fields = ['name', 'instructor']
    list_filter = ['created_at', 'instructor']

# Register the SubCourse model
@admin.register(SubCourse)
class SubCourseAdmin(admin.ModelAdmin):
    list_display = ['name', 'course', 'description']
    search_fields = ['name', 'course__name']
    list_filter = ['course']

# Register the Enrollment model
@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ['student', 'course', 'date_enrolled', 'is_active']
    search_fields = ['student__user__username', 'course__name']
    list_filter = ['is_active', 'date_enrolled', 'course']


# Register the Testimonial model
@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['name', 'designation', 'message', 'image']
    search_fields = ['name', 'designation']



