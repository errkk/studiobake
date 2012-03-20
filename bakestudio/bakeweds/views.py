from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required, permission_required
from django.core.urlresolvers import reverse

from bakeweds.models import Product, BakeDay, Rating

def index(request):


	return render(request,'index.html')