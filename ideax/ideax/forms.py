import os

from PIL import Image
from django import forms
from django.utils.translation import ugettext_lazy as _ # noqa
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.conf import settings
from tinymce import TinyMCE
from martor.fields import MartorFormField

from .models import Idea, Criterion, Category, Challenge, Use_Term, Category_Image, Dimension


class IdeaForm(forms.ModelForm):
    challenge = forms.ModelChoiceField(
        queryset=Challenge.objects.filter(discarted=False),
        empty_label=_('Not related to any challenge'),
        required=False,
        label=_('Challenge')
    )
    oportunity = MartorFormField(label=_('Oportunity'), max_length=Idea._meta.get_field('oportunity').max_length)
    solution = MartorFormField(label=_('Solution'), max_length=Idea._meta.get_field('solution').max_length)
    target = MartorFormField(label=_('Target'), max_length=Idea._meta.get_field('target').max_length)
    summary = MartorFormField(label=_('Summary'), max_length=Idea._meta.get_field('summary').max_length)

    def __init__(self, *args, **kwargs):
        queryset = kwargs.pop('authors', None)
        super(IdeaForm, self).__init__(*args, **kwargs)
        self.fields['authors'] = forms.ModelMultipleChoiceField(
            queryset=queryset,
            widget=FilteredSelectMultiple("", is_stacked=False),
            required=False,
            label=_('Coauthors')
        )

    class Meta:
        model = Idea
        fields = ('title', 'summary', 'oportunity', 'solution', 'target', 'category', 'challenge', 'authors')
        labels = {'title': _('Title'), 'category': _('Category')}

    class Media:
        css = {
            'all': (os.path.join(settings.BASE_DIR, '/static/admin/css/widgets.css')),
        }
        js = ('/admin/jsi18n', 'jquery.js', 'jquery.init.js', 'core.js', 'SelectBox.js', 'SelectFilter2.js')


class IdeaFormUpdate(forms.ModelForm):

    class Meta:
        model = Idea
        fields = ('title', 'oportunity', 'solution', 'target')
        labels = {
            'title': _('Title'),
            'oportunity': _('Oportunity'),
            'solution': _('Solution'),
            'target': _('Target'),
        }


class CriterionForm(forms.ModelForm):

    class Meta:
        model = Criterion
        fields = ('description', 'peso')
        labels = {'peso': _('Weight'), 'description': _('Description')}


class CategoryForm(forms.ModelForm):

    class Meta:
        model = Category
        fields = ('title', 'description', )
        labels = {'title': _('Title'), 'description': _('Description')}


class CategoryImageForm(forms.ModelForm):

    class Meta:
        model = Category_Image
        fields = ('description', 'image', 'category')
        labels = {'description': _('Description'), 'image': _('Image'), 'category': _('Category')}


class ChallengeForm(forms.ModelForm):
    x = forms.FloatField(widget=forms.HiddenInput())
    y = forms.FloatField(widget=forms.HiddenInput())
    width = forms.FloatField(widget=forms.HiddenInput())
    height = forms.FloatField(widget=forms.HiddenInput())

    description = MartorFormField(
        label=_('Description'),
        max_length=Challenge._meta.get_field('description').max_length
    )

    class Meta:
        model = Challenge
        fields = (
            'title',
            'image',
            'x',
            'y',
            'width',
            'height',
            'summary',
            'requester',
            'description',
            'active',
            'limit_date',
            'init_date',
            'featured',
            'category',
        )
        labels = {
            'title': _('Title'),
            'image': _('Image'),
            'summary': _('Summary'),
            'requester': _('Requester'),
            'active': _('Active'),
            'limit_date': _('Limit Date'),
            'init_date': _('Init Date'),
            'featured': _('Featured'),
            'category': _('Category')}
        widgets = {
            'limit_date': forms.DateInput(attrs={'placeholder': 'dd/mm/aaaa'}),
            'init_date': forms.DateInput(attrs={'placeholder': 'dd/mm/aaaa'}),
        }

    def save(self):
        data = self.cleaned_data

        challenge = Challenge(title=data['title'],
                              image=data['image'],
                              summary=data['summary'],
                              requester=data['requester'],
                              description=data['description'],
                              limit_date=data['limit_date'],
                              init_date=data['init_date'],
                              active=data['active'],
                              featured=data['featured'],
                              category=data['category'],
                              discarted=False)

        x = self.cleaned_data.get('x')
        y = self.cleaned_data.get('y')
        w = self.cleaned_data.get('width')
        h = self.cleaned_data.get('height')

        image = Image.open(challenge.image)
        cropped_image = image.crop((x, y, w+x, h+y))

        img_path = challenge.image.path.split('/')
        img_name = img_path.pop()
        img_path.append('challenges')
        img_path.append(img_name)
        img_path = "/".join(img_path)

        cropped_image.save(img_path, format='JPEG', subsampling=0, quality=100)

        challenge.image = '/challenges/'+img_name

        return challenge


class UseTermForm(forms.ModelForm):

    class Meta:
        model = Use_Term
        fields = ('term', 'init_date', 'final_date')
        labels = {'term': _('Term'), 'init_date': _('Initial Date'), 'final_date': _('Final Date')}
        widgets = {
            'term': TinyMCE(),
        }


class EvaluationForm(forms.Form):
    FORMAT_ID = 'category_dimension_%s'
    FORMAT_ID_NOTE = 'note_dimension_%s'

    def __init__(self, *args, **kwargs):
        dimensions = kwargs.pop('extra', None)
        initial_arguments = kwargs.pop('initial', None)
        super(EvaluationForm, self).__init__(*args, **kwargs)

        if initial_arguments:
            for i in initial_arguments:
                id_field = self.FORMAT_ID % initial_arguments[i].dimension.pk
                self.fields[id_field] = forms.ModelChoiceField(
                    queryset=initial_arguments[i].dimension.category_dimension_set,
                    label=initial_arguments[i].dimension.title,
                    initial=initial_arguments[i].category_dimension.id,
                    help_text=initial_arguments[i].dimension.description
                )

                id_field_note = self.FORMAT_ID_NOTE % initial_arguments[i].dimension.pk
                self.fields[id_field_note] = forms.CharField(initial=initial_arguments[i].note,
                                                             widget=forms.Textarea,
                                                             label='',
                                                             required=False)
        if dimensions:
            for dim in dimensions:
                self.fields[self.FORMAT_ID % dim.pk] = forms.ModelChoiceField(
                    queryset=dim.category_dimension_set,
                    label=dim.title,
                    help_text=dim.description,
                )
                self.fields[self.FORMAT_ID_NOTE % dim.pk] = forms.CharField(
                    widget=forms.Textarea,
                    label='',
                    required=False,
                )


class DimensionForm(forms.ModelForm):

    class Meta:
        model = Dimension
        fields = ('title', 'description', 'weight', 'init_date', 'final_date')
        labels = {
            'title': _('Title'), 'description': _('Description'), 'weight': _('Weight'),
            'init_date': _('Initial Date'), 'final_date': _('Final Date'),
            }
        widgets = {
            'init_date': forms.DateInput(attrs={'placeholder': 'dd/mm/aaaa'}),
            'final_date': forms.DateInput(attrs={'placeholder': 'dd/mm/aaaa'}),
        }
