# Generated by Django 3.1.6 on 2021-02-04 13:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Concert',
            fields=[
                ('id', models.AutoField(auto_created=True,
                                        primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=255)),
                ('place', models.CharField(max_length=255)),
                ('place_url', models.URLField()),
                ('date', models.DateField()),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Price',
            fields=[
                ('id', models.AutoField(auto_created=True,
                                        primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.FloatField()),
                ('description', models.CharField(max_length=255)),
                ('concert', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE, to='concert.concert')),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True,
                                        primary_key=True, serialize=False, verbose_name='ID')),
                ('is_done', models.BooleanField(default=False)),
                ('date_created', models.DateTimeField(
                    default=django.utils.timezone.now, verbose_name='Время создания')),
                ('date_closed', models.DateTimeField(
                    default=None, null=True, verbose_name='Время закрытия')),
                ('amount_sum', models.FloatField(default=None,
                                                 null=True, verbose_name='Фактически пришло')),
                ('concert', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE, to='concert.concert')),
                ('price', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE, to='concert.price')),
                ('user', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True,
                                        primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(blank=True, default=None,
                                                                         help_text='Contact phone number', max_length=128, null=True, region=None)),
                ('user', models.OneToOneField(
                    on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
