from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from datetime import datetime, timedelta

from PIL import Image




def is_accectable_file(filename):
	extension = filename.split('.')[-1]
	acceptable_filetypes = ['jpeg','jpeg','gif','png']
	if extension in acceptable_filetypes:
		return True
	else:
		return False







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
			super(Product, self).save(*args,**kwargs)
			size = 200, 200
			filename = str(self.thumbnail.path)
			image = Image.open(filename)
			image.thumbnail(size, Image.ANTIALIAS)
			image.save(filename)
			return True
		else:
			return False








class BakeDay(models.Model):
	date = models.DateField()
	product = models.ForeignKey(Product,blank=True,null=True)
	user = models.ForeignKey(User, unique_for_date='date')

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




