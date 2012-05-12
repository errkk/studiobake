from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from django.conf import settings

from PIL import Image

import mimetypes
import os.path
import sys
import S3
import uuid




def is_accectable_file(filename):
	extension = filename.split('.')[-1]
	acceptable_filetypes = ['jpeg','jpeg','gif','png','jpg']
	if extension in acceptable_filetypes:
		return True
	else:
		return False


def put_s3( filename ):
	conn = S3.AWSAuthConnection(settings.AWS_ACCESS_KEY_ID, settings.AWS_SECRET_ACCESS_KEY)
	
	filedata = open(filename, 'rb').read()
	content_type = mimetypes.guess_type(filename)[0]
	
	if not content_type:
		content_type = 'text/plain'

	just_the_filename = 'thumbs/%s' % filename.split('/')[-1]

	return conn.put(settings.AWS_STORAGE_BUCKET_NAME, just_the_filename, S3.S3Object(filedata),
		{'x-amz-acl': 'public-read', 'Content-Type': content_type})

def remove_s3( filename ):
	conn = S3.AWSAuthConnection(settings.AWS_ACCESS_KEY_ID, settings.AWS_SECRET_ACCESS_KEY)
	
	just_the_filename = 'thumbs/%s' % filename.split('/')[-1]

	return conn.delete(settings.AWS_STORAGE_BUCKET_NAME, just_the_filename)




class Product(models.Model):
	description = models.CharField(max_length=500)
	thumbnail = models.ImageField(upload_to='thumbs')


	class Meta():
		verbose_name= 'Product'
		verbose_name_plural = 'Produce'

	def __unicode__(self):
		return self.description

	def get_absolute_url(self):
		return reverse('bakeweds:detail', args=(self.id,))


	def save(self, *args, **kwargs):
		
		if is_accectable_file(self.thumbnail.name):
		
			try:
				# remove old image from amazon
				old_instance = Product.objects.get(pk=self.id)
				if old_instance.thumbnail.path:
					remove_s3( str(old_instance.thumbnail.path ) )
			except:
				pass

			# Save this one
			super(Product, self).save(*args,**kwargs)
			
			# resize on file system
			size = 200, 200
			filename = str(self.thumbnail.path)
			image = Image.open(filename)
			image.thumbnail(size, Image.ANTIALIAS)			
			image.save(filename)
			
			# send to amazon and remove from local file system
			if put_s3(filename):
				os.remove(filename)
			else:
				return
			

			return True
		else:
			return False


	def prepare_delete(self):
		filename = str(self.thumbnail.path)
		remove_s3(filename)
		return

	def delete(self):
		self.prepare_delete()
		super(Product, self).delete()








class BakeDay(models.Model):
	date = models.DateField()
	product = models.OneToOneField(Product,blank=True,null=True)
	user = models.OneToOneField(User, unique_for_date='date')

	class Meta():
		verbose_name = 'Bake day'
		verbose_name_plural = 'Baking days'

	def __unicode__(self):
		string = ''
		
		if self.user:
			string += self.user.first_name
		
		if self.product and self.user:
			string += ' made a %s' % self.product.description

		if len(string) > 0:
			string += ' on '
		
		string += str(self.date)

		return string





class Rating(models.Model):
	user = models.ForeignKey(User)
	product = models.ForeignKey(Product)
	rating = models.IntegerField(max_length=1)
	comment = models.CharField(max_length=1000)




