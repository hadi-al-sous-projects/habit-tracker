from datetime import timedelta

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.decorators.http import require_POST
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from .forms import TaskForm
from .models import FocusSession, Task


def format_minutes(total):
    hours, minutes = divmod(total, 60)
    if hours:
        return f'{hours} س {minutes} د'
    return f'{minutes} د'


@login_required
def dashboard(request):
    tasks = Task.objects.filter(user=request.user)
    sessions = FocusSession.objects.filter(user=request.user)

    total = tasks.count()
    done = tasks.filter(status='done').count()
    percent = round(done / total * 100) if total else 0
    deep = tasks.filter(task_type='deep').count()
    shallow = tasks.filter(task_type='shallow').count()

    now = timezone.localtime()
    start_today = now.replace(hour=0, minute=0, second=0, microsecond=0)
    start_week = start_today - timedelta(days=6)
    today_minutes = sessions.filter(started_at__gte=start_today).aggregate(
        total=Sum('minutes'))['total'] or 0
    week_minutes = sessions.filter(started_at__gte=start_week).aggregate(
        total=Sum('minutes'))['total'] or 0

    recent = []
    for s in sessions.select_related('task')[:5]:
        recent.append({'session': s, 'duration': format_minutes(s.minutes)})
    return render(request, 'tasks/dashboard.html', {
        'total': total,
        'done': done,
        'percent': percent,
        'deep': deep,
        'shallow': shallow,
        'today_text': format_minutes(today_minutes),
        'week_text': format_minutes(week_minutes),
        'recent_sessions': recent,
    })


class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    paginate_by = 10

    def get_queryset(self):
        qs = Task.objects.filter(user=self.request.user)
        q = self.request.GET.get('q', '').strip()
        task_type = self.request.GET.get('type', '')
        priority = self.request.GET.get('priority', '')
        status = self.request.GET.get('status', '')
        if q:
            qs = qs.filter(title__icontains=q)
        if task_type in dict(Task.TYPE_CHOICES):
            qs = qs.filter(task_type=task_type)
        if priority in dict(Task.PRIORITY_CHOICES):
            qs = qs.filter(priority=priority)
        if status in dict(Task.STATUS_CHOICES):
            qs = qs.filter(status=status)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        get = self.request.GET
        context['current_q'] = get.get('q', '')
        context['current_type'] = get.get('type', '')
        context['current_priority'] = get.get('priority', '')
        context['current_status'] = get.get('status', '')
        context['type_choices'] = Task.TYPE_CHOICES
        context['priority_choices'] = Task.PRIORITY_CHOICES
        context['status_choices'] = Task.STATUS_CHOICES
        params = get.copy()
        params.pop('page', None)
        context['querystring'] = params.urlencode()
        return context


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy('task_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, 'تمت إضافة المهمة')
        return super().form_valid(form)


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy('task_list')

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, 'تم تعديل المهمة')
        return super().form_valid(form)


class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    success_url = reverse_lazy('task_list')

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, 'تم حذف المهمة')
        return super().form_valid(form)


@login_required
def focus_start(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    return render(request, 'tasks/focus_start.html', {'task': task})


@login_required
@require_POST
def focus_save(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    try:
        minutes = int(request.POST.get('minutes', ''))
    except (TypeError, ValueError):
        minutes = None
    if minutes is None or not 1 <= minutes <= 240:
        messages.error(request, 'حدث خطأ: مدة الجلسة غير صالحة ولم تُحفظ')
        return redirect('focus_start', pk=task.pk)
    FocusSession.objects.create(
        user=request.user,
        task=task,
        minutes=minutes,
        started_at=timezone.now() - timedelta(minutes=minutes),
    )
    messages.success(request, 'تم حفظ جلسة التركيز')
    return redirect('session_list')
class SessionListView(LoginRequiredMixin, ListView):
    model = FocusSession
    template_name = 'tasks/session_list.html'
    paginate_by = 10

    def get_queryset(self):
        return FocusSession.objects.filter(user=self.request.user).select_related('task')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        rows = []
        for s in context['object_list']:
            rows.append({'session': s, 'duration': format_minutes(s.minutes)})
        context['rows'] = rows
        params = self.request.GET.copy()
        params.pop('page', None)
        context['querystring'] = params.urlencode()
        return context