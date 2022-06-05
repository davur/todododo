from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import re

from django.db import models
from django.db.models import F, Q



class TaskManager(models.Manager):

    def get_today_list(self):
        today = datetime.today()
        return Task.objects.filter(archived=False).filter(Q(due_date__lte=today, completed=False) | Q(completed_on=today)).order_by('due_date')


    def get_next_list(self):
        today = datetime.today()
        next_7 = today + relativedelta(days=7)
        return Task.objects.filter(archived=False).filter(due_date__gt=today, due_date__lte=next_7, completed=False)

    def get_other_list(self):
        today = datetime.today()
        next_7 = today + relativedelta(days=7)
        return Task.objects.exclude(completed_on=today).filter(archived=False).filter(Q(completed=True) | Q(due_date__isnull=True) | Q(due_date__gt=next_7)).order_by('completed', F('due_date').asc(nulls_last=True))


# Create your models here.
class Task(models.Model):
    objects = TaskManager()

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    due_date = models.DateField(blank=True, null=True)

    completed = models.BooleanField()
    completed_on = models.DateField(blank=True, null=True)

    archived = models.BooleanField(default=False)

    repeat = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.description

    def calculate_next_due_date(self):

        if not self.repeat:
            return None

        method, amount, unit = str(self.repeat).split(" ")

        amount = int(amount)

        # every N days|weeks|months
        # new_due_date = N unit after due_date
        if method == "every" and self.due_date:
            start_date = datetime.strptime(str(self.due_date), "%Y-%m-%d")
        else: # if after == "after":
            start_date = datetime.today()

        if unit[0] == "d":
            new_due_date = start_date + relativedelta(days=amount)
        elif unit[0] == "w":
            new_due_date = start_date + relativedelta(weeks=amount)
        elif unit[0] == "m":
            new_due_date = start_date + relativedelta(months=amount)
        else: # if unit[0] == "y":
            new_due_date = start_date + relativedelta(years=amount)

        return new_due_date


    def save(self, *args, **kwargs):
        repeat = str(self.repeat).lower()
        x = re.compile('^(every|after) [0-9]+ (day|week|month|year)s?$', re.IGNORECASE)

        # TODO Let's do error handling later
        if not x.match(repeat):
            repeat = ""

        self.repeat = repeat

        orig = None

        if self.pk:
            orig = Task.objects.get(pk=self.pk)


        if self.completed and (not orig or not orig.completed):
            self.completed_on = datetime.today()

            if self.due_date and self.repeat:
                new_due_date = self.calculate_next_due_date()

                rep = Task.objects.create(
                        title=self.title,
                        description=self.description,
                        completed=False,
                        due_date=new_due_date.strftime("%Y-%m-%d") if new_due_date else None,
                        repeat=self.repeat)
                rep.save()

        super(Task, self).save(*args, **kwargs)

