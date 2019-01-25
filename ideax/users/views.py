from django.contrib import messages
from django.contrib.auth import authenticate, views as auth_views
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.views.generic import CreateView
from django.db.models import Count, Case, When
from django.db import connection
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from tenant_schemas.utils import get_tenant_model
from .forms import SignUpForm, AuthConfigurationForm
from .utils import set_connection
from ..ideax.models import Popular_Vote, Comment, Idea
from .models import UserProfile, AuthConfiguration



@login_required
def profile(request, pk):
    if pk == 0:
        votes = Popular_Vote.objects.filter(voter=request.user.id).values(
            'voter_id').annotate(contador=Count(Case(When(like=True, then=1))))
        comments = Comment.objects.filter(author_id=request.user.id).values('raw_comment')
        filter_user = request.user
        query_ideas = request.user.userprofile.authors.all()
    else:
        votes = Popular_Vote.objects.filter(voter=pk).values(
            'voter_id').annotate(contador=Count(Case(When(like=True, then=1))))
        comments = Comment.objects.filter(author_id=pk).values('raw_comment')
        filter_user = UserProfile.objects.filter(id=pk)[0].user
        query_ideas = UserProfile.objects.filter(id=pk)[0].user.userprofile.authors.all()
    if not votes:
        getvotes = 0
    else:
        getvotes = votes[0]['contador']
    return render(
        request,
        'users/profile.html',
        {
            'user': filter_user,
            'ideas': query_ideas,
            'popular_vote': getvotes,
            'comments': len(comments),
            'username': request.user,
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

def login(request):
    if request.method == "POST":
        email = request.POST.get('username', '')
        try:
            validate_email(email)
            hostname = email.split('@')[1]
            TenantModel = get_tenant_model()
            set_connection(request, hostname)
        except ValidationError as error:
            messages.error(request, error.message)
            return redirect('users:login')
        except TenantModel.DoesNotExist:
            messages.error(request, _('Tenant not found'))
            return redirect('users:login')
        except AssertionError:
            messages.error(request, _('Invalid tenant model'))
            return redirect('users:login')

        request.session['client'] = request.tenant.domain_url
    return auth_views.login(request)


def check_authconfiguration(request):
    if request.user.is_superuser:
        if AuthConfiguration.objects.filter(active=True):
            pass
        else:
            return redirect('users:set-configuration')
        
            
@login_required
def set_authconfiguration(request, new=False):
    if request.method == "POST":
        form = AuthConfigurationForm(request.POST)
    else:
        form = AuthConfigurationForm()

    # AUDIT
    return save_authconfiguration(request, form, 'configuration/configuration_new.html', True)


def save_authconfiguration(request, form, template_name, new=False):
    if request.method == "POST":
        if form.is_valid():
            auth_configuration = form.save(commit=False)
            auth_configuration.active = True
            auth_configuration.save()
            messages.success(request, _('Configuration saved successfully!'))

            if new:
                return redirect('use_term_new')
            return redirect('idea_list')

    return render(request, template_name, {'form': form})
