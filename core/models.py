# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.postgres.fields import JSONField


class Run(models.Model):
    config = JSONField()
    uuid = models.CharField(max_length=250)
    pi_version = models.CharField(max_length=250)
    pi_build_time = models.DateTimeField()
    spawn_file = models.URLField()

    def __unicode__(self):
        return '<Run %s %s %s>' % (self.uuid, self.pi_version, self.pi_build_time)


class Benchmark(models.Model):
    run = models.ForeignKey(Run, on_delete=models.CASCADE)
    config = JSONField()
    stats = JSONField()
    extra = JSONField()
    name = models.CharField(max_length=250)
    stats_total_us = models.BigIntegerField()
    stats_max_us = models.BigIntegerField()
    stats_min_us = models.BigIntegerField()
    stats_num = models.BigIntegerField()
    stats_mean_us = models.BigIntegerField()
    config_index = models.CharField(max_length=250)
    agentnum = models.IntegerField()
    error = models.CharField(max_length=250)
    duration_us = models.BigIntegerField()
    pilosa_version = models.CharField(max_length=250)

    def __unicode__(self):
        return '<Benchmark %s %s %s>' % (self.name, self.stats_mean_us, self.pilosa_version)
