from django.core.exceptions import ValidationError
from django.forms import ModelForm, CharField, inlineformset_factory, modelform_factory
from django.forms.widgets import PasswordInput, EmailInput, DateTimeInput, TextInput

from my_site.models import User, Property, Meeting, Client


class UserForm(ModelForm):
    password_verify = CharField(widget=PasswordInput(attrs={'placeholder': 'Verify password'}), label="Verify password")

    class Meta:
        model = User

        fields = '__all__'
        widgets = {
            'password': PasswordInput(attrs={'placeholder': 'Password'}),
            'email': EmailInput(attrs={'placeholder': 'Email'}),
            'username': TextInput(attrs={'placeholder': 'Username'}),
        }

    def clean_password_verify(self):
        if self.cleaned_data['password'] != self.cleaned_data['password_verify']:
            raise ValidationError("Passwords do not match")


propertyFormSet = inlineformset_factory(User, Property, exclude=(), extra=2)
meetingFormSet = inlineformset_factory(Client, Meeting, exclude=(), widgets={
    'date': DateTimeInput(attrs={'placeholder': 'Choose time'}), },
                                       extra=2)

clientForm = modelform_factory(Client,
                               fields="__all__",
                               widgets={
                                   'surname': TextInput(attrs={'placeholder': 'Surname'}),
                                   'name': TextInput(attrs={'placeholder': 'Name'}),
                                   'patronymic': TextInput(attrs={'placeholder': 'Patronymic'}),
                                   'phone': TextInput(attrs={'placeholder': 'Phone'}),
                               }, )
