import regex
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView, RedirectView
from django.views import defaults as default_views
from allauth.account.views import confirm_email as allauthemailconfirmation
from rest_framework_swagger.views import get_swagger_view
from django.contrib.auth.views import password_reset, \
    password_reset_done, password_reset_confirm, password_reset_complete


urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='pages/home.html'), name='home'),
    url(r'^about/$', TemplateView.as_view(template_name='pages/about.html'), name='about'),
    # Django Admin, use {% url 'admin:index' %}
    url(settings.ADMIN_URL, admin.site.urls),

    # User management
    url(r'^users/', include('main_auth.users.urls', namespace='users')),
    url(r'^accounts/', include('allauth.urls')),

    # Your stuff: custom urls includes go here
    url(r'^rest-auth/', include('rest_auth.urls')),
    url(r'^rest-auth/registration/account-confirm-email/(?P<key>[-:\w]+)/$', allauthemailconfirmation, name='account_confirm_email'),
    url(r'^rest-auth/registration/account-confirm-email/(?P<key>[-:\w]+)/$', TemplateView.as_view(template_name=''), name='account_confirm_email'),
    url(r'^rest-auth/registration/', include('rest_auth.registration.urls')),

    # Auto Document
    url(r'^docs/$', get_swagger_view(title='API Docs'), name='api_docs'),

    url(r'^test/', TemplateView.as_view(template_name="test/home.html"), name='home'),
    url(r'^signup/$', TemplateView.as_view(template_name="test/signup.html"),
        name='signup'),
    url(r'^email-verification/$',
        TemplateView.as_view(template_name="test/email_verification.html"),
        name='email-verification'),
    url(r'^login/$', TemplateView.as_view(template_name="test/login.html"),
        name='login'),
    url(r'^logout/$', TemplateView.as_view(template_name="test/logout.html"),
        name='logout'),
    url(r'^password-reset/$',
        TemplateView.as_view(template_name="test/password_reset.html"),
        name='password-reset'),
    url(r'^password-reset/confirm/$',
        TemplateView.as_view(template_name="test/password_reset_confirm.html"),
        name='password-reset-confirm'),
    url(r'^user-details/$',
        TemplateView.as_view(template_name="test/user_details.html"),
        name='user-details'),
    url(r'^password-change/$',
        TemplateView.as_view(template_name="test/password_change.html"),
        name='password-change'),
    # this url is used to generate email content
    url(r'^password-reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        TemplateView.as_view(template_name="test/password_reset_confirm.html"),
        name='password_reset_confirm'),
    url(r'^account/', include('allauth.urls')),
    url(r'^accounts/profile/$', RedirectView.as_view(url='/', permanent=True), name='profile-redirect'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        url(r'^400/$', default_views.bad_request, kwargs={'exception': Exception('Bad Request!')}),
        url(r'^403/$', default_views.permission_denied, kwargs={'exception': Exception('Permission Denied')}),
        url(r'^404/$', default_views.page_not_found, kwargs={'exception': Exception('Page not Found')}),
        url(r'^500/$', default_views.server_error),
    ]
    if 'debug_toolbar' in settings.INSTALLED_APPS:
        import debug_toolbar
        urlpatterns = [
            url(r'^__debug__/', include(debug_toolbar.urls)),
        ] + urlpatterns


#   Вариант переопределения  из allauth
    #               url(
    #                   regex=r'^contrib/password_reset/$',
    #                   view=password_reset,
    #                   name='password_reset'
    #               ),
    #               url(
    #                   regex=r'^contrib/password_reset/done/$',
    #                   view=password_reset_done,
    #                   name='password_reset_done'
    #               ),
    #               url(
    #                   regex=r'^contrib/reset/(?P<uidb64>[0-9A-Za-z_\-]+)'
    #                         r'/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
    #                   view=password_reset_confirm,
    #                   name='password_reset_confirm'
    #               ),
    #               url(
    #                   regex=r'^contrib/reset/done/$',
    #                   view=password_reset_complete,
    #                   name='password_reset_complete'
    #               ),
