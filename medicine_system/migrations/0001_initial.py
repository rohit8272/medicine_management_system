# Generated by Django 4.1.13 on 2024-03-08 08:38

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('creted_at', models.DateField(auto_now_add=True)),
                ('name', models.CharField(max_length=100)),
                ('age', models.IntegerField(default=30)),
                ('gender', models.CharField(max_length=10)),
                ('disease', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'customer_details',
            },
        ),
        migrations.CreateModel(
            name='Medicine',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('creted_at', models.DateField(auto_now_add=True)),
                ('name', models.CharField(max_length=100)),
                ('price', models.IntegerField(default=100)),
                ('expiry_date', models.CharField(max_length=50)),
                ('weight_in_ML', models.IntegerField(default=50)),
                ('use_in_disease', models.CharField(max_length=100)),
            ],
        ),
    ]
