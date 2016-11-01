from django.core.exceptions import ValidationError
from django.forms import ModelForm, CharField, inlineformset_factory, modelform_factory
from django.forms.models import ModelChoiceField
from django.forms.widgets import PasswordInput, EmailInput, DateTimeInput, TextInput

from my_site.models import User, Property, Meeting, Client, Owner


class UserForm(ModelForm):
    password_verify = CharField(widget=PasswordInput(attrs={'placeholder': 'Verify password'}), label="Verify password")

    class Meta:
        model = User
        fields = ["username", "email",
                  # "is_admin",
                  "password"]
        widgets = {
            'password': PasswordInput(attrs={'placeholder': 'Password'}),
            'email': EmailInput(attrs={'placeholder': 'Email'}),
            'username': TextInput(attrs={'placeholder': 'Username'}),
        }

    def clean_password_verify(self):
        if self.cleaned_data['password'] != self.cleaned_data['password_verify']:
            raise ValidationError("Passwords do not match")


propertyFormSet = inlineformset_factory(Owner, Property, exclude=(), extra=2)


class MeetingForm(ModelForm):
    property = type("MyModelChoiceField", (ModelChoiceField,),
                    {"label_from_instance": lambda self, p: (
                        "Country: " + p.country + ", town: " + p.town + ", address: " + p.address + ", type: " + p.get_type_display())})(
        queryset=Property.objects.all(),
        empty_label="Select property"
    )

    class Meta:
        model = Meeting
        exclude = ()


meetingFormSet = inlineformset_factory(Client, Meeting, form=MeetingForm,
                                       widgets={'date': DateTimeInput(attrs={'placeholder': 'Choose time'}), }, extra=2,
                                       can_delete=False)

clientForm = modelform_factory(model=Client, exclude=("user",),
                               widgets={
                                   'surname': TextInput(attrs={'placeholder': 'Surname'}),
                                   'name': TextInput(attrs={'placeholder': 'Name'}),
                                   'patronymic': TextInput(attrs={'placeholder': 'Patronymic'}),
                                   'phone': TextInput(attrs={'placeholder': 'Phone'}),
                               }, )


class OwnerForm(ModelForm):
    class Meta:
        model = Owner
        exclude = ("user",)

# class UForm(ModelForm):
#     password = CharField(widget=PasswordInput())
#     password_verify = CharField(widget=PasswordInput(), label="Verify password")
#
#     class Meta:
#         model = U
#         fields = ('username', 'email', 'password')
#
#     def clean_password_verify(self):
#         if self.cleaned_data['password'] != self.cleaned_data['password_verify']:
#             raise ValidationError("Passwords do not match")


# class UserProfileForm(ModelForm):
#     class Meta:
#         model = UserProfile
#         fields = ('website',)
