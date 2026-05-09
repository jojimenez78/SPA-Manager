# Generated manually for social profile links

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0002_clienteperfil_foto'),
    ]

    operations = [
        migrations.AddField(
            model_name='clienteperfil',
            name='facebook',
            field=models.URLField(blank=True),
        ),
        migrations.AddField(
            model_name='clienteperfil',
            name='instagram',
            field=models.URLField(blank=True),
        ),
    ]
