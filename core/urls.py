from django.conf.urls import url

from . import views
from core.views import ChartView, TimeseriesView, GroupedView, GroupsView

urlpatterns = [
    # url(r'^$', views.index, name='index'),
    url(r'^indexes/(?P<slug>[\w-]+)/$', ChartView.as_view(), name='home'),
    url(r'^timeseries/$', TimeseriesView.as_view(), name='timeseries'),
    url(r'^grouped/$', GroupedView.as_view(), name='grouped'),
    url(r'^groups/(?P<slug>[\w-]+)/$', GroupsView.as_view(), name='groups'),
]
