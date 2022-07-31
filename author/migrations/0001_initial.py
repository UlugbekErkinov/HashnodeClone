# Generated by Django 4.0.6 on 2022-07-31 12:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AuthorFollower',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('followers', models.ManyToManyField(blank=True, to='author.authorfollower')),
            ],
        ),
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated at')),
                ('first_name', models.CharField(max_length=128)),
                ('last_name', models.CharField(max_length=128)),
                ('avatar', models.ImageField(upload_to='avatar/')),
                ('bio', models.TextField()),
                ('work_place', models.CharField(max_length=128, null=True)),
                ('linkedin_link', models.CharField(max_length=128)),
                ('instagram_link', models.CharField(max_length=128)),
                ('facebook_link', models.CharField(max_length=128)),
                ('github_link', models.CharField(max_length=128)),
                ('posts_count', models.IntegerField(default=0)),
                ('is_top', models.BooleanField(default=False)),
                ('created_by', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_createdby', to=settings.AUTH_USER_MODEL)),
                ('modified_by', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_modifiedby', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
