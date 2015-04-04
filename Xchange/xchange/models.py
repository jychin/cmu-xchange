from django.db import models
from django.utils.translation import gettext as _
from django.utils import timezone
import datetime
from django import forms

# Create your models here.
from django.contrib.auth.models import User

class XchangeUser(models.Model):
	user = models.OneToOneField(User, primary_key=True)
	age = models.IntegerField(default=0)
	bio = models.CharField(max_length=430)
	followlist = models.ManyToManyField("self", blank=True, null=True)
	# picture = models.FileField(upload_to="pictures", blank=True)
	picture = models.FileField(upload_to = 'pictures', default='pictures/xchange.png')
	content_type = models.CharField(max_length=50) 

class Item(models.Model):
	text = models.CharField(max_length=160)
	xchangeuser = models.ForeignKey(XchangeUser)
	itemphoto = models.FileField(upload_to = 'items')
	content_type = models.CharField(max_length=50)
	created = models.DateTimeField(auto_now_add=True)
	def __unicode__(self):
		return self.text
	def save(self, *args, **kwargs):
		if not self.id:
			self.created = datetime.datetime.today()
		return super(Item, self).save(*args, **kwargs)

class Comment(models.Model):
	xchangeuser = models.ForeignKey(XchangeUser)
	created = models.DateTimeField(auto_now_add=True)
	text = models.CharField(max_length=160)
	item = models.ForeignKey(Item)
	def __unicode__(self):
		return self.text
	def save(self, *args, **kwargs):
		if not self.id:
			self.created = datetime.datetime.today()
		return super(Comment, self).save(*args, **kwargs)

