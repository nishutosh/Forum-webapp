from django.db import models
from django.contrib.auth.models import User
class userextend(models.Model):
  euser=models.OneToOneField(User)
  description=models.TextField(blank=True)

class questions(models.Model):
  user=models.ForeignKey(User ,default=None)
  header=models.CharField(max_length=60)
  body=models.TextField()
  ucode=models.TextField(blank=True)
  reply=models.IntegerField(default=0)
  views=models.IntegerField(default=0)
  dateqtime=models.DateTimeField()
  slug=models.SlugField(null=True,blank=True,max_length=95)
  updated=models.BooleanField(default=False)
  
class answer(models.Model):
  question=models.ForeignKey(questions)
  userans=models.ForeignKey(User)
  answer=models.TextField()
  acode=models.TextField(blank=True)
  datentime=models.DateTimeField()
  class Meta:
     ordering=["datentime"]
 
# Create your models here.
