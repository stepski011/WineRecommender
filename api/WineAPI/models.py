# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
import json


class LocalWine(models.Model):
    lw_id = models.IntegerField(primary_key=True)
    lw_name = models.TextField()
    lw_country = models.TextField(blank=True, null=True)
    lw_region = models.TextField(blank=True, null=True)
    lw_year = models.IntegerField(blank=True, null=True)
    lw_type = models.TextField(blank=True, null=True)
    lw_price = models.FloatField(blank=True, null=True)
    lw_url = models.TextField(blank=True, null=True)
    lw_thumb = models.TextField(blank=True, null=True)
    lw_description = models.TextField(blank=True, null=True)
    lw_seller = models.IntegerField(blank=True, null=True)
    wine = models.ForeignKey('Wine', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'local_wine'


class Wine(models.Model):
    wine_id = models.IntegerField(primary_key=True)
    wine_name = models.TextField(blank=True, null=True)
    wine_alcohol = models.TextField(blank=True, null=True)
    wine_type = models.TextField(blank=True, null=True)
    wine_year = models.IntegerField(blank=True, null=True)
    wine_country = models.TextField(blank=True, null=True)
    wine_region = models.TextField(blank=True, null=True)
    wine_price = models.FloatField(blank=True, null=True)
    wine_rating = models.FloatField(blank=True, null=True)
    wine_thumb = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'wine'


class WineFlavor(models.Model):
    wine_flavor_id = models.IntegerField(primary_key=True)
    black_fruit = models.FloatField(blank=True, null=True)
    citrus_fruit = models.FloatField(blank=True, null=True)
    dried_fruit = models.FloatField(blank=True, null=True)
    earth = models.FloatField(blank=True, null=True)
    floral = models.FloatField(blank=True, null=True)
    microbio = models.FloatField(blank=True, null=True)
    non_oak = models.FloatField(blank=True, null=True)
    oak = models.FloatField(blank=True, null=True)
    red_fruit = models.FloatField(blank=True, null=True)
    spices = models.FloatField(blank=True, null=True)
    tree_fruit = models.FloatField(blank=True, null=True)
    tropical_fruit = models.FloatField(blank=True, null=True)
    vegetal = models.FloatField(blank=True, null=True)
    wine = models.ForeignKey(Wine, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'wine_flavor'


class WineStructure(models.Model):
    wine_structure_id = models.IntegerField(primary_key=True)
    wine_acidity = models.FloatField(blank=True, null=True)
    wine_fizziness = models.FloatField(blank=True, null=True)
    wine_intensity = models.FloatField(blank=True, null=True)
    wine_tannin = models.FloatField(blank=True, null=True)
    wine_sweetness = models.FloatField(blank=True, null=True)
    wine = models.ForeignKey(Wine, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'wine_structure'


class WineDto:
    def __init__(self, id, name, url=""):
        self.id = id
        self.name = name
        self.picture_url = url

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)
