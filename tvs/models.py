from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


# Create your models here.

# used
class Volunteer(models.Model):
    username = models.CharField(max_length=10, null=False)
    full_name = models.CharField(max_length=50, null=False)
    location = models.CharField(max_length=10, null=False)
    contact = models.IntegerField(default=0)
    carrier = models.TextField()
    experience = models.TextField()
    skills = models.TextField()
    why_volunteer = models.TextField()
    status_update = models.IntegerField(default=0)
    length = models.PositiveIntegerField(default=3, validators=[MinValueValidator(3), MaxValueValidator(12)])
    # cv = models.FileField(upload_to="CVs/")
    CERT = (
        ('Certificate level', 'Certificate level'), ('Diploma level', 'Diploma level'), ('Degree level', 'Degree level')
        , ('Masters level', 'Masters level'))
    certificate = models.CharField(max_length=20, choices=CERT)


# used
class UploadFileCvs(models.Model):
    filename = models.CharField(max_length=50)
    year = models.IntegerField()
    uploadcvs = models.FileField(upload_to="documents/")

    # return file name of the csv file
    def __str__(self):
        return self.filename


# used
class ToChart(models.Model):
    region = models.CharField(max_length=20)
    enrolment = models.CharField(max_length=20)
    teacher = models.CharField(max_length=20)
    ptr = models.CharField(max_length=20)


# used
class Users(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    home_address = models.CharField(max_length=100, null=True)
    phone_number = models.IntegerField(default=0)
    POSITION = (('Student', 'Student'), ('Teacher', 'Teacher'))
    role = models.CharField(max_length=10, choices=POSITION)
