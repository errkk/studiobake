from django import forms
from bootstrap.forms import BootstrapForm, Fieldset

class CommentForm(BootstrapForm):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput(), max_length=100)

    class Meta:
        layout = (
            Fieldset("Please Login", "username", "password", ),
        )

        widgets = {
			'username': forms.Textarea(attrs={'cols': 80, 'rows': 20, 'class':'wysihtml5'}),
		}

    

