# Generated by Django 5.0.4 on 2024-04-09 17:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oddam_app', '0002_institution_donation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='institution',
            name='type',
            field=models.CharField(choices=[('fundacja', 'Fundacja'), ('organizacja pozarządowa', 'Organizacja pozarządowa'), ('zbiórka lokalna', 'Zbiórka lokalna')], default='fundacja', max_length=32),
        ),
    ]
