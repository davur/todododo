from datetime import datetime
from dateutil.relativedelta import relativedelta

from django.shortcuts import render
from django.views.generic import UpdateView, ListView


from .models import *



class CreateUpdateView(UpdateView):

    def get_object(self, queryset=None):
        try:
            return super().get_object(queryset)
        except AttributeError:
            return None



class TaskCreateUpdateView(CreateUpdateView):
    model = Task

    # specify the fields
    fields = [
        "completed",
        "title",
        "description",
        "due_date",
        "repeat",
        "archived",
    ]

    success_url ="/"

    def get_context_data(self, *args, **kwargs):
        context = super(TaskCreateUpdateView, self).get_context_data(*args, **kwargs)

        context['today_list'] = Task.objects.get_today_list()
        context['next_list'] = Task.objects.get_next_list()
        context['other_list'] = Task.objects.get_other_list()

        return context

class TaskListView(ListView):
    model = Task


def task_list(request):

    object_list = Task.objects.all().order_by('completed', F('due_date').asc(nulls_last=True))

    today_list = Task.objects.get_today_list()
    next_list = Task.objects.get_next_list()
    other_list = Task.objects.get_other_list()


    con = {
        'today_list': today_list,
        'next_list': next_list,
        'other_list': other_list,
        'object_list': object_list,
    }
    return render(request, template_name="tasks/task_list.html", context=con)


# Create your views here.

def home(request):
    con = {
        "object_list": Task.objects.all()
    }
    return render(request, template_name="tasks/home.html", context=con)


