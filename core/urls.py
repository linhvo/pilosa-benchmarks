from django.conf.urls import url

from . import views
from core.views import ChartView

urlpatterns = [
    # url(r'^$', views.index, name='index'),
    url(r'^indexes/(?P<slug>[\w-]+)/$', ChartView.as_view(), name='home'),
]