# Generated by Django 2.0.1 on 2018-05-07 21:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ideax', '0016_idea_summary'),
    ]

    operations = [
        migrations.AlterField(
            model_name='idea',
            name='summary',
            field=models.TextField(max_length=140, null=True),
        ),
    ]