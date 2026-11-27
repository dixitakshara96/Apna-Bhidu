from django.db import models


class Students(models.Model):
    id = models.AutoField(primary_key=True)
    stud_name = models.CharField(max_length=100)

    # Student ka hashed password store hoga
    password = models.CharField(max_length = 128, null = True, blank = True)


class Mentors(models.Model):
    mentor_id = models.AutoField(primary_key=True)
    mentor_name = models.CharField(max_length=100)

    # Mentor ka hashed password store hoga
    password = models.CharField(max_length = 128, null = True, blank = True)


class Admin(models.Model):
    admin_id = models.AutoField(primary_key=True)
    admin_name = models.CharField(max_length=100)

    # Admin ka hashed password store hoga
    admin_pass = models.CharField(max_length = 128, null = True, blank = True)