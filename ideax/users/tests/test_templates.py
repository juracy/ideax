from django.template import loader


class TestUserTemplates:
    def test_profile_no_idea(self, common_user):
        body = loader.render_to_string(
            'users/profile.html',
            {
                'userP': common_user,
                'ideas': [],
                'popular_vote': 0,
                'comments': 0,
                'username': 'someone',
            }
        )
        assert 'No ideas' in body

    def test_profile_no_idea_ptbr(self, common_user, set_pt_br_language):
        body = loader.render_to_string(
            'users/profile.html',
            {
                'userP': common_user,
                'ideas': [],
                'popular_vote': 0,
                'comments': 0,
                'username': 'someone',
            }
        )
        assert 'Nenhuma ideia' in body

    def test_profile_one_idea(self, common_user):
        body = loader.render_to_string(
            'users/profile.html',
            {
                'userP': common_user,
                'ideas': [1],
                'popular_vote': 0,
                'comments': 0,
                'username': 'someone',
            }
        )
        assert 'Author of one idea' in body

    def test_profile_one_idea_ptbr(self, common_user, set_pt_br_language):
        body = loader.render_to_string(
            'users/profile.html',
            {
                'userP': common_user,
                'ideas': [1],
                'popular_vote': 0,
                'comments': 0,
                'username': 'someone',
            }
        )
        assert 'Autor de uma ideia' in body

    def test_profile_several_ideas(self, common_user):
        body = loader.render_to_string(
            'users/profile.html',
            {
                'userP': common_user,
                'ideas': [1, 2],
                'popular_vote': 0,
                'comments': 0,
                'username': 'someone',
            }
        )
        assert 'Author of 2 ideas' in body

    def test_profile_user_data(self, common_user):
        body = loader.render_to_string(
            'users/profile.html',
            {
                'userP': common_user,
                'ideas': [],
                'popular_vote': 0,
                'comments': 0,
                'username': 'someone',
            }
        )

        assert 'common.idea@dtplabs.in' in body
        assert '<img class="gravatar"' in body

    def test_profile_user_data_noname(self, common_user):
        common_user.get_full_name = lambda: ''
        common_user.username = 'common-username'
        common_user.email = 'common-email'
        body = loader.render_to_string(
            'users/profile.html',
            {
                'userP': common_user,
                'ideas': [],
                'popular_vote': 0,
                'comments': 0,
                'username': 'someone',
            }
        )
        assert 'common-username' in body
        assert 'common-email' in body
