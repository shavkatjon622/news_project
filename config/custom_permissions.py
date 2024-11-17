from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin



class OnlyLoggedSuperUser(LoginRequiredMixin, UserPassesTestMixin): # bu foydalanuvchi ro`yxatdan otmasdan profile kabi qismlarga kirsa uni login pagega jonatadi

    def test_func(self):
        return self.request.user.is_superuser