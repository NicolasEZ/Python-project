# Generated by Django 2.2 on 2020-02-27 01:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HallPass', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Celeb',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ranking', models.PositiveSmallIntegerField()),
                ('photo', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('comments', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.DeleteModel(
            name='Trip',
        ),
    ]