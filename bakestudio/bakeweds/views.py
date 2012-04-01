from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required, permission_required
from django.core.urlresolvers import reverse

from bakeweds.models import Product, BakeDay, Rating
from django.contrib.auth import authenticate, login, logout

from bakeweds.forms import CommentForm, LoginForm, VolunteerForm

from datetime import datetime





def index(request):

	

	today = datetime.now()

	try:
		next_bake_day = BakeDay.objects.filter(date__gt=today)[0]
	except IndexError:
		next_bake_day = False

	try:
		last_bake_day = BakeDay.objects.filter(date__lte=today)[0]
		recent_item = Product.objects.filter(bakeday=last_bake_day)[0]
	except IndexError:
		recent_item = None

	try:
		comments = Rating.objects.filter( product = recent_item ).count()
	except:
		comments = 0

	
	return render( request,'index.html', { 
		'next_bake_day' : next_bake_day,
		'last_bake_day' : last_bake_day,
		'recent_item' : recent_item,
		'comments_count' : comments
		} )





@login_required
def detail(request,id):

	product = Product.objects.get(pk=id)


	if request.method == 'POST':
		form = CommentForm(request.POST)



		if form.is_valid():

			existing = Rating.objects.filter(comment__contains=form.cleaned_data['comment'], product = product, user = request.user )
			if bool(existing):
				request.notifications.error('Think you already wrote that')
			else:
				rating = Rating()

				rating.user = request.user
				rating.product = product
				rating.rating = form.cleaned_data['rating']
				rating.comment = form.cleaned_data['comment']

				if rating.save():
					request.notifications.error('Comment saved')
					return HttpResponseRedirect( reverse('bakeweds:detail', args=[product.id]) )
			
		else:
			pass
	else:
		form = CommentForm()



	try:
		comments = Rating.objects.filter( product = product )
	except:
		comments = False

	if product is not None:
		pass

	return render( request,'detail.html', { 
		'form' : form,
		'product' : product,
		'comments' : comments
		} )

def DeleteComment(request,id):
	comment = Rating.objects.get(pk=id)

	if comment.delete():
		request.notifications.error('Comment deleted')

	return HttpResponseRedirect( reverse('bakeweds:detail', args=[comment.product.id]) )


def volunteer(request):
	
	instance = BakeDay.objects.all()[0]

	if request.method == 'POST':
		form = VolunteerForm(request.POST,instance=instance)

		if form.is_valid():
			pass

	else:
		form = VolunteerForm(instance=instance)

	return render(request,'volunteer.html', {
		'form':form
		})	






'''
Login
____________________________________________________________________________________________
'''	
@csrf_protect
def Login(request):
	
	# Submitted Form
	if request.method == 'POST':
		# Bound To POST
		form = LoginForm(request.POST)

		if form.is_valid():
			# No Errors process form
			username = request.POST['username']
			password = request.POST['password']
			next = request.GET['next'] if 'next' in request.GET else '/'

			user = authenticate(username=username, password=password)
			
			if user is not None:
				if user.is_active:
					login(request, user)
					# Redirect to a success page.
					return HttpResponseRedirect(next)

				else:
					# Return a 'disabled account' error message
					request.notifications.error('Disabled account')
			else:
				request.notifications.error('Your username password combination was incorrect')
				# Return an 'invalid login' error message.

	else:
		# Unbound Form
		form = LoginForm()

	
	return render(request,'login.html', {
		'form':form
		})
	
	
def Logout(request):
	logout(request)
	return HttpResponseRedirect('/')
	
