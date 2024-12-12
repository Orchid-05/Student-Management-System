from django.shortcuts import render,redirect
from .models import *

from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout



from django.contrib.auth.decorators import login_required

from django.views.decorators.cache import cache_control
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from .models import Course, Enrollment
from .forms import *
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .decorators import admin_required
from django.contrib.auth.forms import UserCreationForm  # Import UserCreationForm if not already imported

from django.contrib.auth import update_session_auth_hash




# Create your views here.

@login_required(login_url="/login/")
def enroll_course(request):
    # Check if the user is already enrolled in a course
    if Enrollment.objects.filter(student=request.user.student).exists():
        # If the user is already enrolled, redirect to home page
        messages.info(request, "You are already enrolled in a course.")
        return redirect('home')

    if request.method == "POST":
        # Get selected course ID from the form
        course_id = request.POST.get('course')
        if course_id:
            # Fetch the course and enroll the student
            course = Course.objects.get(id=course_id)
            
            # Create a new enrollment record
            Enrollment.objects.create(student=request.user.student, course=course)

            # Success message
            messages.success(request, f"You have successfully enrolled in {course.name}!")
            
            # Redirect to home page
            return redirect('home')
        else:
            messages.error(request, "Please select a course to enroll.")

    # Fetch available courses
    courses = Course.objects.all()
    return render(request, 'enrollment.html', {'courses': courses})


def mycourse(request):
    # If the user is not logged in
    if not request.user.is_authenticated:
        return render(request, 'mycourse.html', {
            'is_authenticated': False,  # Used to show "Choose a course" linking to login
            'user_has_course': False,
            'courses': [],
        })

    # If the user is logged in, get the corresponding Student instance
    try:
        student = request.user.student  # Assuming `Student` model has a one-to-one relationship with `User`
    except Student.DoesNotExist:
        return render(request, 'mycourse.html', {
            'is_authenticated': True,
            'user_has_course': False,
            'courses': [],
        })

    # Get all enrollments for this student
    enrollments = Enrollment.objects.filter(student=student)
    courses = [enrollment.course for enrollment in enrollments]

    # Pass data to the template
    return render(request, 'mycourse.html', {
        'is_authenticated': True,
        'user_has_course': bool(courses),
        'courses': courses,
    })

def delete_course_ajax(request, course_id):
    # Check if the course exists and belongs to the logged-in user
    enrollment = get_object_or_404(Enrollment, student=request.user, course_id=course_id)
    
    # Delete the course enrollment
    enrollment.delete()

    # Return a success response
    return JsonResponse({'success': True})

def home(request):
    testimonials = Testimonial.objects.all()  # Fetch all testimonials

    if request.user.is_authenticated:
        # If the user is an admin, redirect them to the admin dashboard
        if request.user.is_staff:  # Admin check
            return redirect('admin_dashboard')  # Redirect to the admin dashboard (ensure this URL is defined)
        
        elif hasattr(request.user, 'student'):  # If the user is a student
            # If you want to render the home page as the student dashboard
            return render(request, 'home.html', {'testimonials': testimonials})
        
        else:
            messages.error(request, "Profile not found.")  # Handle case where user doesn't have a profile
            return redirect('home')  # Redirect back to home

    # If the user is not logged in, just show the homepage with testimonials
    return render(request, 'home.html', {'testimonials': testimonials})

def about(request):
    return render(request, 'about.html')

def profile(request):
    return render(request, 'profile.html')

def contact(request):
    return render(request, 'contact.html')



def edit_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user.student)
        
        # Initialize a list to store messages
        update_messages = []

        # Handle username update separately if it's editable
        username = request.POST.get('username')
        if username and username != request.user.username:
            request.user.username = username    
            request.user.save()
            update_messages.append("Your username has been updated successfully.")

        # Handle gender update
        gender = request.POST.get('gender')
        if gender and gender != request.user.student.gender:
            request.user.student.gender = gender
            request.user.student.save()
            update_messages.append("Your gender has been updated successfully.")

        # Handle password change
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        if password and confirm_password:
            if password == confirm_password:
                # Set the new password
                request.user.set_password(password)
                request.user.save()

                # Re-authenticate the user to avoid logout after password change
                update_session_auth_hash(request, request.user)
                update_messages.append("Your password has been updated successfully.")
            else:
                messages.error(request, "The passwords do not match. Please try again.")
                return redirect('edit_profile')

        # Check if the form is valid before saving the profile data
        if form.is_valid():
            form.save()

            # Check if the profile picture was updated
            if 'profile_picture' in request.FILES:
                update_messages.append("Your profile picture has been updated successfully.")

            # If no specific updates, then a generic success message
            if not update_messages:
                update_messages.append("Your profile has been updated successfully.")

            # Display all the messages
            for msg in update_messages:
                messages.success(request, msg)

            return redirect('profile')  # Redirect to the profile page after saving
        else:
            messages.error(request, 'There was an error updating your profile.')

    else:
        # Populate the form with the current profile data
        form = ProfileForm(instance=request.user.student)
        form.fields['username'].initial = request.user.username  # Pre-fill the username field
    
    return render(request, 'edit_profile.html', {'form': form})

def about(request):
    return render(request, 'about.html')

def AllCourse(request):
    return render(request, 'AllCourse.html')

def assignment(request):
    return render(request, 'assignment.html')

