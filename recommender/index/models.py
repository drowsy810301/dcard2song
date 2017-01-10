# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin sqlcustom [app_label]'
# into your database.
from __future__ import unicode_literals

from django.db import models


class C03250(models.Model):
    name = models.TextField(blank=True, null=True)
    index = models.IntegerField(blank=True, null=True)
    val = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'c_03_250'


class C05100(models.Model):
    name = models.TextField(blank=True, null=True)
    index = models.IntegerField(blank=True, null=True)
    val = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'c_05_100'


class C05250(models.Model):
    name = models.TextField(blank=True, null=True)
    index = models.IntegerField(blank=True, null=True)
    val = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'c_05_250'


class C10500(models.Model):
    name = models.TextField(blank=True, null=True)
    index = models.IntegerField(blank=True, null=True)
    val = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'c_10_500'


class Crawling(models.Model):
    aname = models.TextField(blank=True, null=True)
    sname = models.TextField(blank=True, null=True)
    lyrics = models.TextField(blank=True, null=True)
    singer = models.TextField(blank=True, null=True)
    m = models.IntegerField(blank=True, null=True)
    y = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'crawling'


class S03250(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField(blank=True, null=True)
    index = models.IntegerField(blank=True, null=True)
    val = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 's_03_250'


class S05100(models.Model):
    name = models.TextField(blank=True, null=True)
    index = models.IntegerField(blank=True, null=True)
    val = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 's_05_100'


class S05250(models.Model):
    name = models.TextField(blank=True, null=True)
    index = models.IntegerField(blank=True, null=True)
    val = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 's_05_250'
