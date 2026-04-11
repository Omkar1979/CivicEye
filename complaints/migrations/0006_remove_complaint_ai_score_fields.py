from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('complaints', '0005_complaint_fake_score_complaint_image_score_and_more'),
    ]

    operations = [
        migrations.RemoveField(model_name='complaint', name='fake_score'),
        migrations.RemoveField(model_name='complaint', name='image_score'),
        migrations.RemoveField(model_name='complaint', name='is_suspicious'),
        migrations.RemoveField(model_name='complaint', name='text_score'),
    ]
