# Generated by Django 3.1 on 2021-06-07 12:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
        ('courses', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('target', models.CharField(choices=[('Engineering', (('jee-mains', 'JEE-Main'), ('jee-Adv', 'JEE Advanced'), ('bits', 'Bits'))), ('Medical', (('neet', 'NEET'), ('Aiims', 'AIIMS'))), ('other', 'Other')], default='other', max_length=20)),
                ('title', models.CharField(max_length=200)),
                ('Language_choices', models.CharField(choices=[('eng', 'English'), ('Hindi', 'Hindi')], default='English', max_length=20)),
                ('slug', models.SlugField(max_length=200, unique=True)),
                ('overview', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='courses_created', to='account.account')),
                ('students', models.ManyToManyField(blank=True, related_name='courses_joined', to='account.Account')),
            ],
            options={
                'ordering': ['title'],
            },
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.PositiveIntegerField(default='0')),
                ('title', models.CharField(max_length=200)),
                ('slug', models.SlugField(max_length=200, unique=True)),
                ('target', models.CharField(choices=[('Engineering', (('jee-mains', 'JEE-Main'), ('jee-Adv', 'JEE Advanced'), ('bits', 'Bits'))), ('Medical', (('neet', 'NEET'), ('Aiims', 'AIIMS'))), ('other', 'Other')], default='other', max_length=20)),
            ],
            options={
                'ordering': ['number', 'title'],
            },
        ),
        migrations.DeleteModel(
            name='Courses',
        ),
        migrations.AddField(
            model_name='course',
            name='subject',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='courses', to='courses.subject'),
        ),
    ]
