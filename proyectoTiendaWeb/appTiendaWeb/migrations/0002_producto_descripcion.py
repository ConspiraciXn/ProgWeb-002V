# Generated by Django 4.2.2 on 2023-06-10 18:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appTiendaWeb', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='producto',
            name='descripcion',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]
