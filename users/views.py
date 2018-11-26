from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm,UserUpdateForm,ProfileUpdateForm, LoginForm, TeacherRegisterForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import Group
from django.contrib.auth import login as auth_login
from .decorators import is_student, is_teacher
from django.contrib.auth import authenticate

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            # form.save()
            user = form.save(commit=False)
            student_group = Group.objects.get(name='students')
            user.save()
            student_group.user_set.add(user)
            print(form)
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your Account has been created! You are now able to login')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


def register_teacher(request):
    if request.method == 'POST':
        form = TeacherRegisterForm(request.POST)
        if form.is_valid():
            # form.save()
            user = form.save(commit=False)
            teacher_group = Group.objects.get(name='teachers')
            user.save()
            teacher_group.user_set.add(user)
            print(form)
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your Account has been created! You are now able to login')
            return redirect('login')
    else:
        form = TeacherRegisterForm()
    return render(request, 'users/register-teacher.html', {'form':form})

@login_required
@user_passes_test(is_student, login_url='/login/')
# @user_passes_test(lambda u: u.groups.filter(name='student').count() == 1, login_url='/login/')
def profile(request):
    print(request.user)
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST,instance=request.user)
        p_form = ProfileUpdateForm(request.POST,request.FILES,instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your Account has been Updated!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context ={
            'u_form':u_form,
            'p_form':p_form
    }
    return render(request,'users/profile.html',context)

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                if is_student(user):
                    return redirect('student_home')
                elif is_teacher(user):
                    return redirect('teacher_home')
    else:
        form = LoginForm()
    return render(request, "users/login.html", {'form':form})


def student_home(request):
    return render(request, 'users/student_home.html', {})

@user_passes_test(is_teacher, login_url='/login/')
def teacher_home(request):
    return render(request, 'users/teacher_home.html', {})

def register_home(request):
    return render(request, 'users/register_home.html' , {})
