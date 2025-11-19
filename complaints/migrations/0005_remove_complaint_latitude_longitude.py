# Generated manually to remove Google Maps integration

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('complaints', '0004_alter_like_complaint'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='complaint',
            name='latitude',
        ),
        migrations.RemoveField(
            model_name='complaint',
            name='longitude',
        ),
    ]

