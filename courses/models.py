from django.db import models
from account.models import Account
# Create your models here.
Language_choices=(
    ('eng', 'English'),
    ('Hindi', 'Hindi'),
)
Target_exam = [
    ('Engineering', (
            ('jee-mains', 'JEE-Main'),
            ('jee-Adv', 'JEE Advanced'),
            ('bits', 'Bits'),
        )
    ),
    ('Medical', (
            ('neet', 'NEET'),
            ('Aiims', 'AIIMS'),
        )
    ),
    ('other', 'Other'),
]

class Subject(models.Model):
    number = models.PositiveIntegerField(default='0')
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    target = models.CharField(max_length=20,choices=Target_exam,default='other')

    class Meta:
        ordering = ['number','title']

    def _str_(self):
        return self.title

class Course(models.Model):
    owner = models.ForeignKey(Account,related_name='courses_created',on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, related_name='courses',on_delete=models.CASCADE)
    target = models.CharField(max_length=20,choices=Target_exam,default='other')
    title = models.CharField(max_length=200)
    Language_choices = models.CharField(max_length=20,choices=Language_choices,default='English')
    slug = models.SlugField(max_length=200, unique=True)
    overview = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    students = models.ManyToManyField(Account,related_name='courses_joined',blank=True)

    def total_students_enrolled(self):
      return self.likes.count()

    class Meta:
        ordering = ['title']

    def _str_(self):
        return self.title
