from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _ # noqa
from django.views.generic import CreateView
from django.db.models import Count, Case, When

from .forms import SignUpForm
from ..ideax.models import Popular_Vote, Comment, Idea
from .models import UserProfile


@login_required
def profile(request, username):

    if request.user.username == username:
        votes = Popular_Vote.objects.filter(voter=request.user.id).values(
            'id').annotate(contador=Count(Case(When(like=True, then=1))))
        comments = Comment.objects.filter(author_id=request.user.id).values('raw_comment')
        filter_user = request.user
        query_ideas = request.user.userprofile.authors.filter(discarded=False)
    else:
        user = UserProfile.objects.filter(user__username=username)
        pk = user[0].id
        votes = Popular_Vote.objects.filter(voter=pk).values(
            'voter_id').annotate(contador=Count(Case(When(like=True, then=1))))
        comments = Comment.objects.filter(author_id=pk).values('raw_comment')
        filter_user = UserProfile.objects.filter(id=pk)[0].user
        query_ideas = UserProfile.objects.filter(id=pk)[0].user.userprofile.authors.filter(discarded=False)
    if not votes:
        getvotes = 0
    else:
        getvotes = votes[0]['contador']
    return render(
        request,
        'users/profile.html',
        {
            'userP': filter_user,
            'ideas': query_ideas,
            'popular_vote': getvotes,
            'comments': len(comments),
            'username': request.user.username,
        }
    )


@login_required
def who_innovates(request):
    data = dict()
    data['ideas'] = Idea.objects.values("author__user__username", "author__user__email", "author_id").annotate(
        qtd=Count('author_id')).annotate(
        count_dislike=Count(Case(When(popular_vote__like=False, then=1)))).annotate(
        count_like=Count(Case(When(popular_vote__like=True, then=1))))

    return render(request, 'users/who_innovates.html', data)


class SignUpView(CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('index')
    template_name = 'users/sign_up.html'

    def form_invalid(self, form):
        messages.error(self.request, _('Invalid form!'))
        return super().form_invalid(form)

    def form_valid(self, form):
        response = super().form_valid(form)
        username = form.cleaned_data.get('username')
        raw_password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=raw_password)
        login(self.request, user)
        return response
