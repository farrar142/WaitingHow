# Generated by Django 4.0.1 on 2022-01-18 09:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Shop',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='매장이름')),
                ('bizNum', models.CharField(blank=True, max_length=20, null=True, verbose_name='사업자등록번호')),
                ('zipNo', models.CharField(max_length=10, verbose_name='우편번호')),
                ('address', models.CharField(max_length=200, verbose_name='매장위치')),
                ('detailAddress', models.CharField(max_length=200, verbose_name='상세주소')),
                ('reg_date', models.DateTimeField(auto_now_add=True, verbose_name='등록날짜')),
                ('update_date', models.DateTimeField(auto_now=True, verbose_name='갱신날짜')),
                ('lat', models.CharField(max_length=30, verbose_name='위도')),
                ('lng', models.CharField(max_length=30, verbose_name='경도')),
                ('master', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
