from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.utils import timezone
from django.contrib.auth.models import User
import random
import datetime

# Create your models here.

"""
class OTP:
    def generate_otp(self):
        s = '0123456789'
        OTP = ''
        for i in range(4):
            OTP += s[random.randint(0,9)]

        print(OTP)
        return OTP
otp = OTP()
"""


def generate_otp():
    s = '0123456789'
    otp = ''
    for i in range(4):
        otp += s[random.randint(0, 9)]

    return otp


class People(models.Model):

    name = models.CharField(max_length=256)
    face_encoding = ArrayField(models.FloatField())
    voice = models.FileField(upload_to="people/static/people/voice", null=True,blank=True)
    email = models.EmailField(default="a@gmail.com",null=True,blank=True)
    profile_created = models.DateTimeField(blank=True, null=True)

    def create(self):
        self.profile_created = timezone.now()
        self.save()

    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birth_date = models.DateField(blank=True)


class Meeting(models.Model):
    employee = models.ForeignKey(User, on_delete=models.CASCADE)
    visitor = models.ForeignKey(People, on_delete=models.CASCADE, null=True, blank=True)
    purpose = models.CharField(default='', max_length=256)
    description = models.TextField(blank=True)
    code = models.CharField(max_length=4, default=generate_otp)
    start = models.DateTimeField(null=True)
    end = models.DateTimeField(null=True)
    arrived = models.BooleanField(default=False)

    def __str__(self):
        return str(self.pk)


class ReceptionistDisplayMessage(models.Model):
    meeting = models.ForeignKey(Meeting,on_delete=models.CASCADE,default=None)
    created_at = models.DateTimeField(null=True,default=datetime.datetime.now())
    read = models.BooleanField(default=False)

    def __str__(self):
        return str(self.pk)


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    visitor = models.ForeignKey(People, on_delete=models.CASCADE, null=True, blank=True)
    meeting = models.ForeignKey(Meeting, null=True, on_delete=models.CASCADE)
    message = models.TextField()
    read = models.BooleanField(default=False)


class Voice(models.Model):
    title = models.CharField(max_length=100)
    audio = models.FileField(upload_to='people/static/people')

    def __str__(self):
        return self.title