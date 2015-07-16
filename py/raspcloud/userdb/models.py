from django.db import models

# Create your models here.
class userinfo(models.Model):
	username = models.CharField(max_length = 30)
	password = models.CharField(max_length = 30)

	def __unicode__(self):
		return 'Name:'+self.username+'\nPasswd:'+self.password

class fileshared(models.Model):
	filename = models.CharField(max_length = 64)
	path = models.CharField(max_length = 128)
	user = models.CharField(max_length = 30)

	def __unicode__(self):
		return 'Filename:'+self.filename+'\nPath:'+self.path+'\nUser:'+self.user

class chatroomitem(models.Model):
	content = models.CharField(max_length = 1024)
	user = models.CharField(max_length = 30)
	time = models.CharField(max_length = 30)

	def __unicode__(self):
		return 'Content:'+self.content+'\nUser:'+self.user+'\nTime:'+self.time+'\n'