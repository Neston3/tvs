from django import forms
from django.contrib.auth.models import User

from tvs.models import Volunteer, Users, UploadFileCvs


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']


# user more info form
class UserMoreInfo(forms.ModelForm):
    class Meta:
        model = Users
        fields = ['home_address', 'phone_number', 'role']
        widgets = {'role': forms.RadioSelect()}


# apply form fields
class CVUpload(forms.ModelForm):
    length = forms.IntegerField(label='Length (in months)', min_value=3, max_value=12)

    class Meta:
        model = Volunteer
        fields = ['full_name', 'contact', 'certificate', 'carrier'
            , 'experience', 'skills', 'why_volunteer', 'length']
        widgets = {'certificate': forms.RadioSelect()}
        required = 'length'


# validate csv file
def validate_file_extension(value):
    if not value.name.endswith('.csv'):
        raise forms.ValidationError("Only CSV file is accepted")


# manage, data upload
class UploadData(forms.ModelForm):
    uploadcvs = forms.FileField(label='Select a file', validators=[validate_file_extension])

    class Meta:
        model = UploadFileCvs
        fields = ['filename', 'year', 'uploadcvs']
        required = ['filename', 'uploadcvs']
