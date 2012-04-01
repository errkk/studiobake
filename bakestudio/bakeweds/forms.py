from django import forms
from bootstrap.forms import BootstrapForm, Fieldset
from models import Rating, BakeDay

class CommentForm(forms.ModelForm):
	# username = forms.CharField(max_length=100)
	# password = forms.CharField(widget=forms.PasswordInput(), max_length=100)

	class Meta:

		model = Rating
		fields = ['rating','comment']

		widgets = {
			'comment': forms.Textarea(attrs={'cols': 200, 'rows': 5, 'class':'span6'}),
		}

	

class LoginForm(forms.Form):
	username = forms.CharField(label='Username')
	password = forms.CharField(widget=forms.PasswordInput,label='Password')


class VolunteerForm(forms.ModelForm):


	class Meta:
		model = BakeDay
		fields = ['user']
	
