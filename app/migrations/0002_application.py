# Generated by Django 4.0.4 on 2022-05-01 07:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=30)),
                ('description', models.TextField()),
                ('address', models.CharField(max_length=30)),
                ('image', models.ImageField(default='application.jpg', upload_to='')),
                ('status', models.CharField(choices=[('Waiting ...', 'Waiting ...'), ('Expecting a visit!', 'Expecting a visit!'), ('In progress ...', 'In progress ...'), ('Completed', 'Completed')], default='Waiting ...', max_length=18)),
                ('date_of_visit_by_technician', models.DateField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('technician', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]