from django import forms

class ContactForm(forms.Form):
	full_name = forms.CharField(label=(""),widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Full Name'}))
	email = forms.EmailField(label=(""),widget=forms.TextInput(attrs={'class':'form-control','placeholder':'E-Mail'}))
	content = forms.CharField(label=(""),widget=forms.Textarea(attrs={'class':'form-control','placeholder':'Content'}))

class LoginUser(forms.Form):
	username = forms.CharField(label=(""),widget=forms.TextInput(attrs={'class':'form-control','placeholder':'User Name'}))
	password = forms.CharField(label=(""),widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Password'}))

