# Generated by Django 2.2.6 on 2020-02-03 20:16

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('coin_id', models.IntegerField(blank=True, default=0)),
                ('token', models.CharField(max_length=255, unique=True)),
                ('date', models.DateTimeField(blank=True, null=True)),
                ('value', models.FloatField()),
                ('currency', models.CharField(blank=True, max_length=5)),
                ('order_id', models.CharField(blank=True, max_length=255, unique=True)),
                ('status', models.CharField(blank=True, max_length=50)),
            ],
        ),
    ]
