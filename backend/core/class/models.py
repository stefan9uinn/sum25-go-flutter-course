from django.db import models
from account.models import Profile 

class Classroom(models.Model):
    title = models.CharField(max_length = 200)
    description = models.TextField()
    teacher = models.ForeignKey(to = Profile, on_delete = models.CASCADE)


    def __str__(self) -> str:
        return self.title
