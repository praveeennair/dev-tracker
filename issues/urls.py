from django.urls import path

from .views import ReporterView, IssueView


urlpatterns = [
    path(
        'reporters/', ReporterView.as_view(), name='reporters'
    ),

    path(
        'issues/', IssueView.as_view(), name='issues'
    ),
]
