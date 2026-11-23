from django.urls import path

from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('tasks/', views.TaskListView.as_view(), name='task_list'),
    path('tasks/new/', views.TaskCreateView.as_view(), name='task_create'),
    path('tasks/<int:pk>/edit/', views.TaskUpdateView.as_view(), name='task_update'),
    path('tasks/<int:pk>/delete/', views.TaskDeleteView.as_view(), name='task_delete'),
    path('tasks/<int:pk>/focus/', views.focus_start, name='focus_start'),
    path('tasks/<int:pk>/focus/save/', views.focus_save, name='focus_save'),
    path('sessions/', views.SessionListView.as_view(), name='session_list'),
]
