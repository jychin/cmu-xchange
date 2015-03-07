from django.db import models

# User class for built-in authentication module
from django.contrib.auth.models import User
# Import Datetime and timezone
from django.utils import timezone
import datetime
from django.utils.translation import gettext as _
from django import forms

class Profile(models.Model):
	profile_user = models.OneToOneField(User)

	age = models.IntegerField()

	photo = models.FileField(upload_to="pictures", blank=True)

	bio = models.CharField(max_length=430)
	follower = models.ManyToManyField("self")	
	content_type = models.CharField(max_length=50)

class Item(models.Model):
    text = models.CharField(max_length=160)
    user = models.ForeignKey(Profile)
    time = models.DateTimeField(auto_now_add = True)
    def __unicode__(self):
        return self.text
    def save(self, *args, **kwargs):
		if not self.id:
			self.time = datetime.datetime.today()
		return super(Item, self).save(*args, **kwargs)


class Comment(models.Model):
	user = models.ForeignKey(Profile)
	item = models.ForeignKey(Item)
	comment = models.CharField(max_length=430)
	time = models.DateTimeField(auto_now_add = True)
	def __unicode__(self):
		return self.text
	def save(self, *args, **kwargs):
		if not self.id:
			self.time = datetime.datetime.today()
		return super(Comment,self).save(*args, **kwargs)
