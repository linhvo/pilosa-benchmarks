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
        # results = Benchmark.objects.filter(config_index=kwargs.get('slug'), name__contains=self.query)

        context = super(ChartView, self).get_context_data(**kwargs)
        conn = psycopg2.connect("dbname='%s'" % "benchmarks")
        cur = conn.cursor()
        if not self.query:
            all_count = """SELECT pilosa_version, run_id, stats_mean_us, name FROM benchmarks WHERE config_index='%s';"""
            psql = all_count % kwargs.get('slug')
        else:
            all_count = """SELECT pilosa_version, run_id, stats_mean_us, name FROM benchmarks WHERE name LIKE '%s' AND config_index='%s';"""
            psql = all_count % (self.query, kwargs.get('slug'))
        try:
            cur.execute(psql)
            conn.commit()
        except Exception as exc:
            print(exc)
            conn.rollback()
            import ipdb

            ipdb.set_trace()

        filters = cur.fetchall()
        if len(filters) == 0:
            return
        version_map = defaultdict(list)
        for ver in filters:
            version_map[ver[0]].append((ver[1], ver[2], ver[3]))
        if not self.query:
            traces = [go.Box(y=[int(val[1]) for val in version_map[key]],
                             x=[val[2] for val in version_map[key]],
                             name=key,
                             boxpoints='all',
                             whiskerwidth=1, ) for key in version_map.keys()]
        else:
            traces = [go.Box(y=[int(val[1]) for val in version_map[key]],
                             x=[val[0] for val in version_map[key]],
                             name=key, boxpoints='outliers',
                             whiskerwidth=0.2, ) for key in version_map.keys()]
        data1 = [trace for trace in traces]
        div = opy.plot(data1, auto_open=False, output_type='div')
        context['graph'] = div
        return context