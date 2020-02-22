from django.shortcuts import render, redirect
from django.contrib import messages

from .models import Classroom , Student
from .forms import ClassroomForm ,SignupForm, SigninForm ,ItemForm
from django.contrib.auth import login, authenticate, logout

def register(request):
    form = SignupForm()
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)

            user.set_password(user.password)
            user.save()

            login(request, user)
            return redirect("classroom-list")
    context = {
        "form": form,
    }
    return render(request, 'signup.html', context)

def user_login(request):
    form = SigninForm()
    if request.method == 'POST':
        form = SigninForm(request.POST)
        if form.is_valid():

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            auth_user = authenticate(username=username, password=password)
            if auth_user is not None:
                login(request, auth_user)
                return redirect("classroom-list")
    context = {
        "form":form
    }
    return render(request, 'signin.html', context)

def user_logout(request):
    logout(request)
    return redirect("signin")

def classroom_list(request):
    #classrooms = Classroom.objects.all()
    context = {
    "classrooms": Classroom.objects.all()
    }
    return render(request, 'classroom_list.html', context)



def classroom_detail(request, classroom_id):
    classroom = Classroom.objects.get(id=classroom_id)
    students = Student.objects.all().order_by("name" ,"exam_grade")
    context = {
        "classroom": classroom,
        "students": students,
    }
    return render(request, 'classroom_detail.html', context)

def student_create(request, classroom_id):
    classroom = Classroom.objects.get(id= classroom_id)

    if request.user.is_anonymous:
        return redirect('signin')
    if request.user != classroom.teacher:
        return redirect('classroom-detail', classroom_id)
    form = ItemForm()
    if request.method == "POST":
        form = ItemForm(request.POST)
        if form.is_valid():
            student = form.save(commit=False)
            student.classroom= classroom
            student.save()
            return redirect('classroom-detail', classroom_id)
    context = {
        "form":form,
        "classroom":classroom,

    }
    return render(request, 'student_create.html', context)

def student_update(request,classroom_id, student_id):
    student = Student.objects.get(id= student_id)
    form = ItemForm(instance=student)
    if request.user.is_anonymous:
        return redirect('signin')
    if request.user != student.classroom.teacher:
        return redirect('classroom-detail', student.classroom.id)
    if request.method == "POST":
        form = ItemForm(request.POST, instance=student)
        if form.is_valid():
            form.save()

            return redirect('classroom-detail', student.classroom.id)
    context = {
        "form": form,
        "student": student,

    }
    return render(request, 'student_update.html', context)

def student_delete(request, classroom_id, student_id):
    student=Student.objects.get(id=student_id)

    classroom =student.classroom
    if request.user == classroom.teacher:
        student.delete()

    messages.success(request, "Successfully Deleted!")
    return redirect('classroom-detail' , classroom.id)


def classroom_create(request):
    if request.user.is_anonymous:
        return redirect('signin')

    form = ClassroomForm()
    if request.method == "POST":
        form = ClassroomForm(request.POST, request.FILES or None)
        if form.is_valid():
            classroom = form.save(commit=False)
            classroom.teacher= request.user
            classroom.save()
            messages.success(request, "Successfully Created!")
            return redirect('classroom-list')
            print (form.errors)
    context = {
        "form": form,
    }
    return render(request, 'create_classroom.html', context)


def classroom_update(request, classroom_id):
    classroom = Classroom.objects.get(id=classroom_id)
    form = ClassroomForm(instance=classroom)
    if request.method == "POST":
        form = ClassroomForm(request.POST, instance=classroom)
    if form.is_valid():
        form.save()
        messages.success(request, "Successfully Edited!")
        return redirect('classroom-list')
        print (form.errors)
    context = {
    "form": form,
    "classroom": classroom,
    }
    return render(request, 'update_classroom.html', context)




def classroom_delete(request, classroom_id):
    Classroom.objects.get(id=classroom_id).delete()
    messages.success(request, "Successfully Deleted!")
    return redirect('classroom-list')
