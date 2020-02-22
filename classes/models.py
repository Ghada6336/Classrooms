from django.db import models

from django.urls import reverse
from django.contrib.auth.models import User

class Classroom(models.Model):
    subject = models.CharField(max_length=120)
    grade = models.IntegerField()
    year = models.IntegerField()
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse('classroom-detail', kwargs={'classroom_id':self.id})

    def __str__(self):
        return self.subject

class Student(models.Model):
    name = models.CharField(max_length=120)
    dob= models.DateField()
    exam_grade = models.DecimalField(max_digits=10, decimal_places=3)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE ,related_name="students")
    GENDER=(('f', 'female'),
    ('m', 'male'))


    gender = models.CharField(
        max_length=2,
        choices=GENDER
        )
    def __str__(self):
        return self.name
