from django import forms
from bootstrap.forms import BootstrapForm, Fieldset
from models import Rating, BakeDay
from django.contrib.auth.models import User

class CommentForm(forms.ModelForm):

	class Meta:

		model = Rating
		fields = ['rating','comment']

		widgets = {
			'comment': forms.Textarea(attrs={'cols': 200, 'rows': 5, 'class':'span6'}),
		}

	

class LoginForm(forms.Form):
	username = forms.CharField(label='Username')
	password = forms.CharField(widget=forms.PasswordInput,label='Password')


class UserModelChoiceField(forms.ModelChoiceField):
    """
    Extend ModelChoiceField for users so that the choices are
    listed as 'first_name last_name (username)' instead of just
    'username'.

    """
    def label_from_instance(self, obj):
        return '%s %s' % ( obj.first_name, obj.last_name[:1] )

class VolunteerForm(forms.ModelForm):
	user = UserModelChoiceField(User.objects.all())
	class Meta:
		model = BakeDay
		fields = ['user']

	
	
