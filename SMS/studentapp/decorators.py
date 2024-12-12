from django.http import HttpResponseForbidden
from studentapp.models import Student

def admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden("You are not allowed to access this page.")
        
        try:
            student = Student.objects.get(user=request.user)  # Get the associated student object
            if not student.is_admin():
                return HttpResponseForbidden("You are not allowed to access this page.")  # Not an admin
        except Student.DoesNotExist:
            return HttpResponseForbidden("You are not allowed to access this page.")  # No student profile found
        
        return view_func(request, *args, **kwargs)
    return wrapper
