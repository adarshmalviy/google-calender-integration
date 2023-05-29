from django.urls import path
from . import views
# from .views import GoogleCalendarInitView, GoogleCalendarRedirectView

urlpatterns = [
    # path('init/', GoogleCalendarInitView.as_view(), name='init'),
    # path('redirect/', GoogleCalendarRedirectView.as_view(), name='calendar_redirect'),
    # # path('redirect/', GoogleCalendarRedirectView.as_view(), name='redirect'),
    path('init/', views.GoogleCalendarInitView, name='google_permission'),
    path('redirect/', views.GoogleCalendarRedirectView, name='google_redirect')
]
    