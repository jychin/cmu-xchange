from django import forms

from django.contrib.auth.models import User
from models import *
MAX_UPLOAD_SIZE= 250000000
class RegistrationForm(forms.Form):
    firstname = forms.CharField(max_length=20)
    lastname  = forms.CharField(max_length=20)
    username   = forms.CharField(max_length = 20)
    password1  = forms.CharField(max_length = 200, 
                                 label='Password', 
                                 widget = forms.PasswordInput())
    password2  = forms.CharField(max_length = 200, 
                                 label='Confirm password',  
                                 widget = forms.PasswordInput())


    # Customizes form validation for properties that apply to more
    # than one field.  Overrides the forms.Form.clean function.
    def clean(self):
        # Calls our parent (forms.Form) .clean function, gets a dictionary
        # of cleaned data as a result
        cleaned_data = super(RegistrationForm, self).clean()

        # Confirms that the two password fields match
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords did not match.")

        # We must return the cleaned data we got from our parent.
        return cleaned_data


    # Customizes form validation for the username field.
    def clean_username(self):
        # Confirms that the username is not already present in the
        # User model database.
        username = self.cleaned_data.get('username')
        if User.objects.filter(username__exact=username):
            raise forms.ValidationError("Username is already taken.")
        return username


class CreateForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ('profile_user', 'follower','content_type')
    def clean_photo(self):
        #print "lllllllllllll"
        photo = self.cleaned_data['photo']
        #print photo
        if not photo:
           return None
        if not photo.content_type or not photo.content_type.startswith('image'):
            raise forms.ValidationError('File type is not image')
        if photo.size > MAX_UPLOAD_SIZE:
            raise forms.ValidationError('File too big (max size is {0} bytes)'.format(MAX_UPLOAD_SIZE))
        return photo

"""
class EditForm(forms.ModelForm):
    class Meta:
        model = Profile
"""
