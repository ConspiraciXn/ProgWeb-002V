# Generated by Django 4.2.2 on 2023-06-10 18:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(blank=True, max_length=100)),
                ('descripcion', models.CharField(blank=True, max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(blank=True, max_length=100)),
                ('valor', models.IntegerField(blank=True)),
                ('stock', models.IntegerField(blank=True)),
                ('imagen', models.ImageField(upload_to='imagenProductos/')),
                ('categoria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appTiendaWeb.categoria')),
            ],
        ),
    ]