# Generated by Django 3.2 on 2021-06-23 10:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('debate', '0004_rename_pros_tags_debate_tags'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cons',
            name='comments',
            field=models.JSONField(blank=True, default=list, null=True),
        ),
    ]