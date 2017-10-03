# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
from core.models import Benchmark, Run
import plotly.plotly as py
import plotly.graph_objs as go
import plotly.offline as opy
import psycopg2
from collections import defaultdict
from django.views.generic.base import TemplateView


class ChartView(TemplateView):

    template_name = "chart.html"

    def get(self, request, *args, **kwargs):
        self.query = request.GET.get('query')
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        if self.query:
            results = Benchmark.objects.filter(config_index=kwargs.get('slug'), name__icontains=self.query)
        else:
            results = Benchmark.objects.filter(config_index=kwargs.get('slug'))

        context = super(ChartView, self).get_context_data(**kwargs)
        if len(results) == 0:
            return
        version_map = defaultdict(list)
        for ver in results:
            version_map[ver.pilosa_version].append((ver.run_id, ver.stats_mean_us, ver.name))
        if not self.query:
            traces = [go.Box(y=[int(val[1]) for val in version_map[key]],
                             x=[val[2] for val in version_map[key]],
                             name=key,
                             boxpoints='outliers',
                             whiskerwidth=1, ) for key in version_map.keys()]
        else:
            traces = [go.Box(y=[int(val[1]) for val in version_map[key]],
                             x=[val[0] for val in version_map[key]],
                             name=key, boxpoints='outliers',
                             whiskerwidth=0.2, ) for key in version_map.keys()]
        data1 = [trace for trace in traces]

        fig = go.Figure(data=data1)
        div = opy.plot(fig, auto_open=False, output_type='div')
        context['graph'] = div
        return context