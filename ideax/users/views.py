from django.contrib import messages
from django.contrib.auth import authenticate, views as auth_views
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.views.generic import CreateView
from django.db.models import Count, Case, When
from django.db import connection
from .forms import SignUpForm
from .utils import set_connection
from ..ideax.models import Popular_Vote, Comment


@login_required
def profile(request):
    votes = Popular_Vote.objects.filter(voter=request.user.id).values(
        'voter_id').annotate(contador=Count(Case(When(like=True, then=1))))
    comments = Comment.objects.filter(author_id=request.user.id).values('raw_comment')
    return render(
        request,
        'users/profile.html',
        {
            'user': request.user,
            'ideas': request.user.userprofile.authors.all(),
            'popular_vote': votes[0]['contador'],
            'comments': len(comments),
        }
    )


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

def login(request):
    if request.method == "POST":
        email = request.POST.get('username', '')
        hostname = email.split('@')[1]
        set_connection(request, hostname)
        request.session['client'] = request.tenant.domain_url
    return auth_views.login(request)