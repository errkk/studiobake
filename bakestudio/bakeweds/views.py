from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required, permission_required
from django.core.urlresolvers import reverse

from bakeweds.models import Product, BakeDay, Rating

from bakeweds.forms import CommentForm

from datetime import datetime




def index(request):

	today = datetime.now()

	next_bake_day = BakeDay.objects.filter(date__gt=today)[0]

	try:
		last_bake_day = BakeDay.objects.filter(date__lt=today)[0]
		recent_item = Product.objects.filter(BakeDay=last_bake_day)
	except IndexError:
		recent_item = None

	


	if request.method == 'POST':

		form = CommentForm(request.POST)
		
		if form.is_valid():
			
			
			pass
			
			
			# return HttpResponseRedirect(reverse('planner:week_view', args=[week_number]))

	else:

		form = CommentForm()


	return render( request,'index.html', { 
		'form' : form,
		'next_bake_day' : next_bake_day,
		'recent_item' : recent_item
		} )