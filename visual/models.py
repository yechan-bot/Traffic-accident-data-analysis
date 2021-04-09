from django.db import models
from django.urls import reverse

class list(models.Model):
    no = models.AutoField(primary_key=True)
    발생년 = models.IntegerField(blank=True, null=True)
    발생년월일시 = models.IntegerField(blank=True, null=True)
    발생시 = models.IntegerField(blank=True, null=True)
    주야 = models.CharField(max_length=50, blank=True, null=True)
    요일 = models.CharField(max_length=50, blank=True, null=True)
    사망자수 = models.IntegerField(blank=True, null=True)
    부상자수 = models.IntegerField(blank=True, null=True)
    중상자수 = models.IntegerField(blank=True, null=True)
    경상자수 = models.IntegerField(blank=True, null=True)
    부상신고자수 = models.IntegerField(blank=True, null=True)
    발생지시도 = models.CharField(max_length=50, blank=True, null=True)
    발생지시군 = models.CharField(max_length=50, blank=True, null=True)
    사고유형_대분류 = models.CharField(max_length=50, blank=True, null=True)
    사고유형_중분류 = models.CharField(max_length=50, blank=True, null=True)
    사고유형 = models.CharField(max_length=50, blank=True, null=True)
    가해자법규위반 = models.CharField(max_length=50, blank=True, null=True)
    도로형태_대분류 = models.CharField(max_length=50, blank=True, null=True)
    도로형태 = models.CharField(max_length=50, blank=True, null=True)
    가해자_당사자종별 = models.CharField(max_length=50, blank=True, null=True)
    피해자_당사자종별 = models.CharField(max_length=50, blank=True, null=True)
    발생위치x = models.BigIntegerField(db_column='발생위치X', blank=True, null=True)  # Field name made lowercase.
    발생위치y = models.BigIntegerField(db_column='발생위치Y', blank=True, null=True)  # Field name made lowercase.
    경도 = models.FloatField(blank=True, null=True)
    위도 = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = '어린이사고'