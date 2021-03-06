# Generated by Django 3.2 on 2021-06-23 19:23

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('debate', '0007_debate_proslike'),
    ]

    operations = [
        migrations.RenameField(
            model_name='debate',
            old_name='proslike',
            new_name='like',
        ),
        migrations.AlterField(
            model_name='cons',
            name='conslike',
            field=models.ManyToManyField(blank=True, null=True, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='pros',
            name='proslike',
            field=models.ManyToManyField(blank=True, null=True, to=settings.AUTH_USER_MODEL),
        ),
    ]
