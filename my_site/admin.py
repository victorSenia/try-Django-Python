from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.models import Group

from my_site.models import Client, User, Property, Meeting, Owner


class PropertyInline(admin.TabularInline):
    model = Property
    extra = 0


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email',)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'is_active', 'is_admin')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    list_display = ('username', 'email', 'is_admin', 'is_active')
    list_filter = ['is_admin', 'is_active']
    search_fields = ['username', 'email', ]
    # list_editable = ('email',)
    list_per_page = 20
    # exclude = ("password", "last_login")
    # readonly_fields = ("password",)
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('email',)}),
        ('Permissions', {'fields': ('is_admin', 'is_active',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2')}
         ),
    )
    filter_horizontal = ()


class MeetingInline(admin.TabularInline):
    model = Meeting
    extra = 0


class ClientAdmin(admin.ModelAdmin):
    list_display = ('surname', 'name', 'patronymic', 'phone',)
    inlines = [MeetingInline, ]


class OwnerAdmin(admin.ModelAdmin):
    list_display = ("user",)
    inlines = [PropertyInline, ]


admin.site.unregister(Group)
admin.site.register(User, UserAdmin)
admin.site.register(Client, ClientAdmin)
admin.site.register(Owner, OwnerAdmin)
