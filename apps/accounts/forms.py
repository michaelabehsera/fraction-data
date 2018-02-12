from django import forms
from django.contrib.auth.forms import (ReadOnlyPasswordHashField,
                                       UserChangeForm as BaseUserChangeForm)
from django.utils.translation import ugettext as _
from django.contrib.auth import authenticate, password_validation
from django.contrib.auth.forms import SetPasswordForm


from .models import User


class SignUpForm(forms.ModelForm):
    error_messages = {
        'password_mismatch': _("The two password fields didn't match."),
    }

    # user fields
    email = forms.EmailField(
        label='Email Address',
        max_length=75,
        widget=forms.TextInput(attrs={'class': 'form-control m-input m-input--square', 'placeholder': 'Email Address'})
    )

    password1 = forms.CharField(
        max_length=50,
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control m-input m-input--square', 'placeholder': 'Password'})
    )

    password2 = forms.CharField(
        max_length=50,
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control m-input m-input--square', 'placeholder': 'Re-Enter Password'})
    )

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        if self._meta.model.USERNAME_FIELD in self.fields:
            self.fields[self._meta.model.USERNAME_FIELD].widget.attrs.update({'autofocus': True})

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def _post_clean(self):
        super()._post_clean()
        # Validate the password after self.instance is updated with form data
        # by super().
        password = self.cleaned_data.get('password2')
        if password:
            try:
                password_validation.validate_password(password, self.instance)
            except forms.ValidationError as error:
                self.add_error('password2', error)

    def save(self, commit=True):
        user = super(SignUpForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()

        return user


class LoginForm(forms.Form):
    """
    Base class for authenticating users. Extend this to get a form that accepts
    username/password logins.
    """
    username = forms.EmailField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control m-input', 'placeholder': 'Email', 'autofocus': True, 'autocomplete': 'off'}),
    )
    password = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control m-input', 'placeholder': 'Password'})
    )

    error_messages = {
        'invalid_login': _(
            "Please enter a correct %(email)s and password. Note that both "
            "fields may be case-sensitive."
        ),
        'inactive': _("This account is inactive."),
    }

    def __init__(self, request=None, *args, **kwargs):
        """
        The 'request' parameter is set for custom auth use by subclasses.
        The form data comes in via the standard 'data' kwarg.
        """
        self.request = request
        self.user_cache = None
        super(LoginForm, self).__init__(*args, **kwargs)

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username is not None and password:
            self.user_cache = authenticate(self.request, username=username, password=password)
            if self.user_cache is None:

                raise forms.ValidationError(
                    self.error_messages['invalid_login'],
                    code='invalid_login',
                    params={'email': 'Email Address'},
                )
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data

    def confirm_login_allowed(self, user):
        """
        Controls whether the given User may log in. This is a policy setting,
        independent of end-user authentication. This default behavior is to
        allow login by active users, and reject login by inactive users.

        If the given user cannot log in, this method should raise a
        ``forms.ValidationError``.

        If the given user may log in, this method should return None.
        """
        if not user.is_active:
            raise forms.ValidationError(
                self.error_messages['inactive'],
                code='inactive',
            )

    def get_user_id(self):
        if self.user_cache:
            return self.user_cache.id
        return None

    def get_user(self):
        return self.user_cache


class UserChangeForm(BaseUserChangeForm):
    email = forms.EmailField(label=_('Email'), max_length=75)
    password = ReadOnlyPasswordHashField(label=_('Password'),
                                         help_text=_('Raw passwords are not stored, so there is no way to see '
                                                     "this user's password, but you can change the password "
                                                     'using <a href="password/">this form</a>.'))


class UserCreationForm(forms.ModelForm):
    email = forms.EmailField(label=_('Email'), max_length=75)
    password1 = forms.CharField(label=_('Password'),
                                widget=forms.PasswordInput)
    password2 = forms.CharField(label=_('Password confirmation'),
                                widget=forms.PasswordInput,
                                help_text=_('Enter the same password as above, for verification.'))

    class Meta:
        model = User
        fields = ('email',)

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(_("The two password fields didn't match."))
        return password2

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class PasswordChangeForm(SetPasswordForm):
    """
    A form that lets a user change their password by entering their old
    password.
    """
    error_messages = dict(SetPasswordForm.error_messages, **{
        'password_incorrect': _("Your current password was entered incorrectly. Please enter it again."),
    })
    old_password = forms.CharField(
        label=_("Current password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autofocus': True}),
    )

    field_order = ['old_password', 'new_password1', 'new_password2']

    def clean_old_password(self):
        """
        Validates that the old_password field is correct.
        """
        old_password = self.cleaned_data["old_password"]
        if not self.user.check_password(old_password):
            raise forms.ValidationError(
                self.error_messages['password_incorrect'],
                code='password_incorrect',
            )
        return old_password

    def __init__(self, *args, **kwargs):
        super(PasswordChangeForm, self).__init__(*args, **kwargs)
        self.fields['old_password'].widget.attrs = {'class': 'form-control m-input m-input--square'}
        self.fields['new_password1'].widget.attrs = {'class': 'form-control m-input m-input--square'}
        self.fields['new_password2'].widget.attrs = {'class': 'form-control m-input m-input--square'}
        self.fields['new_password1'].help_text = ''
