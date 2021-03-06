from __future__ import unicode_literals

import os

from django.contrib import admin
from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
from MajorProject1 import settings


class CustomUser(AbstractUser):
    mobile = models.CharField(max_length=15)
    is_student = models.BooleanField(verbose_name="Student", default=False)
    is_verified = models.BooleanField(verbose_name="verified", default=False)


class Parent(models.Model):
    user = models.OneToOneField(CustomUser, null=True)
    mother_name = models.CharField(max_length=128)
    father_name = models.CharField(max_length=128)
    mobile = models.CharField(max_length=15, null=True)
    email = models.CharField(max_length=128, null=True)
    is_registered = models.BooleanField(default=False)

    def __unicode__(self):
        return self.father_name

    class Meta:
        unique_together = ('mother_name', 'father_name', 'mobile')


class Branch(models.Model):
    code = models.CharField(max_length=2, unique=True)
    name = models.CharField(max_length=64)

    def __unicode__(self):
        return self.name


class Student(models.Model):
    user = models.OneToOneField(CustomUser, null=True)
    parent = models.ForeignKey(Parent)
    branch = models.ForeignKey(Branch)
    name = models.CharField(max_length=128)
    hall_ticket = models.CharField(max_length=10, unique=True)
    gender = models.CharField(max_length=6)
    mobile = models.CharField(max_length=15, null=True)
    email = models.CharField(max_length=128, null=True)
    is_registered = models.BooleanField(default=False)
    cgpa = models.CharField(max_length=10, default='0')

    def __unicode__(self):
        return self.hall_ticket


# class Faculty(models.Model):
#     user = models.OneToOneField(CustomUser, null=True)
#     name = models.CharField(max_length=128)
#     roll_no = models.CharField(max_length=10, unique=True)
#     gender = models.CharField(max_length=6)
#     mobile = models.CharField(max_length=15)
#     email = models.CharField(max_length=128, null=True)
#     branch = models.ForeignKey(Branch)
#     is_registered = models.BooleanField(default=False)


class Subject(models.Model):
    subject_code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=128)
    max_internal_marks = models.IntegerField(null=True)
    max_external_marks = models.IntegerField(null=True)

    def __unicode__(self):
        return self.name


class ExamInfo(models.Model):
    student = models.ForeignKey(Student, related_name='examinfo')
    year_of_pursue_roman = models.CharField(max_length=5)
    semester_roman = models.CharField(max_length=2)
    year_of_pursue = models.IntegerField()
    semester = models.IntegerField()
    year_of_calendar = models.IntegerField()
    month_of_year = models.CharField(max_length=15)
    supple = models.BooleanField()
    total = models.CharField(max_length=5, default='0')

    def __unicode__(self):
        if self.supple == False:
            desc = ' Main'
        else:
            desc = ' Supple'
        return self.year_of_pursue_roman+" "+self.semester_roman+desc

    class Meta:
        ordering = ['year_of_pursue', 'semester']


class Result(models.Model):
    subject = models.ForeignKey(Subject, related_name='subjects')
    examinfo = models.ForeignKey(ExamInfo, related_name='result')
    internal_marks = models.CharField(max_length=3)
    external_marks = models.CharField(max_length=3)
    total = models.CharField(max_length=3)
    results = models.CharField(max_length=5)
    credits = models.IntegerField()

    def __unicode__(self):
        return self.subject.name



class AchievementInASemester(models.Model):
    rank = models.IntegerField()
    student = models.ForeignKey(Student, related_name='achievementinasemester')
    examinfo = models.ForeignKey(ExamInfo, related_name='examinfo')

    def __unicode__(self):
        return self.student.hall_ticket+" "+self.examinfo.year_of_pursue_roman+" "+self.examinfo.semester_roman+" "+str(self.rank)


class AchievementInASubject(models.Model):
    rank = models.IntegerField()
    student = models.ForeignKey(Student, related_name='ach_subject')
    result = models.ForeignKey(Result, related_name='ach_res')
    year_of_pursue_roman = models.CharField(max_length=5)
    semester_roman = models.CharField(max_length=2)
    semester = models.IntegerField()
    year_of_pursue = models.IntegerField()

    def __unicode__(self):
        return self.student.hall_ticket+" "+self.result.subject.name+" "+str(self.rank)


class SaltForActivation(models.Model):
    user = models.OneToOneField(CustomUser)
    # salt = models.CharField(max_length=10)

    def __unicode__(self):
        return self.user.username

class Document(models.Model):
    docfile = models.FileField()

    def delete(self, using=None, keep_parents=False):
        os.remove(os.path.join(settings.MEDIA_ROOT, self.docfile.name))
        return super(Document, self).delete(using, keep_parents)


admin.site.register(Parent)
admin.site.register(ExamInfo)
admin.site.register(Subject)
admin.site.register(AchievementInASubject)
admin.site.register(AchievementInASemester)
admin.site.register(Result)
# admin.site.unregister(Group)