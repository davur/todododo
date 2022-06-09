"""todododo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from tasks import views as tasks_views


urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', tasks_views.home, name='home'),
    # path('', tasks_views.TaskListView.as_view(), name='tasks'),
    path('', tasks_views.task_list, name='tasks/list'),
    path('tasks/new/', tasks_views.TaskCreateUpdateView.as_view(), name="tasks/new"),
    path('tasks/<pk>/', tasks_views.TaskCreateUpdateView.as_view(), name="tasks/task"),
]
