from django.db import models

# Create your models here.
class Students(models.Model):
    id = models.AutoField(primary_key = True)
    stud_name = models.CharField(max_length = 100)

class Mentors(models.Model):
    mentor_id = models.AutoField(primary_key = True)
    mentor_name = models.CharField(max_length = 100)

