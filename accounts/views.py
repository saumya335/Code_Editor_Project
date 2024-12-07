import subprocess
import tempfile
import json
import os
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import RegisterForm, LoginForm
from django.contrib.auth.models import User

# Home View
def home(request):
    return render(request, 'accounts/home.html')

# Login View
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "Login successful!")
                return redirect('login_success')
            else:
                messages.error(request, "Invalid credentials. Please try again.")
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})

# Register View
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.is_staff = form.cleaned_data['is_staff']  # Save staff status from form
            user.save()
            login(request, user)
            messages.success(request, "Registration successful. You are now logged in.")
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})

# Login Success View
def login_success_view(request):
    return render(request, 'accounts/login_success_view.html')

# About View
def about(request):
    return render(request, 'accounts/about.html')

# Contact View
def contact(request):
    return render(request, 'accounts/contact.html')

# Code Editor View
def codeEditor(request):
    return render(request, 'accounts/codeeditor.html')

# Code Editor API for real-time collaboration
@csrf_exempt
def code_editor_api(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            code = data.get('code', '')
            language = data.get('language', '')

            with tempfile.NamedTemporaryFile(delete=False, suffix=".tmp") as temp_code_file:
                temp_code_file.write(code.encode('utf-8'))
                temp_code_file.close()

                # Execute based on language
                if language == "python":
                    result = subprocess.run(
                        ['python3', temp_code_file.name],
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        text=True,
                        timeout=5
                    )
                elif language == "javascript":
                    result = subprocess.run(
                        ['node', temp_code_file.name],
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        text=True,
                        timeout=5
                    )
                elif language == "java":
                    compile_result = subprocess.run(
                        ['javac', temp_code_file.name],
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        text=True
                    )
                    if compile_result.returncode == 0:
                        result = subprocess.run(
                            ['java', temp_code_file.name.replace('.tmp', '')],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            text=True,
                            timeout=5
                        )
                    else:
                        os.unlink(temp_code_file.name)
                        return JsonResponse({'error': compile_result.stderr})
                else:
                    os.unlink(temp_code_file.name)
                    return JsonResponse({'error': 'Unsupported language selected.'})

                os.unlink(temp_code_file.name)

                if result.returncode == 0:
                    return JsonResponse({'output': result.stdout})
                else:
                    return JsonResponse({'error': result.stderr})

        except subprocess.TimeoutExpired:
            return JsonResponse({'error': 'Code execution timed out.'})
        except Exception as e:
            return JsonResponse({'error': str(e)})
    else:
        return JsonResponse({'error': 'Invalid request method.'})

# Profile View
class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context

# Logout View
def logout(request):
    return render(request, 'accounts/logout.html')

# My Projects View
def my_projects(request):
    return render(request, 'accounts/myprojects.html')

# Password Change View
def password_change(request):
    return render(request, 'accounts/password_change.html')

# Collaborate View
def collaborate_view(request):
    return render(request, 'accounts/collaborate.html')

# Fetch online users (from DB or cache)
def fetch_online_users(request):
    if request.method == "POST":
        status = request.POST.get('status')
        online_users = [user.username for user in User.objects.filter(is_active=True)]  # Example
        return JsonResponse(online_users, safe=False)
    return JsonResponse({'error': 'Invalid request method.'})

# Fetch users by online/offline status
@csrf_exempt
def fetch_users_by_status(request):
    # Get the status from the POST request
    status = request.POST.get('status')

    if status == 'online':
        # Placeholder logic for online users
        online_users = [user.username for user in User.objects.filter(is_active=True)]  # You can adjust this logic as needed
    elif status == 'offline':
        # Placeholder logic for offline users
        offline_users = [user.username for user in User.objects.filter(is_active=False)]
    else:
        return JsonResponse({'error': 'Invalid status.'})

    # Return the JSON response based on the status
    if status == 'online':
        return JsonResponse({'online_users': online_users}, safe=False)
    elif status == 'offline':
        return JsonResponse({'offline_users': offline_users}, safe=False)
