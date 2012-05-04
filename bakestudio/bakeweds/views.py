from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required, permission_required
from django.core.urlresolvers import reverse

from bakeweds.models import Product, BakeDay, Rating
from django.contrib.auth import authenticate, login, logout

from bakeweds.forms import CommentForm, LoginForm, VolunteerForm

from datetime import datetime, timedelta





def index(request):

	today = datetime.now()

	try:
		next_bake_day = BakeDay.objects.filter(date__gte=today).order_by('date')[0]
	except IndexError:
		next_bake_day = False


	past_bakes = BakeDay.objects.filter(date__lte=today).order_by('-date')[:7]
	
	try:
		last_bake_day = past_bakes[0]
		recent_item = last_bake_day.product
	except IndexError:
		recent_item = None
		last_bake_day = None

	try:
		comments = Rating.objects.filter( product = recent_item ).count()
	except:
		comments = 0

	
	return render( request,'index.html', { 
		'next_bake_day' : next_bake_day,
		'last_bake_day' : last_bake_day,
		'comments_count' : comments,
		'past_bakes'	: past_bakes
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


@login_required
def volunteer(request):
	today = datetime.now()
	future_bake_days = BakeDay.objects.filter(date__gt=today)

	if future_bake_days:
		instance = future_bake_days[0]
	else:
		instance = BakeDay()
		
		next_7days = [today.date() + timedelta(i) for i in xrange(7)]
		next_wed = [d for d in next_7days if 'Wed' in d.ctime()][0]
		
		instance.date = next_wed


	if request.method == 'POST':
		form = VolunteerForm(request.POST,instance=instance)

		if form.is_valid():
			if form.save():
				request.notifications.error( '%s Was assigned for %s' % ( instance.user.first_name, instance.date ) )

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
	
