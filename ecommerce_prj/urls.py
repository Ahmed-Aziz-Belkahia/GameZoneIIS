
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.conf.urls import handler404, handler500

urlpatterns = [
    # path('jet/', include('jet.urls', 'jet')),  # Django JET URLS
    path('khalabiza/', admin.site.urls),
    
    path('user/', include("userauths.urls")),
    path('b/', include("core.urls")),
    path('vendor/', include("vendor.urls")),
    path('base/', include("addons.urls")),
    path('report/', include("reports.urls")),
    path('blog/', include("blog.urls")),
    path('help-center/', include("help_center.urls")),

    
    # path("ckeditor/", include("ckeditor_uploader.urls")),
    path("ckeditor5/", include('django_ckeditor_5.urls')),
    
    # Change Password
    path('user/change-password/',auth_views.PasswordChangeView.as_view(template_name='userauths/password-reset/change-password.html',success_url = '/user/password-reset-complete/'),name='change_password'),
    
    
    # Re-Captcha Validation
    # path('captcha/', include('captcha.urls')),
    
    # Password Reset
    path('user/password-reset/', auth_views.PasswordResetView.as_view( template_name='userauths/password-reset/password_reset.html', subject_template_name='userauths/password-reset/password_reset_subject.txt', email_template_name='userauths/password-reset/password_reset_email.html', success_url='/user/check_email/' ), name='password_reset'),
    path('user/password-reset/done/', auth_views.PasswordResetDoneView.as_view( template_name='userauths/password-reset/password_reset_done.html' ), name='password_reset_done'),
    path('user/password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view( template_name='userauths/password-reset/password_reset_confirm.html' ), name='password_reset_confirm'),
    path('user/password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='userauths/password-reset/password_reset_complete.html'), name='password_reset_complete'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
urlpatterns + [path('', include("store.urls"))]