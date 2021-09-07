from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from ..decorators import is_helpdesk_staff


class MustBeStaffMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return is_helpdesk_staff(self.request.user)
