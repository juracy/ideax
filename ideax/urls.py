from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from django.views.i18n import JavaScriptCatalog
from django.conf.urls import url
from . import views
from ideax.feeds import *

urlpatterns = [
    url(r'^media/uploader/$', views.markdown_uploader, name='markdown_uploader_page'),
    path('martor/', include('martor.urls')),
    url(r'^tinymce/', include('tinymce.urls')),
    path('admin/', admin.site.urls),
    path('accounts/login/', auth_views.login, name='login'),
    path('accounts/logout/', auth_views.logout, name='logout'),
    path('', views.index, name='index'),
    path('idea/list', views.idea_list, name='idea_list'),
    path('idea/<int:pk>/', views.idea_detail, name='idea_detail'),
    path('idea/new/', views.idea_new, name='idea_new'),
    path('idea/new/<int:challenge_pk>', views.idea_new_from_challenge, name='idea_new_from_challenge'),
    path('idea/<int:pk>/edit/', views.idea_edit, name='idea_edit'),
    path('idea/<int:pk>/remove/', views.idea_remove, name='idea_remove'),
    path('criterion/', views.criterion_list, name='criterion_list'),
    path('criterion/new/', views.criterion_new, name='criterion_new'),
    path('criterion/<int:pk>/edit/', views.criterion_edit, name='criterion_edit'),
    path('criterion/<int:pk>/remove/', views.criterion_remove, name='criterion_remove'),
    path('idea/<int:pk>/like/', views.like_popular_vote, name='like_ideia'),
    path('idea/<int:pk>/dislike/', views.like_popular_vote, name='dislike_ideia'),
    path('idea/<int:pk>/changephase/<int:new_phase>/', views.change_idea_phase, name='change_phase'),
    path('idea/filter/<int:phase_pk>', views.idea_filter, name ="idea_filter"),
    path('category/new/', views.category_new, name='category_new'),
    path('category/list/', views.category_list, name='category_list'),
    path('category/<int:pk>/edit/', views.category_edit, name='category_edit'),
    path('category/<int:pk>/remove/', views.category_remove, name='category_remove'),
    #path('idea/comment/<int:pk>', views.form_redirect, name='form'),
    path('post/comment/', views.post_comment, name='post_comment'),
    path('idea/comments/<int:pk>/', views.idea_comments, name='idea_comments'),
    path('idea/evaluation/<int:idea_pk>/', views.idea_evaluation, name='evaluation'),
    path('term/accept', views.accept_use_term, name="accept_term"),
    path('term', views.get_term_of_user, name="term_of_use"),
    path('feed/comment/latest',Comment_Feed()),
    path('feed/idea/latest', New_Idea_Feed(), name="rss"),
    path('report/idea/<int:idea_id>/detail/', views.idea_detail_pdf, name="idea_detail_pdf"),
    path('challenge/<int:challenge_pk>/', views.challenge_detail, name="challenge_detail"),
    path('challenge/new/', views.challenge_new, name='challenge_new'),
    path('challenge/edit/<int:challenge_pk>', views.challenge_edit, name='challenge_edit'),
    path('challenge/list/', views.challenge_list, name='challenge_list'),
    path('report', views.report_ideas, name='report_ideas'),
    path('useterm/new/', views.use_term_new, name='use_term_new'),
    path('useterm/list/', views.use_term_list, name='use_term_list'),
    path('useterm/', views.get_valid_use_term, name='use_term'),
    path('useterm/<int:pk>/', views.use_term_detail, name='use_term_detail'),
    path('useterm/<int:pk>/edit/', views.use_term_edit, name='use_term_edit'),
    path('useterm/<int:pk>/remove/', views.use_term_remove, name='use_term_remove'),
    path('categoryimage/new/', views.category_image_new, name='category_image_new'),
    path('categoryimage/list/', views.category_image_list, name='category_image_list'),
    path('categoryimage/<int:pk>/edit/', views.category_image_edit, name='category_image_edit'),
    path('categoryimage/<int:pk>/remove/', views.category_image_remove, name='category_image_remove'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
