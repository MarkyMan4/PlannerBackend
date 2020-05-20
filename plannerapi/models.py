from django.db import models
from django.contrib.auth.models import User


class Project(models.Model):
    name = models.CharField(max_length=80)
    description = models.CharField(max_length=4000, default='')
    start_date = models.DateField()
    end_date = models.DateField()
    active = models.BooleanField(default=True)

class PeopleOnProject(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    percent_allocated = models.IntegerField()

    class Meta:
        unique_together = ('user', 'project')
        index_together = ('user', 'project')
