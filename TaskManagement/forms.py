# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Task, User, Team

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'description', 'due_date', 'status', 'assigned_to', 'team']

class TaskStatusForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['status']


class ManagerTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'description', 'due_date']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'})
        }

    def clean_due_date(self):
        due_date = self.cleaned_data.get('due_date')
        from django.utils import timezone
        today = timezone.localdate()
        if due_date is None:
            return due_date
        if due_date <= today:
            raise forms.ValidationError('The due date must be later than today.')
        return due_date


class RegisterForm(UserCreationForm):
    new_team_name = forms.CharField(max_length=100, required=False, label='Create a new team')

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'team', 'new_team_name', 'role']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Allow registering without selecting an existing team when creating a new one
        self.fields['team'].required = False

    def clean(self):
        cleaned = super().clean()
        team = cleaned.get('team')
        new_team_name = (cleaned.get('new_team_name') or '').strip()

        if not team and not new_team_name:
            raise forms.ValidationError('Select an existing team or create a new team.')
        if team and new_team_name:
            raise forms.ValidationError('You must choose one option: an existing team or creating a new team, not both.')

        cleaned['new_team_name'] = new_team_name
        return cleaned


class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['name']
