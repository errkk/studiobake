from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from datetime import datetime, timedelta



class Product(models.Model):
	description = models.CharField(max_length=500)


	class Meta():
		verbose_name= 'Product'
		verbose_name_plural = 'Produce'


class BakeDay(models.Model):
	date = models.DateField()
	product = models.ForeignKey(Product,blank=True,null=True)
	user = models.ForeignKey(User, unique_for_date='date')

	class Meta():
		verbose_name = 'Bake day'
		verbose_name_plural = 'Baking days'


class Rating(models.Model):
	user = models.ForeignKey(User)
	product = models.ForeignKey(Product)
	rating = models.IntegerField(max_length=1)
	comment = models.CharField(max_length=1000)