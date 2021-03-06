from django.contrib.auth.models import AbstractUser
from django.db import models


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class User(AbstractUser):
    is_active = models.BooleanField(default=False)

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}" if self.first_name or self.last_name else 'Not provided'


class Specialization(BaseModel):
    name = models.CharField(max_length=100)


class StudentGroup(BaseModel):
    name = models.CharField(max_length=100)
    specialization = models.ForeignKey(Specialization, on_delete=models.CASCADE, related_name='studentgroups')


class Student(BaseModel):
    name = models.CharField(max_length=1000)
    telegram_nick = models.CharField(max_length=100)
    telegram_id = models.CharField(max_length=100)
    group = models.ForeignKey(StudentGroup, on_delete=models.CASCADE, related_name='students')


class Question(BaseModel):
    text = models.CharField(max_length=4000)
    lesson = models.PositiveSmallIntegerField()
    specialization = models.ForeignKey(Specialization, on_delete=models.CASCADE, related_name='questions')


class Option(BaseModel):
    text = models.CharField(max_length=4000)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='options')
    correct = models.BooleanField(default=False)


class Answer(BaseModel):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    option = models.ForeignKey(Option, on_delete=models.CASCADE, related_name='answers')
