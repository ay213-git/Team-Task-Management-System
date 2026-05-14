from django.shortcuts import render

# Create your views here.

# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import transaction
from .models import Task, User, Team
from .forms import TaskForm, TaskStatusForm, RegisterForm, TeamForm, ManagerTaskForm
from django.contrib.auth import login, logout


def home(request):
    if request.user.is_authenticated:
        return redirect('task_list')
    return render(request, 'home.html')

def logout_view(request):
    logout(request)
    return redirect("home")

@login_required
def task_list(request):
    tasks = Task.objects.filter(team=request.user.team)

    status_filter = request.GET.get('status', None)
    assigned_to_filter = request.GET.get('assigned_to', None)

    if status_filter:
        tasks = tasks.filter(status=status_filter)
    if assigned_to_filter:
        tasks = tasks.filter(assigned_to__username=assigned_to_filter)

    tasks_new = tasks.filter(status='new')
    tasks_in_progress = tasks.filter(status='in_progress')
    tasks_completed = tasks.filter(status='completed')

    return render(request, 'task_list.html', {
        'tasks': tasks,
        'tasks_new': tasks_new,
        'tasks_in_progress': tasks_in_progress,
        'tasks_completed': tasks_completed,
    })


@login_required
def add_task(request):
    if request.user.role != 'manager':
        return redirect('task_list')  # אם המשתמש לא מנהל, לא תתאפשר לו הגישה

    if request.method == 'POST':
        form = ManagerTaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.created_by = request.user
            task.team = request.user.team  # הצוות נבחר אוטומטית לפי הצוות של המנהל
            task.status = 'new'  # הסטטוס תמיד חדש
            task.assigned_to = None  # אין שיוך עובד בעת יצירה
            task.save()
            return redirect('task_list')
    else:
        form = ManagerTaskForm()

    return render(request, 'add_task.html', {'form': form})


@login_required
def change_task_status(request, task_id):
    task = get_object_or_404(Task, pk=task_id)

    if request.user.role != 'worker' or task.assigned_to != request.user or task.team != request.user.team:
        return redirect('task_list')  # אם המשתמש לא עובד או לא משוייך למשימה, לא תתאפשר לו הגישה

    if request.method == 'POST':
        form = TaskStatusForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskStatusForm(instance=task)

    return render(request, 'change_task_status.html', {'form': form, 'task': task})


def register(request):
    if request.user.is_authenticated:
        return redirect('task_list')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                user = form.save(commit=False)
                new_team_name = form.cleaned_data.get('new_team_name')
                selected_team = form.cleaned_data.get('team')

                if new_team_name:
                    team, _ = Team.objects.get_or_create(name=new_team_name)
                else:
                    team = selected_team

                user.team = team
                user.save()

            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            authenticated_user = authenticate(request, username=username, password=raw_password)
            if authenticated_user is not None:
                login(request, authenticated_user)
                return redirect('task_list')
    else:
        form = RegisterForm()

    return render(request, 'registration/register.html', {'form': form})


@login_required
def edit_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)

    # רק מנהל מהצוות של המשימה, ורק אם המשימה לא משוייכת לאף אחד
    if request.user.role != 'manager' or task.team != request.user.team or task.assigned_to is not None:
        return redirect('task_list')

    if request.method == 'POST':
        form = ManagerTaskForm(request.POST, instance=task)
        if form.is_valid():
            updated_task = form.save(commit=False)
            # ודא שהצוות נשאר הצוות של המנהל
            updated_task.team = request.user.team
            updated_task.status = 'new'  # הסטטוס חייב להיות חדש
            updated_task.assigned_to = None  # אין אפשרות לשייך עובד דרך עריכה
            updated_task.save()
            return redirect('task_list')
    else:
        form = ManagerTaskForm(instance=task)

    return render(request, 'edit_task.html', {'form': form, 'task': task})


@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)

    # רק מנהל מהצוות של המשימה, ורק אם המשימה לא משוייכת לאף אחד
    if request.user.role != 'manager' or task.team != request.user.team or task.assigned_to is not None:
        return redirect('task_list')

    if request.method == 'POST':
        task.delete()
        return redirect('task_list')

    # אם לא POST, החזר לרשימת המשימות
    return redirect('task_list')


@login_required
def assign_task(request, task_id):
    if request.method != 'POST':
        return redirect('task_list')
    task = get_object_or_404(Task, pk=task_id)
    user = request.user
    # רק עובד, מאותה קבוצה, ומשימה לא משוייכת
    if user.role != 'worker' or task.team != user.team or task.assigned_to is not None:
        return redirect('task_list')
    task.assigned_to = user
    task.status = 'in_progress'
    task.save()
    return redirect('task_list')


@login_required
def complete_task(request, task_id):
    if request.method != 'POST':
        return redirect('task_list')
    task = get_object_or_404(Task, pk=task_id)
    user = request.user
    # רק עובד, מאותה קבוצה, ומשימה משוייכת אליו
    if user.role != 'worker' or task.team != user.team or task.assigned_to != user:
        return redirect('task_list')
    task.status = 'completed'
    task.save()
    return redirect('task_list')

