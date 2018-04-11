# Generated by Django 2.0.4 on 2018-04-07 17:50

import uuid

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('customer', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='RawReview',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.PositiveIntegerField()),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('text', models.TextField()),
                ('dogs', models.CharField(max_length=200)),
                ('owner', models.CharField(max_length=100)),
                ('owner_image', models.URLField()),
                ('owner_phone_number', models.CharField(max_length=12)),
                ('owner_email', models.EmailField(max_length=254)),
                ('sitter', models.CharField(max_length=100)),
                ('sitter_image', models.URLField()),
                ('sitter_phone_number', models.CharField(max_length=12)),
                ('sitter_email', models.EmailField(max_length=254)),
                ('owner_object', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='raw_reviews', to='customer.Owner')),
                ('sitter_object', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='raw_reviews', to='customer.Sitter')),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('rating', models.PositiveIntegerField()),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('text', models.TextField()),
                ('dogs', models.CharField(max_length=200)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='customer.Owner')),
                ('sitter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='customer.Sitter')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
