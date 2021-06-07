# Generated by Django 3.1 on 2021-06-07 16:45

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Debate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('pros', models.JSONField(blank=True, default=dict, null=True)),
                ('cons', models.JSONField(blank=True, default=dict, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
