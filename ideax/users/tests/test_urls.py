from django.urls import reverse


class TestUsersUrls:
    namespace = 'users'

    def test_login(self):
        assert reverse(f'{self.namespace}:login') == '/accounts/login/'

    def test_logout(self):
        assert reverse(f'{self.namespace}:logout') == '/accounts/logout/'

    def test_sign_up(self):
        assert reverse(f'{self.namespace}:sign-up') == '/accounts/sign-up/'

    def test_profile(self):
        assert reverse(f'{self.namespace}:profile', args=['username']) == '/users/profile/username/'
