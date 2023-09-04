# Generated by Django 4.2.1 on 2023-08-31 17:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('game_id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200, verbose_name='Título')),
            ],
            options={
                'verbose_name': 'Juego',
                'verbose_name_plural': 'Juegos',
            },
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Género')),
            ],
            options={
                'verbose_name': 'género',
                'verbose_name_plural': 'géneros',
            },
        ),
        migrations.CreateModel(
            name='Spec',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Especificaciones')),
            ],
            options={
                'verbose_name': 'spec',
                'verbose_name_plural': 'specs',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Tag')),
            ],
            options={
                'verbose_name': 'tag',
                'verbose_name_plural': 'tags',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('user_id', models.CharField(max_length=200, primary_key=True, serialize=False)),
                ('steam_id', models.BigIntegerField()),
                ('items_count', models.IntegerField(verbose_name='Cantidad de Juegos')),
                ('user_url', models.URLField(verbose_name='Link al usuario')),
                ('games', models.ManyToManyField(to='games.game')),
            ],
            options={
                'verbose_name': 'Usuario',
                'verbose_name_plural': 'Usuarios',
            },
        ),
        migrations.CreateModel(
            name='GameInfo',
            fields=[
                ('game', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='games.game')),
                ('price', models.IntegerField(null=True, verbose_name='Precio')),
                ('release_date', models.DateField(null=True, verbose_name='Fecha de salida')),
                ('publisher', models.CharField(max_length=200, null=True, verbose_name='Editor')),
                ('developer', models.CharField(max_length=200, null=True, verbose_name='Desarrollador')),
                ('url', models.URLField(verbose_name='Url al juego')),
                ('early_access', models.BooleanField(verbose_name='¿Acceso anticipado?')),
                ('genres', models.ManyToManyField(to='games.genre', verbose_name='Géneros')),
                ('specs', models.ManyToManyField(to='games.spec', verbose_name='Especificaciones')),
                ('tags', models.ManyToManyField(to='games.tag', verbose_name='Tags')),
            ],
            options={
                'verbose_name': 'Detalles de juego',
                'verbose_name_plural': 'Detalles de juegos',
            },
        ),
    ]