def schedule(request):
    return render(request, 'schedule.html')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def login_page(request):
    
     if request.method=="POST":
         username=request.POST.get('username')
         password=request.POST.get('password')

        # Validate if username is empty
         if not username:
            messages.error(request, 'Username cannot be empty.')
            return redirect('/login/')

        # Validate if password is empty
         if not password:
            messages.error(request, 'Password cannot be empty.')
            return redirect('/login/')
         
        

         # Check if the username exists
         if not User.objects.filter(username=username).exists():
             messages.error(request,'Invalid username')
             return redirect('/login/')
         

         # Authenticate user
         user=authenticate(request, username=username, password=password)  #authenticate is a function in django that is used to check whether password and username is correct .
        
        # Check if authentication failed
         if user is None:
             messages.error(request,'Invalid password')
             return redirect('/login/')
         
        # Restrict superusers from accessing the frontend
         if user.is_superuser:
            messages.error(request, 'Superuser access is not allowed here.')
            return redirect('/login/')  # Redirect to admin page

         try:
            student_profile = Student.objects.get(user=user)  # Retrieve the student's profile
         except Student.DoesNotExist:
            messages.error(request, 'Student profile not found.')
            return redirect('/login/')
         
              
       # Redirect user based on role
         if student_profile.role == 'admin':  # Check if the role is 'admin'
            login(request, user)
            return redirect('/admin_dashboard/')  # Redirect admin to admin dashboard

         # Regular user
         login(request,user)      ##login method is used to maintain the session that is next time y loggedin it will recognize y.
         return redirect('/enroll/')
             
             
     return render(request,'login.html')

def register_page(request):
    
     if request.method=="POST":
         first_name=request.POST.get('first_name')
         last_name=request.POST.get('last_name')
         username=request.POST.get('username')
         email = request.POST.get('email')
         password=request.POST.get('password')

          # Validate required fields
         if not all([first_name, last_name, username, email, password]):
            messages.error(request, "All fields are required.")
            return redirect('/register/')
         
          # Validate email format
         try:
            validate_email(email)
         except ValidationError:
            messages.error(request, "Invalid email address.")
            return redirect('/register/')
         
         # Check if username or email already exists
         if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
            return redirect('/register/')
         if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return redirect('/register/')
         
         # Create the user with hashed password
         user= User.objects.create(
             first_name=first_name,
             last_name=last_name,
             username= username,
             email=email,
          )
         
         user.set_password(password)
         user.save()
         
         messages.info(request,'Account created.')
         
         return redirect('/login')
     return render(request,'register.html')





@admin_required
def admin_dashboard(request):
    total_users = User.objects.count()  # Total registered users
    total_students = User.objects.filter(student__role='student').count()  # Total students
    total_courses = Course.objects.count()  # Total number of courses
    total_enrollments = Enrollment.objects.count()  # Total number of enrollments

    # Prepare context for the template
    context = {
        'total_users': total_users,
        'total_students': total_students,
        'total_courses': total_courses,
        'total_enrollments': total_enrollments,
    }
    
    return render(request, 'admin_dashboard.html', context)


def manage_users(request):
    # Get all users
    users = User.objects.all()
    # Get only students
    students = Student.objects.filter(role='student')

    students = students.prefetch_related('enrollment_set')
    
    return render(request, 'manage_users.html', {'users': users, 'students': students})


def edit_user(request, user_id):
    user = get_object_or_404(User, id=user_id)  # Get the user by ID
    form = UserEditForm(instance=user)

    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=user)
        if form.is_valid():
            # Store the original values before saving
            original_username = user.username
            original_first_name = user.first_name
            original_last_name = user.last_name
            original_email = user.email
            original_password = user.password  # Store the original password

            # Save the form but don't save the password yet
            updated_user = form.save(commit=False)

            # Only update the password if it's provided (i.e., not empty)
            password_changed = False
            if form.cleaned_data.get('password'):  # Check if password is filled out
                updated_user.set_password(form.cleaned_data['password'])
                password_changed = True  # Mark password as changed

            # Save the updated user object (only after hashing the password)
            updated_user.save()

            # Check for changes and create a success message
            changes = []

            # Track changes for each field
            if original_username != updated_user.username:
                changes.append(f"Username changed from {original_username} to {updated_user.username}")
            if original_first_name != updated_user.first_name:
                changes.append(f"First name changed from {original_first_name} to {updated_user.first_name}")
            if original_last_name != updated_user.last_name:
                changes.append(f"Last name changed from {original_last_name} to {updated_user.last_name}")
            if original_email != updated_user.email:
                changes.append(f"Email changed from {original_email} to {updated_user.email}")
            if password_changed:
                changes.append("Password updated.")

            # Create a success message based on the changes
            if changes:
                message = ' | '.join(changes)  # Combine all changes in a single message
                messages.success(request, f"User updated successfully. {message}")
            else:
                messages.success(request, "No changes were made.")

            return redirect('manage_users')  # Redirect to the manage_users page

    return render(request, 'edit_user.html', {'form': form, 'user': user})

def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        # Delete the user
        user.delete()

        # Add a success message
        messages.success(request, f'User {user.username} has been deleted successfully.')

        # Redirect to the same page (e.g., manage_users page)
        return redirect('manage_users')

    return redirect('manage_users')

def admin_logout(request):
    logout(request)  # Log the admin out
    return redirect('login_page')  # Redirect to the login page after logout


def logout_page(request):
    logout(request)
    return redirect('/login/')

