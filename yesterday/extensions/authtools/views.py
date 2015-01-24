# Subclassing Authtools views
# https://github.com/fusionbox/django-authtools/blob/master/authtools/views.py

from __future__ import absolute_import

from authtools.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView, \
    PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView


class ExtLoginView(LoginView):
    template_name = 'accounts/login.html'

login = ExtLoginView.as_view()


class ExtLogoutView(LogoutView):
    template_name = 'accounts/logout.html'

logout = ExtLogoutView.as_view()


class ExtPasswordChangeView(PasswordChangeView):
    template_name = 'accounts/password_change.html'

    def get_success_url(self):
        from django.contrib.auth import update_session_auth_hash
        # https://docs.djangoproject.com/en/1.7/topics/auth/default/#session-invalidation-on-password-change

        update_session_auth_hash(self.request, self.request.user)
        return super(ExtPasswordChangeView, self).get_success_url()

password_change = ExtPasswordChangeView.as_view()


class ExtPasswordChangeDoneView(PasswordChangeDoneView):
    template_name = 'accounts/password_change_done.html'

password_change_done = ExtPasswordChangeDoneView.as_view()


class ExtPasswordResetView(PasswordResetView):
    template_name = 'accounts/password_reset.html'
    subject_template_name = 'accounts/password_reset_subject.txt'
    email_template_name = 'accounts/password_reset_email.html'

password_reset = ExtPasswordResetView.as_view()


class ExtPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'accounts/password_reset_done.html'

password_reset_done = ExtPasswordResetDoneView.as_view()


class ExtPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'accounts/password_reset_confirm.html'

password_reset_confirm = ExtPasswordResetConfirmView.as_view()
password_reset_confirm_uidb36 = ExtPasswordResetConfirmView.as_view()


class ExtPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'accounts/password_reset_complete.html'

password_reset_complete = ExtPasswordResetCompleteView.as_view()
