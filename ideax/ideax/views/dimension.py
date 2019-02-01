from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.translation import ugettext_lazy as _ # noqa

from ...util import get_client_ip, audit
from ..forms import DimensionForm
from ..models import Dimension


class DimensionHelper:
    @classmethod
    def get_dimension_list(cls):
        return {'dimension_list': Dimension.objects.all()}


@login_required
@permission_required('ideax.add_dimension', raise_exception=True)
def dimension_new(request):
    if request.method == "POST":
        form = DimensionForm(request.POST)
        if form.is_valid():
            dimension = form.save()
            dimension.save()
            messages.success(request, _('Dimension saved successfully!'))
            audit(request.user.username, get_client_ip(request), 'CREATE_DIMENSION', Dimension.__name__, dimension.id)
            return redirect('dimension_list')
    else:
        form = DimensionForm()
    return render(request, 'ideax/dimension_new.html', {'form': form})


@login_required
def dimension_list(request):
    audit(request.user.username, get_client_ip(request), 'DIMENSION_LIST', Dimension.__name__, '')
    return render(request, 'ideax/dimension_list.html', DimensionHelper.get_dimension_list())


@login_required
@permission_required('ideax.change_dimension', raise_exception=True)
def dimension_edit(request, pk):
    dimension = get_object_or_404(Dimension, pk=pk)
    if request.method == "POST":
        form = DimensionForm(request.POST, instance=dimension)
        if form.is_valid():
            form.save()
            messages.success(request, _('Dimension changed successfully!'))
            audit(
                request.user.username,
                get_client_ip(request),
                'EDIT_DIMENSION_SAVE',
                Dimension.__name__,
                str(dimension.id)
            )
            return redirect('dimension_list')
    else:
        form = DimensionForm(instance=dimension)

    return render(request, 'ideax/dimension_edit.html', {'form': form})


@login_required
@permission_required('ideax.delete_dimension', raise_exception=True)
def dimension_remove(request, pk):
    dimension = get_object_or_404(Dimension, pk=pk)
    dimension.delete()
    messages.success(request, _('Dimension removed successfully!'))
    audit(request.user.username, get_client_ip(request), 'REMOVE_DIMENSION', Dimension.__name__, str(pk))
    return redirect('dimension_list')
